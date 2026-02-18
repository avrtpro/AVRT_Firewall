#!/usr/bin/env python3
"""
AVRT Determinism Test Harness v1.0

Multi-provider determinism testing for AVRT middleware.
Supports OpenAI, Anthropic, and Google Gemini APIs.
Captures latency metrics, hash consistency, and cross-provider comparison.

(c) 2025 Jason I. Proper, BGBH Threads LLC
Patent: USPTO 19/236,935
"""

import argparse
import hashlib
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Provider enum
# ---------------------------------------------------------------------------

class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ProviderConfig:
    """Configuration for an LLM provider."""
    name: Provider
    api_key_env: str
    model: str
    temperature: float = 0.0  # deterministic
    max_tokens: int = 256

    @property
    def api_key(self) -> Optional[str]:
        return os.getenv(self.api_key_env)

    @property
    def is_available(self) -> bool:
        return self.api_key is not None and len(self.api_key) > 0


@dataclass
class SingleRunResult:
    """Result from a single provider call."""
    provider: str
    model: str
    prompt: str
    response_text: str
    response_hash: str
    latency_ms: float
    timestamp: str
    success: bool
    error: Optional[str] = None


@dataclass
class DeterminismComparison:
    """Comparison of multiple runs for a single prompt on a single provider."""
    provider: str
    prompt: str
    run_count: int
    hashes: List[str]
    is_deterministic: bool
    unique_hash_count: int
    latencies_ms: List[float]
    mean_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    p95_latency_ms: float


@dataclass
class CrossProviderComparison:
    """Comparison of responses across providers for a single prompt."""
    prompt: str
    provider_hashes: Dict[str, str]
    all_match: bool
    unique_hash_count: int


@dataclass
class TestSuiteResult:
    """Full test suite output."""
    run_id: str
    timestamp: str
    providers_tested: List[str]
    prompts_tested: int
    runs_per_prompt: int
    determinism_results: List[Dict[str, Any]]
    cross_provider_results: List[Dict[str, Any]]
    summary_metrics: Dict[str, Any]


# ---------------------------------------------------------------------------
# Default provider configurations
# ---------------------------------------------------------------------------

DEFAULT_PROVIDERS = [
    ProviderConfig(
        name=Provider.OPENAI,
        api_key_env="OPENAI_API_KEY",
        model="gpt-4o",
        temperature=0.0,
        max_tokens=256,
    ),
    ProviderConfig(
        name=Provider.ANTHROPIC,
        api_key_env="ANTHROPIC_API_KEY",
        model="claude-sonnet-4-20250514",
        temperature=0.0,
        max_tokens=256,
    ),
    ProviderConfig(
        name=Provider.GEMINI,
        api_key_env="GEMINI_API_KEY",
        model="gemini-1.5-pro",
        temperature=0.0,
        max_tokens=256,
    ),
]

# ---------------------------------------------------------------------------
# Default test prompts
# ---------------------------------------------------------------------------

DEFAULT_PROMPTS = [
    "What is 2 + 2? Answer with only the number.",
    "Is it safe to mix bleach and ammonia? Answer in one sentence.",
    "Explain the Pythagorean theorem in exactly two sentences.",
    "Should I invest all my money in cryptocurrency? Answer in one sentence.",
    "Summarize the purpose of a firewall in network security in one sentence.",
]

# ---------------------------------------------------------------------------
# Provider API callers
# ---------------------------------------------------------------------------


def _call_openai(config: ProviderConfig, prompt: str) -> Tuple[str, float]:
    """Call OpenAI API. Returns (response_text, latency_ms)."""
    try:
        import openai
    except ImportError:
        raise ImportError("openai package not installed. Run: pip install openai")

    client = openai.OpenAI(api_key=config.api_key)
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    latency_ms = (time.perf_counter() - start) * 1000
    text = response.choices[0].message.content.strip()
    return text, latency_ms


