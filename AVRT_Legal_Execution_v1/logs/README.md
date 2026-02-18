# AVRT Legal Execution Logs

**Directory:** `AVRT_Legal_Execution_v1/logs/`

---

## Purpose

This directory stores runtime output from the AVRT determinism test harness and validation tools.

## Expected Files

| File | Source | Description |
|------|--------|-------------|
| `determinism_results_*.json` | `avrt_determinism_test_live.py` | Per-run JSON output with hash comparison, latency metrics, and provider-level results |
| `summary_metrics.json` | `avrt_determinism_test_live.py` | Aggregated metrics across all runs and providers |
| `validation_audit_*.log` | Runtime logging | Timestamped validation audit entries |

## Log Retention

- Logs are not committed to version control by default.
- Add `*.json` and `*.log` files here during local test runs.
- For CI/CD, configure artifact collection to capture this directory.

## Log Format

All JSON logs conform to the following top-level schema:

```json
{
  "run_id": "UUID",
  "timestamp": "ISO-8601",
  "provider": "openai | anthropic | gemini",
  "results": [],
  "metrics": {}
}
```

## .gitkeep

This file ensures the directory is tracked in version control while keeping actual log files local.
