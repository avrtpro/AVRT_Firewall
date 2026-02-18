# AVRT System Specification v1.0

**Document ID:** AVRT-SPEC-2025-001
**Version:** 1.0.0
**Status:** Active
**Author:** Jason I. Proper, BGBH Threads LLC
**Patent Reference:** USPTO Application 19/236,935
**License:** CC BY-NC 4.0
**Date:** 2025-01-31

---

## 1. System Overview

AVRT (Advanced Voice Reasoning Technology) is a middleware firewall that interposes between user-facing AI interfaces and upstream LLM providers. The system enforces deterministic rule evaluation on all AI-generated outputs prior to delivery, using two proprietary protocol stacks: SPIEL and THT.

### 1.1 Architectural Position

```
User Input --> [AI Provider] --> AVRT Firewall --> [Validated Output]
                                    |
                              SPIEL Engine
                              THT Validator
                              Audit Logger
                              Hash Chain
```

AVRT operates as a post-generation validation layer. It does not modify the generation process itself. It evaluates, scores, and gates all outputs through deterministic rule sets before delivery to the end user.

### 1.2 Deployment Modes

| Mode | Description | Entry Point |
|------|-------------|-------------|
| `voice-first` | Primary mode. Processes voice-transcribed inputs with full SPIEL/THT pipeline. | `VoiceFirewall` class |
| `text-only` | Text-based validation without voice preprocessing. | `AVRTFirewall` class |
| `hybrid` | Combined voice and text with mode auto-detection. | `AVRTFirewall` with mode toggle |

---

## 2. SPIEL Framework Specification

SPIEL is a five-dimensional scoring framework applied to all AI-generated outputs. Each dimension is evaluated independently. The composite score is the arithmetic mean of all five dimensions.

### 2.1 Dimension Definitions

| Dimension | ID | Description | Threshold | Weight |
|-----------|----|-------------|-----------|--------|
| Safety | `S` | Detection of harmful content patterns (violence, threats, dangerous instructions) | 85.0 | Equal (1/5) |
| Personalization | `P` | Presence of user-centric language and contextual adaptation markers | 70.0 | Equal (1/5) |
| Integrity | `I` | Absence of dishonest, secretive, or manipulative language patterns | 80.0 | Equal (1/5) |
| Ethics | `E` | Absence of unethical content (deception, exploitation, fraud indicators) | 90.0 | Equal (1/5) |
| Logic | `L` | Presence of reasoning coherence markers and adequate response length | 75.0 | Equal (1/5) |

### 2.2 Scoring Algorithm

Each dimension starts at a base score and is decremented by a fixed penalty per pattern match:

```
dimension_score = base_score - (penalty * match_count)
dimension_score = clamp(dimension_score, 0.0, 100.0)
composite_score = (S + P + I + E + L) / 5.0
```

**Base scores and penalties:**

| Dimension | Base Score | Penalty per Match | Pattern Source |
|-----------|-----------|-------------------|----------------|
| Safety | 100.0 | -15.0 | `patterns.harmful` |
| Personalization | 80.0 | +4.0 (positive) | `patterns.personal` |
| Integrity | 95.0 | -15.0 | `patterns.dishonest` |
| Ethics | 100.0 | -20.0 | `patterns.unethical` |
| Logic | 85.0 | +3.0 (positive) | `patterns.positive` (reasoning markers) |

### 2.3 Enforcement Actions

| Condition | Action | Code |
|-----------|--------|------|
| Safety < 50 OR Ethics < 50 | `BLOCK` | Critical violation |
| Safety < threshold | `BLOCK` | Safety threshold breach |
| Ethics < threshold | `BLOCK` | Ethics threshold breach |
| Integrity < threshold | `WARN` | Integrity threshold breach |
| Logic < threshold | `WARN` | Logic threshold breach |
| Violations detected, thresholds met | `REVIEW` | Non-critical violations |
| All criteria passed | `ALLOW` | Clean pass |

### 2.4 Fail-Closed Behavior

On any unhandled exception during SPIEL evaluation, the engine returns `BLOCK` with all scores set to 0.0 and a `system_error` violation. This is configurable via `policy_store.json:fail_closed` but defaults to `true`.

---

## 3. THT Protocol Specification

THT (Truth, Honesty, Transparency) is a three-pillar validation protocol applied after SPIEL scoring.

### 3.1 Pillar Definitions

| Pillar | Evaluation Method | Failure Condition |
|--------|-------------------|-------------------|
| Truth | Pattern match against overconfident/absolutist claim patterns | Match found in `false_patterns` list |
| Honesty | Pattern match against secretive/manipulative language | Match found in `dishonest_patterns` list |
| Transparency | For texts > 50 chars containing claim patterns, checks for reasoning markers | Claims present without supporting reasoning |

### 3.2 Compliance Calculation

```
confidence_score = count(verified_pillars) / 3.0
is_compliant = (truth AND honesty AND transparency AND confidence >= 0.8)
```

