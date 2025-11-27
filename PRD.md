# Product Requirements Document (PRD)
## Project: Round-Trip Translation Turing Machine with LLM Agents
## Authors: Ofri Kutchinsky & Lior Abuhav

---

## 1. Purpose
The purpose of this project is to design and implement a modular, Turing-machine-inspired pipeline composed of multiple stateless translation agents executed via the Claude CLI. The system demonstrates how complex behavior can emerge from minimal, deterministic building blocks that communicate exclusively through files.

This PRD defines the **goals, requirements, constraints, and acceptance criteria** of the system.  
*Implementation details, setup instructions, experiment descriptions, and architectural explanations are intentionally kept out of this PRD because they appear in the README.*

---

## 2. Objectives

### Functional Objectives
- Implement three stateless agents:
  - English → Spanish  
  - Spanish → Hebrew  
  - Hebrew → English  
- Each agent:
  - Runs via Claude CLI  
  - Accepts an input file and produces an output file  
  - Has no memory, context, or side effects  
  - Outputs only the translated text  
- Implement two pipelines:
  - **Single Sentence Pipeline**: round-trip translation + distance measurement  
  - **Batch Experiment**: evaluate semantic drift for typo levels 0–50%  
- Use Python **only** for embeddings, distance computation, and plotting.

### Non‑Functional Objectives
- Deterministic behavior (same inputs → same outputs).
- Minimal agent logic.
- Fully reproducible results.
- Clear project structure.

---

## 3. Scope

### In Scope
- File-based communication between agents  
- Bash scripting for orchestration  
- Claude CLI translation execution  
- Embedding-based evaluation  
- Experiment with multiple typo levels  
- Plot and CSV generation

### Out of Scope
- UI or web server  
- Python-based translation  
- Parallel or distributed execution  
- Advanced embeddings or external ML models

---

## 4. System Overview
The system functions like a simplified Turing Machine:

```
Input File → Agent 1 → Agent 2 → Agent 3 → Output File
```

- Each agent performs exactly one operation.
- Pipelines (`run_single.sh` and `run_batch.sh`) orchestrate execution.
- Python post-processing computes semantic drift.
- Files act as the “tape” passed from step to step.

(See README for detailed architecture explanation, diagrams, and examples.)

---

## 5. User Stories
- As a user, I can provide one English sentence and get its round-trip translated version plus a distance score.
- As a researcher, I can run the experiment on predefined typo levels and examine results.
- As an evaluator, I can reproduce all results using the commands provided in the README.

---

## 6. Functional Requirements

### FR1 – Agents
- FR1.1: Each agent must take two file paths (input, output).  
- FR1.2: Agents must use the Claude CLI in non-interactive `--print` mode.  
- FR1.3: Prompts must enforce deterministic translation without explanations.

### FR2 – Single Sentence Pipeline
- FR2.1: Save the input sentence to a file.  
- FR2.2: Sequentially execute EN→ES→HE→EN.  
- FR2.3: Output the final English sentence.  
- FR2.4: Compute cosine distance in Python.

### FR3 – Batch Experiment
- FR3.1: Load typo-level input files from `data/`.  
- FR3.2: Run all through the pipeline to generate back-translated outputs.  
- FR3.3: Compute distances and save a CSV.  
- FR3.4: Generate plot (`typos_vs_distance.png`).

---

## 7. Non‑Functional Requirements
- NFR1: Determinism under identical inputs.  
- NFR2: Simplicity and clarity of code.  
- NFR3: All experiment outputs stored under `experiments/`.  
- NFR4: Project must run using only instructions in the README.

---

## 8. Risks & Mitigation

| Risk | Mitigation |
|------|-----------|
| Claude CLI rate limits | Use `haiku`, add small sleeps if needed |
| Unexpected meta‑responses | Use strict prompts and `--print` |
| Missing input files | Provide fallback warnings in pipeline |
| Reproducibility issues | Fix model version and deterministic prompts |

---

## 9. Acceptance Criteria

- ✔ Three agents exist and perform correct translations.  
- ✔ Running `./run_single.sh` prints original + final English + distance.  
- ✔ Running `./run_batch.sh` produces translation outputs for each typo level.  
- ✔ Running `python embeddings/run_experiment.py` creates CSV + PNG.  
- ✔ README enables any user to reproduce full experiment.  
- ✔ No Python translation code exists; agents are shell + CLI only.

---

This PRD defines **what** the system must achieve.  
The README explains **how** to install, run, and understand it.  
Together, they provide a complete documentation set for the project.
