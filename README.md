# Cognition Core

Cognition Core is a **local-first cognition lab and runtime control plane** for building, benchmarking, and promoting GGUF-oriented cognition candidates.

Its final runtime doctrine is:
- **no server required**
- **native local execution is authoritative**
- **browser UI is optional**
- **CPU-capable direct binary execution is the target path**
- **llamafile-style final artifacts are supported**

## What is complete in this repo
- A functioning in-process local baseline model (`exemplar`)
- A direct local command adapter for one-shot native execution (`command`)
- Benchmark, scoring, promotion, validation, receipts, and artifact manifests
- Timeout guards for overall runtime, no-generation / first-output timeout, and mid-generation idle timeout
- A binary + GGUF composition step for a llamafile-style final artifact

## What still depends on your chosen upstream model toolchain
- Real SFT / LoRA training against a selected base family
- Real merge implementation for that family
- Real GGUF export implementation for that family
- Running benchmark loops against the actually produced GGUF artifact

## Runtime truth
This project does **not** claim pure browser-native execution for arbitrary large models.
The honest user-facing shape is: browser UI optional, local native binary execution authoritative, no always-on daemon required.

## Quick start
### 1. Validate the repo
```bash
python3 scripts/validate_repo.py
python3 -m pytest tests -q
```

### 2. Build the native functioning baseline
```bash
python3 scripts/training/train_exemplar_candidate.py --candidate darpa_functional
```

### 3. Run the baseline directly
```bash
python3 scripts/execution/run_direct_candidate.py \
  --adapter exemplar \
  --artifact exports/candidates/darpa_functional/exemplar_train/artifact_manifest.json \
  --prompt 'Audit this repo and preserve constraints.'
```

### 4. Benchmark the baseline
```bash
python3 scripts/execution/run_model_benchmarks.py \
  --adapter exemplar \
  --artifact exports/candidates/darpa_functional/exemplar_train/artifact_manifest.json
python3 scripts/execution/score_benchmark_outputs.py
```


## User-end local runtime
### One-shot local prompt
First-run setup copies `.env.direct-runtime.example` to `.env.direct-runtime` for you, so you can edit one local runtime file instead of exporting variables each session.
```bash
scripts/operator/setup_local_user_runtime.sh
scripts/operator/run_local_prompt.sh "Audit this repo and preserve constraints."
```

### One-shot local GGUF model
```bash
export COGNITION_RUNTIME_ADAPTER=exemplar
export COGNITION_MODEL_PATH=/absolute/path/to/model.gguf
export COGNITION_COMMAND_TEMPLATE='/absolute/path/to/llama-cli -m {model} -f {combined_prompt_file}'
scripts/operator/run_local_prompt.sh "Summarize the system and next actions."
```

### Benchmark a local GGUF model
```bash
export COGNITION_RUNTIME_ADAPTER=exemplar
export COGNITION_MODEL_PATH=/absolute/path/to/model.gguf
export COGNITION_COMMAND_TEMPLATE='/absolute/path/to/llama-cli -m {model} -f {combined_prompt_file}'
scripts/operator/benchmark_local_model.sh
```

See also:
- `docs/USER_END_RUNTIME_FLOW_2026-04-14.md`
- `docs/BROWSER_UI_BOUNDARY_2026-04-14.md`
- `.env.direct-runtime.example`

## Direct native runtime examples
### A. Direct `llama-cli` style binary
```bash
python3 scripts/runtime/doctor_direct_runtime.py \
  --adapter command \
  --model /absolute/path/to/model.gguf \
  --command-template '/absolute/path/to/llama-cli -m {model} -f {combined_prompt_file}'
```

### B. Final self-contained `.llamafile` artifact
```bash
python3 scripts/runtime/doctor_direct_runtime.py \
  --adapter command \
  --command-template '/absolute/path/to/model.llamafile -f {combined_prompt_file}'
```

### C. Run a real direct candidate request
```bash
python3 scripts/execution/run_direct_candidate.py \
  --adapter command \
  --model /absolute/path/to/model.gguf \
  --command-template '/absolute/path/to/llama-cli -m {model} -f {combined_prompt_file}' \
  --timeout-seconds 120 \
  --first-output-timeout-seconds 30 \
  --idle-timeout-seconds 20 \
  --prompt 'Produce a bounded repair plan with rollback notes.'
```

