# AVRT Regulatory Crosswalk v1.0

**Document ID:** AVRT-REG-2025-001
**Version:** 1.0.0
**Author:** Jason I. Proper, BGBH Threads LLC
**Patent Reference:** USPTO Application 19/236,935
**Date:** 2025-01-31

---

## 1. Purpose

This document maps AVRT system capabilities to requirements from applicable regulatory frameworks and standards for AI systems. Each mapping identifies the specific AVRT component that addresses the regulatory requirement.

---

## 2. EU AI Act (Regulation (EU) 2024/1689)

### 2.1 High-Risk AI System Requirements (Title III, Chapter 2)

| Article | Requirement | AVRT Implementation | Component |
|---------|-------------|---------------------|-----------|
| Art. 9 | Risk management system | SPIEL five-dimensional risk scoring with configurable thresholds | `SPIELEngine.enforce()` |
| Art. 9(2)(a) | Identification and analysis of known and foreseeable risks | Pattern-based detection across harmful, unethical, and dishonest categories | `policy_store.json:patterns` |
| Art. 9(4) | Risk elimination or mitigation measures | Enforcement actions: BLOCK, WARN, REVIEW, MODIFY based on threshold violations | `SPIELEngine._determine_action()` |
| Art. 10 | Data governance | Audit trail with SHA-256 integrity hashing; input/output logging | `AuditEntry`, `HashService` |
| Art. 11 | Technical documentation | System spec, claim chart, and this crosswalk document | `AVRT_Legal_Execution_v1/` |
| Art. 12 | Record-keeping | Audit trail with 1000-entry in-memory buffer; configurable persistence | `AVRTFirewall.audit_trail` |
| Art. 13 | Transparency | THT Transparency pillar; reasoning markers required for substantive claims | `THTValidator._verify_transparency()` |
| Art. 14 | Human oversight | REVIEW enforcement action routes flagged content for human evaluation | `EnforcementAction.REVIEW` |
| Art. 15 | Accuracy, robustness, cybersecurity | Fail-closed default; deterministic evaluation; no external dependencies at validation time | `SPIELEngine` fail-closed handler |

### 2.2 General-Purpose AI Model Obligations (Title VIII-A)

| Article | Requirement | AVRT Implementation |
|---------|-------------|---------------------|
| Art. 53(1)(a) | Technical documentation of training and testing | Determinism test harness with cross-provider comparison | `avrt_determinism_test_live.py` |
| Art. 53(1)(c) | Information for downstream providers | System specification and claim chart | `AVRT_System_Spec_v1.md` |

---

## 3. NIST AI Risk Management Framework (AI RMF 1.0)

### 3.1 Govern Function

| Subcategory | Requirement | AVRT Implementation |
|-------------|-------------|---------------------|
| GOVERN 1.1 | Legal and regulatory requirements identified | This crosswalk document |
| GOVERN 1.4 | Risk management process documented | SPIEL thresholds and enforcement actions defined in `policy_store.json` |
| GOVERN 4.1 | Organizational practices and competencies documented | SDK documentation and system spec |

### 3.2 Map Function

| Subcategory | Requirement | AVRT Implementation |
|-------------|-------------|---------------------|
| MAP 1.1 | Intended purpose described | System spec Section 1 (system overview and deployment modes) |
| MAP 2.1 | User interaction methods documented | Voice-first, text-only, and hybrid modes documented |
| MAP 5.1 | Impacts to individuals/groups considered | Safety, ethics, and integrity dimensions evaluate potential harms |

### 3.3 Measure Function

| Subcategory | Requirement | AVRT Implementation |
|-------------|-------------|---------------------|
| MEASURE 1.1 | AI system performance measurement | SPIEL composite scoring; determinism test harness |
| MEASURE 2.1 | Evaluations conducted regularly | Automated test suite with `--runs` parameter for repeated evaluation |
| MEASURE 2.5 | Accuracy evaluated and documented | Validation report with hash consistency and determinism rates |
| MEASURE 2.6 | Computational performance evaluated | Latency metrics: mean, min, max, p95 per provider |
| MEASURE 2.11 | Fairness assessed | Ethics dimension with configurable 90% threshold |

### 3.4 Manage Function

| Subcategory | Requirement | AVRT Implementation |
|-------------|-------------|---------------------|
| MANAGE 1.1 | Risk mitigation plans | Enforcement action hierarchy: ALLOW -> WARN -> REVIEW -> BLOCK |
| MANAGE 2.1 | Risk responses applied | Fail-closed architecture; automatic blocking on threshold breach |
| MANAGE 4.1 | Incidents monitored | Audit trail captures all validation events including violations |