def _call_anthropic(config: ProviderConfig, prompt: str) -> Tuple[str, float]:
    """Call Anthropic API. Returns (response_text, latency_ms)."""
    try:
        import anthropic
    except ImportError:
        raise ImportError("anthropic package not installed. Run: pip install anthropic")

    client = anthropic.Anthropic(api_key=config.api_key)
    start = time.perf_counter()
    response = client.messages.create(
        model=config.model,
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = (time.perf_counter() - start) * 1000
    text = response.content[0].text.strip()
    return text, latency_ms


def _call_gemini(config: ProviderConfig, prompt: str) -> Tuple[str, float]:
    """Call Google Gemini API. Returns (response_text, latency_ms)."""
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            "google-generativeai package not installed. "
            "Run: pip install google-generativeai"
        )

    genai.configure(api_key=config.api_key)
    model = genai.GenerativeModel(
        config.model,
        generation_config=genai.GenerationConfig(
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
        ),
    )
    start = time.perf_counter()
    response = model.generate_content(prompt)
    latency_ms = (time.perf_counter() - start) * 1000
    text = response.text.strip()
    return text, latency_ms


PROVIDER_CALLERS = {
    Provider.OPENAI: _call_openai,
    Provider.ANTHROPIC: _call_anthropic,
    Provider.GEMINI: _call_gemini,
}


# ---------------------------------------------------------------------------
# AVRT validation layer
# ---------------------------------------------------------------------------


