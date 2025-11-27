#!/usr/bin/env bash
set -e

DATA_DIR="data"
mkdir -p "$DATA_DIR"

# Typo levels to process:
LEVELS=(0 10 20 30 40 50)

for LEVEL in "${LEVELS[@]}"; do
  ORIG_FILE="$DATA_DIR/en_input_${LEVEL}.txt"
  ES_FILE="$DATA_DIR/es_${LEVEL}.txt"
  HE_FILE="$DATA_DIR/he_${LEVEL}.txt"
  BACK_FILE="$DATA_DIR/en_back_${LEVEL}.txt"

  echo "=== Running pipeline for typo level ${LEVEL}% ==="

  if [ ! -f "$ORIG_FILE" ]; then
    echo "WARNING: $ORIG_FILE does not exist, skipping this level."
    continue
  fi

  ./agents/en2es.sh "$ORIG_FILE" "$ES_FILE"
  ./agents/es2he.sh "$ES_FILE" "$HE_FILE"
  ./agents/he2en.sh "$HE_FILE" "$BACK_FILE"

  echo "Created round-trip file: $BACK_FILE"
  echo
done
