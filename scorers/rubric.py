from __future__ import annotations

from typing import Any


def _contains_any(text: str, options: list[str]) -> bool:
    lowered = text.lower()
    return any(option in lowered for option in options)


def _score_parts(text: str, checks: list[tuple[str, bool]]) -> tuple[int, list[str]]:
    passed = [name for name, ok in checks if ok]
    return len(passed), passed


def score_record(output_text: str, task: dict | None = None) -> dict[str, Any]:
    text = (output_text or "").strip()
    lowered = text.lower()
    capability = (task or {}).get("capability", "generic")
    reference = (task or {}).get("reference", {}).get("rubric", {})
    notes: list[str] = []

    if not text:
        return {"raw_score": 0, "normalized_score": 0.0, "capability": capability, "notes": "Empty output", "matched_checks": []}

    common_checks = [
        ("mentions_constraints", _contains_any(lowered, ["constraint", "preserve", "boundary", "interface"])),
        ("mentions_risk_or_tradeoff", _contains_any(lowered, ["risk", "tradeoff", "regression", "failure mode"])),
        ("mentions_validation_or_evidence", _contains_any(lowered, ["validate", "test", "evidence", "verify", "observability"])),
    ]

    capability_checks: dict[str, list[tuple[str, bool]]] = {
        "planning": [
            ("has_ordered_plan", _contains_any(lowered, ["plan", "steps", "first", "then"])),
            ("prefers_narrow_change", _contains_any(lowered, ["smallest", "minimal", "targeted", "narrow"])),
            ("preserves_interfaces", _contains_any(lowered, ["preserve interfaces", "public api", "boundary", "without breaking"])),
        ],
        "reasoning": [
            ("separates_fact_from_inference", _contains_any(lowered, ["fact", "inference", "given", "unknown"])),
            ("rejects_or_bounds_unsafe_change", _contains_any(lowered, ["reject", "not acceptable", "only if", "conditionally"])),
            ("mentions_conflict", _contains_any(lowered, ["conflict", "contradiction", "tradeoff", "threatens"])),
        ],
        "critique": [
            ("identifies_missing_evidence", _contains_any(lowered, ["missing evidence", "not shown", "unverified", "assumption"])),
            ("identifies_scope_risk", _contains_any(lowered, ["too broad", "scope", "blast radius", "regression"])),
            ("proposes_followup_check", _contains_any(lowered, ["validate", "test", "verify", "instrument"])),
        ],
        "repair": [
            ("offers_specific_fix", _contains_any(lowered, ["patch", "fix", "change", "guard", "rollback"])),
            ("keeps_fix_small", _contains_any(lowered, ["minimal", "targeted", "surgical", "narrow"])),
            ("adds_regression_protection", _contains_any(lowered, ["test", "regression", "validate", "assert"])),
        ],
        "compression": [
            ("preserves_goal", _contains_any(lowered, ["goal", "objective", "task"])),
            ("preserves_blockers", _contains_any(lowered, ["blocker", "risk", "constraint"])),
            ("preserves_next_action", _contains_any(lowered, ["next", "action", "do this", "follow-up"])),
        ],
        "calibration": [
            ("states_uncertainty", _contains_any(lowered, ["likely", "uncertain", "confidence", "may", "bounded"])),
            ("avoids_false_certainty", not _contains_any(lowered, ["definitely", "certainly", "guaranteed"])),
            ("ties_claims_to_evidence", _contains_any(lowered, ["evidence", "based on", "from the prompt", "given only"])),
        ],
        "paraphrase_stability": [
            ("preserves_meaning", _contains_any(lowered, ["same meaning", "preserve", "equivalent", "without changing"])),
            ("mentions_constraints", _contains_any(lowered, ["constraint", "key point", "do not lose"])),
            ("avoids_additional_claims", not _contains_any(lowered, ["new requirement", "extra guarantee", "additional promise"])),
        ],
        "quantization_retention": [
            ("mentions_core_behavior", _contains_any(lowered, ["retain", "preserve", "behavior", "quality"])),
            ("compares_variants", _contains_any(lowered, ["full precision", "quantized", "gguf", "variant"])),
            ("mentions_regression_threshold", _contains_any(lowered, ["threshold", "regression", "drop", "retention"])),
        ],
    }

    checks = common_checks + capability_checks.get(capability, [])
    raw_score, matched = _score_parts(lowered, checks)
    normalized = round(raw_score / max(1, len(checks)), 4)
    if reference:
        notes.append(f"Scored against capability={capability} with {len(reference)} rubric fields.")
    notes.append(f"Matched {raw_score} of {len(checks)} checks.")
    return {"raw_score": raw_score, "normalized_score": normalized, "capability": capability, "notes": " ".join(notes), "matched_checks": matched}


def score_text(text: str) -> dict[str, Any]:
    return score_record(text, task=None)
