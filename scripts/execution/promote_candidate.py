from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scored", default="results/scored_outputs.json")
    parser.add_argument("--scoreboard", default="results/scoreboard.json")
    parser.add_argument("--model-name", default="heuristic_minimal_doctrine")
    parser.add_argument("--report", default="reports/promotion_decision.json")
    args = parser.parse_args()

    scored = json.loads(Path(args.scored).read_text(encoding="utf-8"))
    scoreboard_path = Path(args.scoreboard)
    scoreboard = json.loads(scoreboard_path.read_text(encoding="utf-8")) if scoreboard_path.exists() else {"models": []}
    summary = scored.get("summary", {})
    results = scored.get('results', [])
    sample = results[0] if results else {}
    entry = {
        "candidate_id": f"cand_{uuid4().hex[:10]}",
        "run_id": sample.get('run_id'),
        "model": args.model_name,
        "adapter": sample.get('adapter'),
        "backend_identity": sample.get('backend_identity'),
        "prompt_profile": sample.get('prompt_profile'),
        "benchmark_version": "seed_tasks_v1",
        "scorer_version": scored.get('scorer_version', 'unknown'),
        "reasoning_accuracy": summary.get("reasoning", 0.0),
        "planning_quality": summary.get("planning", 0.0),
        "critique_usefulness": summary.get("critique", 0.0),
        "repair_success": summary.get("repair", 0.0),
        "compression_retention": summary.get("compression", 0.0),
        "calibration_error": round(1.0 - summary.get("calibration", 0.0), 4),
        "paraphrase_stability": summary.get("paraphrase_stability", 0.0),
        "overall_weighted_score": scored.get("overall_weighted_score", 0.0),
        "failure_rate": round(scored.get('failure_count', 0) / max(1, len(results)), 4),
        "latency_summary_ms": {
            "avg": round(sum(r.get('latency_ms', 0.0) for r in results) / max(1, len(results)), 2) if results else 0.0,
            "max": max((r.get('latency_ms', 0.0) for r in results), default=0.0),
        },
        "artifacts": {"scored_outputs": args.scored, "promotion_report": args.report},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "incumbent": False,
    }

    incumbent = max(scoreboard.get("models", []), key=lambda m: m.get("overall_weighted_score", 0.0), default=None)
    promoted = False
    decision_reason = "No incumbent present; candidate accepted as current best baseline."
    if incumbent is None:
        promoted = True
    else:
        better = entry["overall_weighted_score"] > incumbent.get("overall_weighted_score", 0.0)
        no_bad_repair_drop = entry["repair_success"] >= incumbent.get("repair_success", 0.0) - 0.04
        no_bad_calibration_regression = entry["calibration_error"] <= incumbent.get("calibration_error", 1.0) + 0.03
        no_failure_regression = entry['failure_rate'] <= incumbent.get('failure_rate', 1.0)
        promoted = better and no_bad_repair_drop and no_bad_calibration_regression and no_failure_regression
        if promoted:
            decision_reason = "Candidate improved weighted score without unacceptable repair/calibration/failure regression."
        else:
            decision_reason = "Candidate did not clear promotion gate against incumbent."

    deduped = [m for m in scoreboard.get('models', []) if m.get('run_id') != entry.get('run_id')]
    for model in deduped:
        model['incumbent'] = False
    entry['incumbent'] = promoted or not deduped
    deduped.append(entry)
    scoreboard['models'] = deduped
    scoreboard_path.write_text(json.dumps(scoreboard, indent=2), encoding="utf-8")

    report = {
        "ok": True,
        "candidate": entry,
        "incumbent_before": incumbent,
        "promoted": promoted,
        "decision_reason": decision_reason,
    }
    Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "promoted": promoted, "report": args.report, "overall_weighted_score": entry["overall_weighted_score"]}, indent=2))


if __name__ == "__main__":
    main()
