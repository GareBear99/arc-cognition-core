.PHONY: validate test counts candidate-gate backend-check bundle model-card

validate:
	python3 cognition_lab.py validate

test:
	python3 -m pytest tests -q

counts:
	python3 cognition_lab.py count-data
	python3 cognition_lab.py count-benchmarks

candidate-gate:
	python3 cognition_lab.py candidate-gate

backend-check:
	python3 cognition_lab.py backend-check

bundle:
	python3 scripts/execution/generate_release_bundle.py

model-card:
	python3 scripts/execution/generate_model_card.py --model-name heuristic_minimal_doctrine --adapter heuristic
readiness:
	python scripts/execution/generate_readiness_report.py

smoke-local:
	python scripts/execution/smoke_local_candidate.py


prepare-corpus:
	python scripts/training/prepare_distillation_corpus.py

training-readiness:
	python scripts/execution/run_training_readiness_gate.py

train-candidate-stub:
	python scripts/training/train_lora_candidate.py --candidate qwen3_coder_480b_a35b_instruct

preference-candidate-stub:
	python scripts/training/train_preference_candidate.py --candidate qwen3_coder_480b_a35b_instruct

merge-candidate-stub:
	python scripts/training/merge_adapters_stub.py --candidate qwen3_coder_480b_a35b_instruct

export-gguf-candidate-stub:
	python scripts/training/export_gguf_candidate.py --candidate qwen3_coder_480b_a35b_instruct


distillation-counts:
	python3 scripts/training/report_distillation_counts.py


run-day0:
	bash scripts/operator/run_day0_candidate.sh

run-day1-stub:
	bash scripts/operator/run_day1_shaping_stub.sh

run-day2-stub:
	bash scripts/operator/run_day2_export_stub.sh
