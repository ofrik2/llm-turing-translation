#!/usr/bin/env bash

# Usage:
#   ./run_single.sh "your English sentence here"

set -e

if [ $# -lt 1 ]; then
  echo "Usage: $0 \"your English sentence here\""
  exit 1
fi

DATA_DIR="data"
mkdir -p "$DATA_DIR"

ORIG_FILE="$DATA_DIR/single_input.txt"
ES_FILE="$DATA_DIR/single_es.txt"
HE_FILE="$DATA_DIR/single_he.txt"
BACK_FILE="$DATA_DIR/single_en_back.txt"

SENTENCE="$*"

# 1. Save original sentence
echo "$SENTENCE" > "$ORIG_FILE"

echo "Original English:"
cat "$ORIG_FILE"
echo

# 2. Run through the three agents
echo "[EN → ES]"
./agents/en2es.sh "$ORIG_FILE" "$ES_FILE"

echo "[ES → HE]"
./agents/es2he.sh "$ES_FILE" "$HE_FILE"

echo "[HE → EN]"
./agents/he2en.sh "$HE_FILE" "$BACK_FILE"

echo
echo "Final English:"
cat "$BACK_FILE"
echo

# 3. Compute embedding distance (Python is allowed here)
python3 - <<EOF
from embeddings.distance_utils import compute_distance_between_files
dist, orig, back = compute_distance_between_files("$ORIG_FILE", "$BACK_FILE")
print(f"Cosine distance: {dist}")
EOF
