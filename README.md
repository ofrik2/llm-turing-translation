# LLM Turing Translation

A Turing-machine-inspired experiment that measures semantic drift in language through multi-step LLM translation chains.

## Overview

This project implements a simple "Turing-machine-like" system composed of three LLM-based agents that communicate through files. Each agent performs one translation step in a chain:

```
English → Spanish → Hebrew → English
```

The system introduces controlled typos into an original English sentence, passes it through the translation chain, and measures the semantic distance between the original and final English output using vector embeddings and cosine distance.

### The Analogy to Turing Machines

In this project, an **agent** is a small, stateless program that:
- Takes text as input (from a file)
- Performs a transformation (translation)
- Writes text as output (to a file)
- Has no memory of previous calls
- Only communicates through files

This is analogous to a Turing Machine, where:
- The **"tape"** = files on disk
- Each **agent** = one simple state/transition
- The **whole system** = a pipeline of simple steps

## Project Structure

```
llm-turing-translation/
├── .gitignore              # Ignore Python caches, venvs, etc.
├── README.md               # This documentation
├── requirements.txt        # Python dependencies for embeddings/plotting
├── run_pipeline.sh         # Orchestrates the three translation agents
├── agents/
│   ├── en2es.sh           # English → Spanish agent
│   ├── es2he.sh           # Spanish → Hebrew agent
│   └── he2en.sh           # Hebrew → English agent
├── data/
│   ├── en_input_0.txt     # English sentence, 0% typos
│   ├── en_input_20.txt    # English sentence, ~20% typos
│   ├── en_input_40.txt    # English sentence, ~40% typos
│   └── ...                # Generated files from pipeline
├── embeddings/
│   └── compute_distances.py  # Embeddings + cosine distance + plotting
└── experiments/
    └── .gitkeep           # Placeholder (results CSV and PNG go here)
```

## How It Works

For a given typo level X (e.g., 0, 20, 40%):

1. **Input**: `data/en_input_X.txt` — Original English with X% typos
2. **Step 1**: `agents/en2es.sh` → `data/es_X.txt` — English → Spanish
3. **Step 2**: `agents/es2he.sh` → `data/he_X.txt` — Spanish → Hebrew
4. **Step 3**: `agents/he2en.sh` → `data/en_back_X.txt` — Hebrew → English
5. **Analysis**: Compare `en_input_X.txt` and `en_back_X.txt` using embeddings

The semantic distance is calculated using cosine similarity of sentence embeddings, revealing how much meaning is lost or altered through the translation chain at different noise levels.

## Prerequisites

- **Bash shell** (Linux, macOS, or WSL on Windows)
- **Python 3.7+** with pip
- **Claude CLI** (or another LLM CLI tool)
  - Install: Follow [Anthropic's Claude CLI documentation](https://docs.claude.com)
  - Configure with your API key

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ofrik2/llm-turing-translation.git
   cd llm-turing-translation
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make agent scripts executable:**
   ```bash
   chmod +x agents/*.sh
   chmod +x run_pipeline.sh
   ```

4. **Verify Claude CLI is installed:**
   ```bash
   claude --version
   ```

## Usage

### Basic Usage

Run the complete pipeline for all typo levels:

```bash
./run_pipeline.sh
```

This will:
1. Process all input files in `data/` (0%, 20%, 40% typos)
2. Run each through the three translation agents
3. Generate intermediate and final translation files

### Step-by-Step Usage

You can also run individual translation steps:

**English to Spanish:**
```bash
./agents/en2es.sh
# Reads: data/en_input_X.txt
# Writes: data/es_X.txt
```

**Spanish to Hebrew:**
```bash
./agents/es2he.sh
# Reads: data/es_X.txt
# Writes: data/he_X.txt
```

**Hebrew to English:**
```bash
./agents/he2en.sh
# Reads: data/he_X.txt
# Writes: data/en_back_X.txt
```

### Computing Semantic Distance

After running the pipeline, compute the semantic distances and generate visualizations:

```bash
python embeddings/compute_distances.py
```

This will:
- Load original and round-trip English texts
- Generate embeddings for each sentence
- Calculate cosine distances
- Create a plot showing typo rate vs. semantic drift
- Save results to `experiments/results.csv` and `experiments/semantic_drift_plot.png`

### Adding Custom Input

To test with your own sentences:

1. Create a new input file in `data/`:
   ```bash
   echo "Your English sentence here" > data/en_input_custom.txt
   ```

2. Modify `run_pipeline.sh` to include your custom input, or run agents manually:
   ```bash
   # Update the input file path in each agent script
   ./agents/en2es.sh
   ./agents/es2he.sh
   ./agents/he2en.sh
   ```

3. Compute the semantic distance for your custom input

## Understanding the Results

The output from `compute_distances.py` includes:

- **CSV file** (`experiments/results.csv`): Tabular data with typo percentages and corresponding cosine distances
- **Plot** (`experiments/semantic_drift_plot.png`): Visual representation of how semantic meaning degrades with increased noise

**Interpretation:**
- **Low distance (close to 0)**: High semantic similarity, meaning is preserved
- **High distance (close to 2)**: Low semantic similarity, significant meaning loss
- The curve shows the relationship between input noise (typos) and output degradation

## Experiment Ideas

- Test different source languages
- Add more translation steps (e.g., English → Spanish → Hebrew → French → English)
- Vary the typo types (character swaps, deletions, insertions)
- Compare different LLM models
- Test with different text genres (technical, conversational, poetic)

## Configuration

### Changing the LLM

The agent scripts use Claude CLI by default. To use a different LLM:

1. Open each agent script (e.g., `agents/en2es.sh`)
2. Replace the `claude` command with your LLM CLI tool
3. Adjust the prompt format as needed for your model

Example:
```bash
# Instead of:
claude "Translate to Spanish: $(cat data/en_input_0.txt)"

# Use:
gpt-cli "Translate to Spanish: $(cat data/en_input_0.txt)"
```

### Adjusting Typo Levels

To create input files with different typo percentages:

1. Manually edit text files in `data/`
2. Or write a script to programmatically introduce typos
3. Name them following the pattern: `en_input_X.txt` where X is the typo percentage

## Troubleshooting

**Issue: "claude: command not found"**
- Solution: Install Claude CLI and ensure it's in your PATH

**Issue: Permission denied when running scripts**
- Solution: Make scripts executable with `chmod +x agents/*.sh run_pipeline.sh`

**Issue: Python module not found**
- Solution: Ensure you've installed dependencies with `pip install -r requirements.txt`

**Issue: No output files generated**
- Solution: Check that input files exist in `data/` and agent scripts have correct file paths

## Dependencies

- Python packages (see `requirements.txt`):
  - `sentence-transformers` or `openai` for embeddings
  - `numpy` for distance calculations
  - `matplotlib` for plotting
  - `pandas` for data handling

## Contributing

Contributions are welcome! Feel free to:
- Add new language pairs
- Improve distance metrics
- Add visualization features
- Optimize agent performance
- Write additional documentation

Please open an issue or submit a pull request.

## Acknowledgments

This project explores concepts from:
- Turing machines and computational theory
- Information theory and semantic preservation
- Natural language processing and machine translation