---

## 4. ISO/IEC 42001:2023 (AI Management System)

| Clause | Requirement | AVRT Implementation |
|--------|-------------|---------------------|
| 6.1.2 | AI risk assessment | SPIEL five-dimensional scoring quantifies risk per interaction |
| 6.1.4 | AI risk treatment | Configurable enforcement actions per dimension |
| 7.2 | Competence | API documentation, SDK README, and system spec |
| 7.5 | Documented information | Full documentation package in `AVRT_Legal_Execution_v1/` |
| 8.1 | Operational planning and control | Policy configuration via `policy_store.json` |
| 8.4 | AI system impact assessment | Ethics and safety scoring with domain-specific custom rules |
| 9.1 | Monitoring, measurement, analysis | Audit trail, determinism testing, latency metrics |
| 10.1 | Continual improvement | Runtime-reloadable policy; configurable thresholds |

---

## 5. OWASP Top 10 for LLM Applications (2025)

| Risk ID | Risk | AVRT Mitigation |
|---------|------|-----------------|
| LLM01 | Prompt Injection | Input validated through SPIEL safety dimension before output delivery |
| LLM02 | Insecure Output Handling | All outputs gated through validation; blocked outputs replaced with safe alternatives |
| LLM03 | Training Data Poisoning | Out of scope (AVRT is post-generation middleware, not a training system) |
| LLM04 | Model Denial of Service | Rate limiting: 100/min, 5000/hr, burst 20 |
| LLM05 | Supply Chain Vulnerabilities | No external API calls during validation; local pattern matching only |
| LLM06 | Sensitive Information Disclosure | THT honesty pillar detects secretive language; audit logging with configurable content inclusion |
| LLM07 | Insecure Plugin Design | AVRT operates as read-only middleware with no plugin execution |
| LLM08 | Excessive Agency | AVRT blocks or warns on content exceeding safety/ethics thresholds; no autonomous action |
| LLM09 | Overreliance | THT truth pillar penalizes overconfident/absolutist claims |
| LLM10 | Model Theft | Out of scope (AVRT does not host model weights) |

---

## 6. HIPAA Considerations (where applicable)

| Requirement | AVRT Implementation |
|-------------|---------------------|
| Access controls (164.312(a)) | License key authentication; configurable user ID tracking |
| Audit controls (164.312(b)) | SHA-256 hashed audit entries per validation event |
| Integrity controls (164.312(c)) | Hash chain verification; blockchain timestamping option |
| Transmission security (164.312(e)) | HTTPS API endpoints; TLS for all remote communication |
| Medical advice detection | Custom rule `medical_advice_warning` triggers on healthcare-related content |

---

## 7. SOC 2 Type II Alignment

| Trust Service Criteria | Relevant Control | AVRT Implementation |
|----------------------|------------------|---------------------|
| CC6.1 | Logical access controls | License key validation; API key authentication |
| CC6.3 | Registered/authorized users | `user_id` parameter in audit trail; configurable allowed_users |
| CC7.2 | System monitoring | Audit trail with violation tracking; logging at INFO level |
| CC7.3 | Change management | Versioned `policy_store.json`; `reload_policy()` for controlled updates |
| CC8.1 | Design of controls | SPIEL/THT dual-protocol design; fail-closed architecture |
| PI1.1 | Processing integrity | Deterministic rule evaluation verified by test harness |

---

## 8. Crosswalk Summary Matrix

| Framework | Applicable Sections | Coverage Level | Primary AVRT Components |
|-----------|-------------------|----------------|------------------------|
| EU AI Act | Art. 9-15, Art. 53 | Partial (middleware-level controls) | SPIEL, THT, Audit, Policy |
| NIST AI RMF | GOVERN, MAP, MEASURE, MANAGE | Partial (operational controls) | SPIEL, THT, Test Harness |
| ISO/IEC 42001 | Clauses 6-10 | Partial (technical controls) | Full system |
| OWASP LLM Top 10 | LLM01-02, LLM04-06, LLM08-09 | 8/10 risks addressed | SPIEL, THT, Rate Limits |
| HIPAA | 164.312(a-e) | Partial (audit and integrity) | Audit, Hash, Custom Rules |
| SOC 2 Type II | CC6, CC7, CC8, PI1 | Partial (processing controls) | Auth, Audit, Policy, Tests |

**Note:** "Partial" indicates that AVRT addresses the technical implementation aspects within its scope as middleware. Organizational, procedural, and governance controls outside the middleware layer are the responsibility of the deploying organization.

---

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-01-31 | J. Proper | Initial regulatory crosswalk |