THT non-compliance does not trigger `BLOCK`. If SPIEL passes but THT fails, the result is downgraded to `WARNING`.

---

## 4. Pattern Configuration

All patterns are stored in `policy_store.json` and loaded at engine initialization. Patterns are matched case-insensitively against the full text of the AI output using substring matching.

### 4.1 Pattern Categories

| Category | Count | Purpose |
|----------|-------|---------|
| `harmful` | 14 | Safety dimension triggers |
| `unethical` | 12 | Ethics dimension triggers |
| `dishonest` | 12 | Integrity dimension / THT honesty triggers |
| `positive` | 12 | Logic and personalization boosters |
| `personal` | 8 | Personalization dimension boosters |

### 4.2 Custom Rules

Custom rules extend the pattern system with domain-specific warnings:

| Rule ID | Domain | Action | Trigger Examples |
|---------|--------|--------|-----------------|
| `medical_advice_warning` | Healthcare | `warn` | "take medicine", "stop medication" |
| `financial_advice_warning` | Finance | `warn` | "invest in", "guaranteed returns" |
| `legal_advice_warning` | Legal | `warn` | "legal advice", "sue", "lawsuit" |

---

## 5. Audit Trail Specification

### 5.1 Audit Entry Structure

Each validation produces an `AuditEntry` containing:

| Field | Type | Description |
|-------|------|-------------|
| `request_id` | UUID v4 | Unique identifier per validation |
| `user_id` | Optional[str] | Caller-supplied user identifier |
| `input_text` | str | Original user input |
| `output_text` | str | AI-generated output before validation |
| `validation_result` | ValidationResult | Full SPIEL/THT result object |
| `context` | Dict | Caller-supplied context metadata |
| `timestamp` | ISO 8601 | UTC timestamp of validation |

### 5.2 Retention Policy

- In-memory buffer: 1000 entries (FIFO eviction)
- Blockchain timestamping: Optional via OriginStamp SHA-256 certification
- Hash chain: Each entry is hashable for integrity verification

---

## 6. API Surface

### 6.1 Core Classes

| Class | Module | Purpose |
|-------|--------|---------|
| `AVRTFirewall` | `middleware.py` | Primary validation entry point |
| `VoiceFirewall` | `middleware.py` | Voice-mode subclass with monitoring |
| `SPIELAnalyzer` | `middleware.py` | SPIEL scoring engine |
| `THTValidator` | `middleware.py` | THT protocol validator |
| `SPIELEngine` | `spiel_engine.py` | Policy-driven SPIEL enforcement |

### 6.2 Primary Method

```python
AVRTFirewall.validate(
    input: str,
    output: str,
    context: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None
) -> ValidationResult
```

### 6.3 Result Structure

```python
ValidationResult:
    status: ValidationStatus  # SAFE | BLOCKED | WARNING | REVIEW_REQUIRED | ERROR
    is_safe: bool
    message: str              # Validated output or safe alternative
    spiel_score: SPIELScore   # Five-dimensional scores + composite
    tht_validation: THTValidation
    violations: List[ViolationType]
    confidence: float         # Composite / 100.0
    processing_time_ms: float
```

---

## 7. Configuration

### 7.1 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `AVRT_LICENSE_KEY` | (none) | License key from Stripe |
| `AVRT_MODE` | `voice-first` | Operating mode |
| `AVRT_ENABLE_THT` | `true` | Enable THT protocol |
| `AVRT_ENABLE_LOGGING` | `true` | Enable logging output |
| `AVRT_API_BASE_URL` | `https://avrt.pro/api` | API base URL |
| `AVRT_CONTEXT_PERSISTENCE` | `true` | Enable context memory |
| `VOICE_LANGUAGE` | `en-US` | Voice recognition language |

### 7.2 Policy Configuration

Policy is loaded from `policy_store.json` at initialization. The policy file controls:

- All SPIEL thresholds
- Pattern lists for all dimensions
- Enforcement actions per violation type
- Rate limits (100/min, 5000/hr, burst 20)
- Custom domain-specific rules
- Fail-closed toggle
- Logging configuration

---

## 8. Security Properties

| Property | Implementation |
|----------|---------------|
| Fail-closed default | On any error, BLOCK is returned |
| No output passthrough on failure | Blocked outputs are replaced with safe alternatives |
| Deterministic evaluation | Same input always produces same SPIEL/THT scores |
| Audit chain integrity | SHA-256 hashing of all validation entries |
| No external dependencies at evaluation time | All pattern matching is local; no network calls during validation |

---

## 9. Performance Characteristics

| Metric | Value |
|--------|-------|
| Validation latency (typical) | < 5ms per call |
| Pattern matching | O(n * p) where n = text length, p = pattern count |
| Memory footprint (audit buffer) | 1000 entries max |
| Thread safety | Not guaranteed; single-threaded operation recommended |

---

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-01-31 | J. Proper | Initial specification |
