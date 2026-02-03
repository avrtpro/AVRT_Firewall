"""
AVRT Audit Router
Handles audit trail queries and compliance reporting

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import logging
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Header, Depends

from models.schemas import (
    AuditEntrySchema,
    AuditQueryRequest,
    AuditQueryResponse,
    ValidationStatus
)
from services.hash_service import HashService

logger = logging.getLogger("AVRT.Audit")

router = APIRouter()

# In-memory audit store (use database in production)
audit_store: List[dict] = []
hash_service = HashService()


async def verify_license(authorization: Optional[str] = Header(None)) -> str:
    """Verify license key from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    return authorization[7:]


@router.get("/audit", response_model=AuditQueryResponse)
async def get_audit_trail(
    limit: int = 100,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    status_filter: Optional[ValidationStatus] = None,
    license_key: str = Depends(verify_license)
):
    """
    Query audit trail entries.

    - **limit**: Maximum entries to return (default 100)
    - **start_date**: Filter by start date (ISO8601)
    - **end_date**: Filter by end date (ISO8601)
    - **status_filter**: Filter by validation status
    """
    logger.info(f"Audit query: limit={limit}, start={start_date}, end={end_date}")

    try:
        # Filter entries
        filtered_entries = audit_store.copy()

        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            filtered_entries = [
                e for e in filtered_entries
                if datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')) >= start_dt
            ]

        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            filtered_entries = [
                e for e in filtered_entries
                if datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')) <= end_dt
            ]

        if status_filter:
            filtered_entries = [
                e for e in filtered_entries
                if e['status'] == status_filter.value
            ]

        # Limit results
        filtered_entries = filtered_entries[-limit:]

        # Convert to schema
        entries = [
            AuditEntrySchema(
                request_id=e['request_id'],
                user_id=e.get('user_id'),
                input_text=e['input_text'],
                output_text=e['output_text'],
                status=ValidationStatus(e['status']),
                spiel_score=e.get('spiel_score'),
                tht_compliant=e.get('tht_compliant', True),
                violations=e.get('violations', []),
                timestamp=e['timestamp'],
                integrity_hash=e['integrity_hash']
            )
            for e in filtered_entries
        ]

        # Generate chain hash
        chain_hash = hash_service.generate_chain_hash([
            e['integrity_hash'] for e in filtered_entries
        ])

        return AuditQueryResponse(
            entries=entries,
            total_count=len(filtered_entries),
            chain_hash=chain_hash
        )

    except Exception as e:
        logger.error(f"Audit query error: {e}")
        raise HTTPException(status_code=500, detail=f"Audit query failed: {str(e)}")


@router.get("/audit/{request_id}")
async def get_audit_entry(
    request_id: str,
    license_key: str = Depends(verify_license)
):
    """
    Get a specific audit entry by request ID.
    """
    for entry in audit_store:
        if entry['request_id'] == request_id:
            return AuditEntrySchema(
                request_id=entry['request_id'],
                user_id=entry.get('user_id'),
                input_text=entry['input_text'],
                output_text=entry['output_text'],
                status=ValidationStatus(entry['status']),
                spiel_score=entry.get('spiel_score'),
                tht_compliant=entry.get('tht_compliant', True),
                violations=entry.get('violations', []),
                timestamp=entry['timestamp'],
                integrity_hash=entry['integrity_hash']
            )

    raise HTTPException(status_code=404, detail="Audit entry not found")


@router.post("/audit/verify")
async def verify_audit_integrity(
    request_ids: List[str],
    expected_chain_hash: str,
    license_key: str = Depends(verify_license)
):
    """
    Verify integrity of audit entries.

    Checks that the chain hash matches expected value.
    """
    entries = [
        e for e in audit_store
        if e['request_id'] in request_ids
    ]

    if len(entries) != len(request_ids):
        raise HTTPException(
            status_code=400,
            detail="Not all requested entries found"
        )

    computed_hash = hash_service.generate_chain_hash([
        e['integrity_hash'] for e in entries
    ])

    is_valid = computed_hash == expected_chain_hash

    return {
        "valid": is_valid,
        "computed_hash": computed_hash,
        "expected_hash": expected_chain_hash,
        "entries_verified": len(entries)
    }


@router.get("/audit/export")
async def export_audit_trail(
    format: str = "json",
    license_key: str = Depends(verify_license)
):
    """
    Export audit trail for compliance reporting.

    - **format**: Export format (json, csv)
    """
    if format not in ["json", "csv"]:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'json' or 'csv'")

    chain_hash = hash_service.generate_chain_hash([
        e['integrity_hash'] for e in audit_store
    ])

    if format == "json":
        return {
            "entries": audit_store,
            "total_count": len(audit_store),
            "chain_hash": chain_hash,
            "exported_at": datetime.utcnow().isoformat(),
            "format": "json"
        }
    else:
        # CSV format
        import io
        import csv

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'request_id', 'user_id', 'input_text', 'output_text',
            'status', 'spiel_score', 'tht_compliant', 'timestamp', 'integrity_hash'
        ])
        writer.writeheader()

        for entry in audit_store:
            writer.writerow({
                'request_id': entry['request_id'],
                'user_id': entry.get('user_id', ''),
                'input_text': entry['input_text'][:100],
                'output_text': entry['output_text'][:100],
                'status': entry['status'],
                'spiel_score': entry.get('spiel_score', ''),
                'tht_compliant': entry.get('tht_compliant', True),
                'timestamp': entry['timestamp'],
                'integrity_hash': entry['integrity_hash']
            })

        return {
            "csv_content": output.getvalue(),
            "total_count": len(audit_store),
            "chain_hash": chain_hash,
            "exported_at": datetime.utcnow().isoformat(),
            "format": "csv"
        }


# Internal function to add audit entries (called from validation router)
def add_audit_entry(entry: dict):
    """Add an entry to the audit store."""
    audit_store.append(entry)

    # Keep only last 10000 entries in memory
    if len(audit_store) > 10000:
        audit_store[:] = audit_store[-10000:]