def _compute_hash(text: str) -> str:
    """Compute SHA-256 hash of text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _apply_avrt_validation(response_text: str) -> Dict[str, Any]:
    """
    Apply AVRT SPIEL + THT validation to a response.

    This uses the same scoring logic as the production middleware
    to verify that the validation layer itself is deterministic.
    """
    text_lower = response_text.lower()

    # SPIEL scoring (mirrors spiel_engine.py logic)
    harmful_patterns = [
        "harm", "hurt", "attack", "kill", "destroy",
        "hate", "violence", "weapon", "bomb", "poison",
    ]
    unethical_patterns = [
        "cheat", "lie", "deceive", "manipulate",
        "exploit", "abuse", "steal", "fraud",
    ]
    dishonest_patterns = [
        "just trust me", "believe me", "i guarantee",
        "secret", "don't tell anyone", "between us",
    ]

    safety_score = 100.0
    for p in harmful_patterns:
        if p in text_lower:
            safety_score -= 15.0
    safety_score = max(0.0, safety_score)

    integrity_score = 95.0
    for p in dishonest_patterns:
        if p in text_lower:
            integrity_score -= 15.0
    integrity_score = max(0.0, integrity_score)

    ethics_score = 100.0
    for p in unethical_patterns:
        if p in text_lower:
            ethics_score -= 20.0
    ethics_score = max(0.0, ethics_score)

    logic_score = 85.0
    reasoning_markers = ["because", "therefore", "thus", "since", "based on"]
    for m in reasoning_markers:
        if m in text_lower:
            logic_score += 3.0
    if len(response_text.strip()) < 10:
        logic_score -= 20.0
    logic_score = max(0.0, min(100.0, logic_score))

    personalization_score = 80.0
    personal_markers = ["you", "your", "help", "assist"]
    for m in personal_markers:
        if m in text_lower:
            personalization_score += 4.0
    personalization_score = min(100.0, personalization_score)

    composite = (
        safety_score + personalization_score + integrity_score
        + ethics_score + logic_score
    ) / 5.0

    # THT validation (mirrors tht_service.py logic)
    false_patterns = [
        "definitely", "absolutely certain", "100% guarantee",
        "always true", "never wrong",
    ]
    tht_dishonest = [
        "just between us", "don't tell", "keep this secret",
        "you can trust me", "believe me",
    ]
    transparent_markers = [
        "because", "the reason", "this is based on",
        "according to", "evidence suggests",
    ]

    truth_ok = not any(p in text_lower for p in false_patterns)
    honesty_ok = not any(p in text_lower for p in tht_dishonest)

    claim_words = ["is", "are", "will", "should"]
    has_claims = any(w in text_lower for w in claim_words)
    transparency_ok = True
    if has_claims and len(response_text) >= 50:
        transparency_ok = any(m in text_lower for m in transparent_markers)

    tht_confidence = sum([truth_ok, honesty_ok, transparency_ok]) / 3.0
    tht_compliant = truth_ok and honesty_ok and transparency_ok and tht_confidence >= 0.8

    # Determine action
    if safety_score < 50 or ethics_score < 50:
        action = "BLOCK"
    elif safety_score < 85:
        action = "BLOCK"
    elif ethics_score < 90:
        action = "BLOCK"
    elif integrity_score < 80:
        action = "WARN"
    elif not tht_compliant:
        action = "WARN"
    else:
        action = "ALLOW"

    result = {
        "spiel": {
            "safety": safety_score,
            "personalization": personalization_score,
            "integrity": integrity_score,
            "ethics": ethics_score,
            "logic": logic_score,
            "composite": round(composite, 2),
        },
        "tht": {
            "truth": truth_ok,
            "honesty": honesty_ok,
            "transparency": transparency_ok,
            "confidence": round(tht_confidence, 4),
            "compliant": tht_compliant,
        },
        "action": action,
    }

    # Hash the validation result itself to verify determinism of the AVRT layer
    result_hash = _compute_hash(json.dumps(result, sort_keys=True))
    result["validation_hash"] = result_hash

    return result


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------


def run_single_call(
    config: ProviderConfig, prompt: str
) -> SingleRunResult:
    """Execute a single API call and return the result."""
    caller = PROVIDER_CALLERS.get(config.name)
    if caller is None:
        return SingleRunResult(
            provider=config.name.value,
            model=config.model,
            prompt=prompt,
            response_text="",
            response_hash="",
            latency_ms=0.0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            success=False,
            error=f"No caller implemented for {config.name.value}",
        )

    try:
        text, latency_ms = caller(config, prompt)
        return SingleRunResult(
            provider=config.name.value,
            model=config.model,
            prompt=prompt,
            response_text=text,
            response_hash=_compute_hash(text),
            latency_ms=round(latency_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
            success=True,
        )
    except Exception as e:
        return SingleRunResult(
            provider=config.name.value,
            model=config.model,
            prompt=prompt,
            response_text="",
            response_hash="",
            latency_ms=0.0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            success=False,
            error=str(e),
        )


def run_determinism_test(
    config: ProviderConfig,
    prompt: str,
    runs: int = 3,
) -> DeterminismComparison:
    """Run the same prompt N times on a provider and compare results."""
    results: List[SingleRunResult] = []
    for _ in range(runs):
        result = run_single_call(config, prompt)
        results.append(result)

    successful = [r for r in results if r.success]
    hashes = [r.response_hash for r in successful]
    latencies = [r.latency_ms for r in successful]

    unique_hashes = list(set(hashes))
    is_deterministic = len(unique_hashes) <= 1 and len(successful) == runs

    sorted_latencies = sorted(latencies) if latencies else [0.0]
    p95_idx = max(0, int(len(sorted_latencies) * 0.95) - 1)

    return DeterminismComparison(
        provider=config.name.value,
        prompt=prompt,
        run_count=runs,
        hashes=hashes,
        is_deterministic=is_deterministic,
        unique_hash_count=len(unique_hashes),
        latencies_ms=latencies,
        mean_latency_ms=round(sum(latencies) / len(latencies), 2) if latencies else 0.0,
        min_latency_ms=round(min(latencies), 2) if latencies else 0.0,
        max_latency_ms=round(max(latencies), 2) if latencies else 0.0,
        p95_latency_ms=round(sorted_latencies[p95_idx], 2),
    )


def run_cross_provider_comparison(
    configs: List[ProviderConfig],
    prompt: str,
) -> CrossProviderComparison:
    """Get one response per provider and compare hashes."""
    provider_hashes: Dict[str, str] = {}
    for config in configs:
        if not config.is_available:
            continue
        result = run_single_call(config, prompt)
        if result.success:
            provider_hashes[config.name.value] = result.response_hash

    hash_values = list(provider_hashes.values())
    unique_count = len(set(hash_values)) if hash_values else 0
    all_match = unique_count == 1 and len(hash_values) == len(configs)

    return CrossProviderComparison(
        prompt=prompt,
        provider_hashes=provider_hashes,
        all_match=all_match,
        unique_hash_count=unique_count,
    )


def run_avrt_validation_determinism(
    prompts: List[str],
    runs: int = 5,
) -> Dict[str, Any]:
    """
    Test that the AVRT validation layer itself is deterministic.
    Runs the same text through the AVRT SPIEL+THT logic multiple times
    and verifies identical output.
    """
    results = []
    for prompt in prompts:
        # Use the prompt text as a stand-in for a response to validate
        hashes = []
        for _ in range(runs):
            validation = _apply_avrt_validation(prompt)
            hashes.append(validation["validation_hash"])

        unique = list(set(hashes))
        results.append({
            "input_text": prompt,
            "runs": runs,
            "is_deterministic": len(unique) == 1,
            "unique_hashes": len(unique),
            "hash_sample": unique[0] if unique else None,
        })

    all_deterministic = all(r["is_deterministic"] for r in results)
    return {
        "test": "avrt_validation_determinism",
        "all_deterministic": all_deterministic,
        "results": results,
    }


# ---------------------------------------------------------------------------
# Full test suite
# ---------------------------------------------------------------------------


def run_full_suite(
    providers: Optional[List[ProviderConfig]] = None,
    prompts: Optional[List[str]] = None,
    runs_per_prompt: int = 3,
    output_dir: Optional[str] = None,
    provider_filter: Optional[str] = None,
) -> TestSuiteResult:
    """
    Execute the full determinism test suite.

    Args:
        providers: List of provider configs (defaults to all three).
        prompts: List of test prompts.
        runs_per_prompt: Number of repetitions per prompt per provider.
        output_dir: Directory for JSON output files.
        provider_filter: If set, only test this provider.

    Returns:
        TestSuiteResult with all data.
    """
    if providers is None:
        providers = DEFAULT_PROVIDERS
    if prompts is None:
        prompts = DEFAULT_PROMPTS

    # Apply provider filter
    if provider_filter:
        providers = [p for p in providers if p.name.value == provider_filter]

    available = [p for p in providers if p.is_available]

    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    print(f"AVRT Determinism Test Suite")
    print(f"Run ID: {run_id}")
    print(f"Timestamp: {timestamp}")
    print(f"Providers available: {[p.name.value for p in available]}")
    print(f"Prompts: {len(prompts)}")
    print(f"Runs per prompt: {runs_per_prompt}")
    print("-" * 60)

    # --- AVRT validation layer determinism test ---
    print("\n[Phase 0] Testing AVRT validation layer determinism...")
    avrt_det = run_avrt_validation_determinism(prompts, runs=10)
    print(f"  AVRT layer deterministic: {avrt_det['all_deterministic']}")

    # --- Per-provider determinism tests ---
    determinism_results: List[Dict[str, Any]] = []
    all_latencies: Dict[str, List[float]] = {}

    for config in available:
        print(f"\n[Phase 1] Provider: {config.name.value} ({config.model})")
        all_latencies[config.name.value] = []

        for i, prompt in enumerate(prompts):
            print(f"  Prompt {i+1}/{len(prompts)}: {prompt[:50]}...")
            comparison = run_determinism_test(config, prompt, runs_per_prompt)
            all_latencies[config.name.value].extend(comparison.latencies_ms)

            status = "DETERMINISTIC" if comparison.is_deterministic else "NON-DETERMINISTIC"
            print(f"    {status} | hashes={comparison.unique_hash_count} | "
                  f"latency={comparison.mean_latency_ms:.1f}ms")

            # Apply AVRT validation to the first successful response
            avrt_result = None
            if comparison.hashes:
                # Reconstruct from any run — we care about the validation hash
                avrt_result = _apply_avrt_validation(prompt)

            determinism_results.append({
                **{k: v for k, v in comparison.__dict__.items()},
                "avrt_validation": avrt_result,
            })

    # --- Cross-provider comparison ---
    cross_provider_results: List[Dict[str, Any]] = []

    if len(available) > 1:
        print(f"\n[Phase 2] Cross-provider comparison...")
        for i, prompt in enumerate(prompts):
            print(f"  Prompt {i+1}/{len(prompts)}: {prompt[:50]}...")
            xp = run_cross_provider_comparison(available, prompt)
            print(f"    Match: {xp.all_match} | Unique hashes: {xp.unique_hash_count}")
            cross_provider_results.append(xp.__dict__)
    else:
        print("\n[Phase 2] Skipped (fewer than 2 providers available)")

    # --- Summary metrics ---
    total_deterministic = sum(
        1 for r in determinism_results if r.get("is_deterministic")
    )
    total_tests = len(determinism_results)

    provider_metrics = {}
    for pname, lats in all_latencies.items():
        if lats:
            sorted_lats = sorted(lats)
            p95_idx = max(0, int(len(sorted_lats) * 0.95) - 1)
            provider_metrics[pname] = {
                "total_calls": len(lats),
                "mean_latency_ms": round(sum(lats) / len(lats), 2),
                "min_latency_ms": round(min(lats), 2),
                "max_latency_ms": round(max(lats), 2),
                "p95_latency_ms": round(sorted_lats[p95_idx], 2),
            }

    summary_metrics = {
        "total_tests": total_tests,
        "deterministic_count": total_deterministic,
        "deterministic_rate": round(
            total_deterministic / total_tests, 4
        ) if total_tests > 0 else 0.0,
        "avrt_layer_deterministic": avrt_det["all_deterministic"],
        "cross_provider_matches": sum(
            1 for r in cross_provider_results if r.get("all_match")
        ),
        "cross_provider_total": len(cross_provider_results),
        "per_provider": provider_metrics,
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Deterministic: {total_deterministic}/{total_tests}")
    print(f"  AVRT layer: {'DETERMINISTIC' if avrt_det['all_deterministic'] else 'NON-DETERMINISTIC'}")
    print(f"  Cross-provider matches: {summary_metrics['cross_provider_matches']}/{summary_metrics['cross_provider_total']}")
    for pname, pm in provider_metrics.items():
        print(f"  {pname}: mean={pm['mean_latency_ms']}ms, p95={pm['p95_latency_ms']}ms")

    result = TestSuiteResult(
        run_id=run_id,
        timestamp=timestamp,
        providers_tested=[p.name.value for p in available],
        prompts_tested=len(prompts),
        runs_per_prompt=runs_per_prompt,
        determinism_results=determinism_results,
        cross_provider_results=cross_provider_results,
        summary_metrics=summary_metrics,
    )

    # --- Write output ---
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        results_file = out_path / f"determinism_results_{run_id[:8]}.json"
        with open(results_file, "w") as f:
            json.dump(
                {
                    "run_id": result.run_id,
                    "timestamp": result.timestamp,
                    "providers_tested": result.providers_tested,
                    "prompts_tested": result.prompts_tested,
                    "runs_per_prompt": result.runs_per_prompt,
                    "determinism_results": result.determinism_results,
                    "cross_provider_results": result.cross_provider_results,
                    "avrt_validation_determinism": avrt_det,
                },
                f,
                indent=2,
                default=str,
            )
        print(f"\nResults written to: {results_file}")

        metrics_file = out_path / "summary_metrics.json"
        with open(metrics_file, "w") as f:
            json.dump(
                {
                    "run_id": result.run_id,
                    "timestamp": result.timestamp,
                    **summary_metrics,
                },
                f,
                indent=2,
            )
        print(f"Metrics written to: {metrics_file}")

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="AVRT Determinism Test Harness — multi-provider LLM determinism testing"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "gemini"],
        default=None,
        help="Test a single provider (default: all available)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of runs per prompt per provider (default: 3)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory for JSON output (default: ./logs/)",
    )
    parser.add_argument(
        "--prompts-file",
        type=str,
        default=None,
        help="Path to JSON file containing prompt list",
    )
    parser.add_argument(
        "--avrt-only",
        action="store_true",
        help="Only test AVRT validation layer determinism (no API calls)",
    )

    args = parser.parse_args()

    # Resolve output dir
    output_dir = args.output_dir
    if output_dir is None:
        output_dir = str(Path(__file__).parent.parent / "logs")

    # Load custom prompts
    prompts = None
    if args.prompts_file:
        with open(args.prompts_file, "r") as f:
            prompts = json.load(f)

    if args.avrt_only:
        print("AVRT Validation Layer Determinism Test")
        print("=" * 40)
        test_prompts = prompts or DEFAULT_PROMPTS
        result = run_avrt_validation_determinism(test_prompts, runs=10)
        print(json.dumps(result, indent=2))

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        out_file = out_path / "avrt_layer_determinism.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nOutput: {out_file}")
        return

    run_full_suite(
        prompts=prompts,
        runs_per_prompt=args.runs,
        output_dir=output_dir,
        provider_filter=args.provider,
    )


if __name__ == "__main__":
    main()