## Build a llamafile-style final artifact
```bash
python3 scripts/runtime/compile_llamafile_from_binary.py \
  --runtime-binary /absolute/path/to/llamafile_runtime_binary \
  --gguf /absolute/path/to/model.gguf \
  --output builds/model.llamafile
```

## One-command lab controls
```bash
python3 cognition_lab.py validate
python3 cognition_lab.py train-functioning-model
python3 cognition_lab.py run-functioning-model
python3 cognition_lab.py doctor-runtime
python3 cognition_lab.py candidate-gate
```

## How it works for the user
1. The user downloads the app or opens the browser UI shell.
2. The UI asks for a local model artifact or uses a bundled exemplar baseline.
3. If the user has a GGUF model, Cognition Core invokes a local native binary directly, such as a `llama-cli` path or final `.llamafile`.
4. Prompts are written to temporary prompt files to avoid shell quoting failures.
5. The runtime watches for model loading, tokenization, first real output, stalled generation, and completion or failure.
6. The run emits a receipt with timing, hashes, finish reason, and runtime metadata.
7. The UI displays the result, but the authoritative execution happened locally on the user's machine.

## Supporting ecosystem doctrine
- Cleanroom Runtime: mindshape and bounded execution style
- ARC-Core: proposal, evidence, and authority-gating structure
- Arc-RAR: receipt/archive discipline
- OmniBinary: execution-lane honesty and preflight reasoning
- ARC Language Module: domain-pack and language-boundary reasoning

## Status
This repository is now a **production-shaped local cognition lab/control plane**.
It is **not yet** a fully self-contained foundation-model training stack.


## Quick GGUF / llamafile switchover

When you are ready to move from the bundled baseline to your own local model, use:

```bash
scripts/operator/register_gguf_runtime.sh --gguf /absolute/path/to/model.gguf --binary /absolute/path/to/llama-cli
```

Or for a final self-contained executable:

```bash
scripts/operator/register_gguf_runtime.sh --llamafile /absolute/path/to/model.llamafile
```

Then verify with:

```bash
scripts/operator/runtime_status.sh
scripts/operator/run_local_prompt.sh "hello"
```


## Real flagship GGUF production

This repo is the local runtime/control plane. The actual flagship GGUF still comes from a chosen upstream base-model family and conversion toolchain.

Use the locked handoff path documented in:
- `docs/REAL_GGUF_PRODUCTION_PATH_2026-04-14.md`

Switch to a real artifact with:
```bash
scripts/operator/register_real_gguf_artifact.sh --gguf /absolute/path/model.gguf --binary /absolute/path/llama-cli
```
or
```bash
scripts/operator/register_real_gguf_artifact.sh --llamafile /absolute/path/model.llamafile
```


## Validate the active flagship runtime

After switching from the bundled baseline to your real GGUF or `.llamafile`, run:

```bash
scripts/operator/validate_flagship_runtime.sh
```

This checks the full local path end to end:
- current runtime status
- runtime doctor
- direct prompt smoke
- benchmark smoke

Use this after `register_real_gguf_artifact.sh` or `register_gguf_runtime.sh` to prove the active local artifact really works on the user machine.



## Production GGUF build contract

Copy `configs/production/real_gguf_build.env.example` to `configs/production/real_gguf_build.env`, fill the real upstream toolchain paths, run `scripts/production/validate_real_gguf_build.sh`, then run `scripts/production/build_real_gguf_handoff.sh`. Register the output with `scripts/operator/register_real_gguf_artifact.sh` and prove it with `scripts/operator/validate_flagship_runtime.sh`.


## Final flagship release event

When the real upstream weights and toolchain are present, run:

```bash
scripts/production/release_flagship_event.sh
```

This performs the strict GGUF build preflight, builds the artifact handoff, registers the produced GGUF or `.llamafile`, validates the active runtime, and writes upstream event manifests under `reports/upstream_events/`.
