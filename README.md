# Cognition Core

Production-hardened alpha cognition lab for building, benchmarking, shaping, and promoting **GGUF-oriented local AI cognition candidates**.

This repository is designed around **planning, critique, repair, calibration, benchmark-driven promotion, and distillation** from Cleanroom Runtime, ARC-Core, Arc-RAR, and OmniBinary v2.2.

## Core goals
- Native planning
- Native self-critique
- Native repair
- Calibrated uncertainty
- Compression that preserves constraints
- Strong retention after GGUF export

## Frontier target
The target is a Claude-like / Maverick-class local cognition family.

This project does not treat GGUF as the source of intelligence.
It treats GGUF as the deployable result of a promoted cognition checkpoint.

## Directory layout
- `specs/` doctrine, contract, benchmarks, promotion rules, schemas
- `configs/` model and training configs
- `data/` cognition datasets
- `benchmarks/` benchmark task suites
- `datasets/` source buckets and dataset policy planning
- `evals/` evaluation-only or mostly-evaluation suites
- `scripts/` dataset, training, eval, and export utilities
- `results/` scoreboards and reports
- `exports/` promoted GGUF variants

## Core doctrine
The model should natively:
- observe
- infer
- plan
- critique
- repair
- compress
- calibrate

## Hard gates
A candidate fails if:
- it only performs well under a giant system prompt
- it regresses in self-critique or repair
- it becomes more overconfident
- it loses too much cognition quality after quantization


## Quick start

```bash
python3 scripts/validate_repo.py
python3 scripts/build_dataset.py
python3 scripts/run_benchmarks.py
python3 scripts/build_repo_capsule.py . --output examples/capsules/self_capsule.json
```

## Current package status
This repository is a **starter program** for a cognition-core project.
It includes doctrine, schemas, starter datasets, starter benchmarks, validation, and local repo-capsule generation.
It does **not** include a trained frontier checkpoint yet.


## Execution-first loop

```bash
python3 scripts/execution/run_model_benchmarks.py --adapter heuristic
python3 scripts/execution/score_benchmark_outputs.py
python3 scripts/execution/promote_candidate.py --model-name heuristic_minimal_doctrine
python3 scripts/execution/run_quantization_retention.py
```

## MCP and attachment tooling

This package also includes a bounded MCP-style tool registry and an adapter-ready integration path for AI Screenshot Attachment.


## One-command lab controls

```bash
python3 cognition_lab.py validate
python3 cognition_lab.py count-data
python3 cognition_lab.py count-benchmarks
python3 cognition_lab.py backend-check
python3 cognition_lab.py candidate-gate
```

## Test layer

```bash
python3 -m pytest tests -q
```


## Release hygiene

```bash
python3 scripts/execution/generate_release_bundle.py
python3 scripts/execution/generate_model_card.py --model-name heuristic_minimal_doctrine --adapter heuristic
```

## Production-readiness boundary
This repository can be hardened as a **production-ready lab scaffold**.
It is **not** a production-ready frontier cognition model until a real model backend, training pipeline, larger corpora, and real GGUF retention comparisons are in place.

## Merged source doctrine
- Cleanroom Runtime: mind shape
- ARC-Core: structured reasoning ontology
- Arc-RAR: receipt/archive discipline
- OmniBinary v2.2: execution-lane and preflight reasoning


## GitHub launch metadata
- Suggested repository description: `Production-hardened alpha cognition lab for building, benchmarking, shaping, and promoting GGUF-oriented local AI cognition candidates.`
- Suggested topics: see `repo-metadata/repository_topics.txt`
- Suggested first release notes: see `repo-metadata/RELEASE_DRAFT_v0.3.0-alpha.md`
- Suggested repo metadata file: `repo-metadata/repository_metadata.json`
