# Round-Trip Translation Pipeline Using LLM Agents  
### *Turing-machine-style pipeline with Claude CLI + Python embeddings*

## 1. Overview

This project implements a simple *Turing-machine-style* pipeline composed of **three stateless translation agents**, each implemented as a standalone shell script using the **Claude CLI**.

The three agents perform:

1. **English → Spanish**  
2. **Spanish → Hebrew**  
3. **Hebrew → English**

The agents communicate **only through files**, simulating how a Turing Machine passes information along a tape.

Two main tasks are implemented:

### **Part 1 — Single-sentence pipeline**

Given any English sentence (with typos), the pipeline:

1. Saves the sentence to `data/single_input.txt`  
2. Runs it through EN→ES→HE→EN  
3. Outputs the final back-translated English sentence  
4. Uses Python **only** to compute the cosine distance between original and final embeddings  

### **Part 2 — Experiment: Typo percentage vs semantic drift**

We prepare several fixed English inputs with increasing typo percentages:

```
0%, 10%, 20%, 30%, 40%, 50%
```

We then run the full pipeline for each and measure how typo noise affects semantic drift.

Python is used **only** for:
- Embedding generation  
- Cosine distance calculation  
- CSV export  
- Plotting  

## 2. Conceptual Architecture

Agents behave like Turing-machine transitions:

```
English input
   ↓
EN→ES agent
   ↓
Spanish intermediate
   ↓
ES→HE agent
   ↓
Hebrew intermediate
   ↓
HE→EN agent
   ↓
Final English output
```

Each agent:
- reads a file  
- calls Claude  
- writes the result  
- is fully stateless  

## 3. Repository Structure

```
llm-turing-translation/
  README.md
  run_single.sh
  run_batch.sh
  agents/
    en2es.sh
    es2he.sh
    he2en.sh
  data/
    en_input_0.txt
    en_input_10.txt
    en_input_20.txt
    en_input_30.txt
    en_input_40.txt
    en_input_50.txt
  embeddings/
    distance_utils.py
    run_experiment.py
  experiments/
    .gitkeep
```

## 4. Installation

### Install Claude CLI

```
claude
/login
```

### Make scripts executable

```
chmod +x run_single.sh
chmod +x run_batch.sh
chmod -R +x agents/
```

### Install Python dependencies

```
pip install -r requirements.txt
```

## 5. Part 1 — Single Sentence Pipeline

```
./run_single.sh "this is my test sentence with severl tpoys in it"
```

Example output:

```
Original English:
this is my test sentence with severl tpoys in it

[EN → ES]
[ES → HE]
[HE → EN]

Final English:
This is my text with a few typos in it.

Cosine distance: 0.1039
```

## 6. Part 2 — Typo% vs Semantic Drift

Input files:

```
data/en_input_0.txt
data/en_input_10.txt
data/en_input_20.txt
data/en_input_30.txt
data/en_input_40.txt
data/en_input_50.txt
```

### Run batch translations

```
./run_batch.sh
```

### Run experiment (plot + CSV)

```
cd embeddings
python run_experiment.py
```

Result files:

```
experiments/results.csv
experiments/typos_vs_distance.png
```

## 7. Embeddings

We use simple 26-dimensional letter frequency vectors + cosine distance (allowed per assignment).

All implemented in:

```
embeddings/distance_utils.py
```

## 8. Conclusion

This project demonstrates:
- LLM agents orchestrated as stateless translators  
- File-based communication like a Turing machine  
- Effect of typos on semantic drift  
- Clean separation between LLM usage (bash) and measurement (Python)  
