#!/usr/bin/env bash
# Spanish → Hebrew agent
# Usage: ./agents/es2he.sh INPUT_FILE OUTPUT_FILE

set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 INPUT_FILE OUTPUT_FILE"
  exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

MODEL="haiku"

USER_MESSAGE="$(cat "$INPUT_FILE")"

PROMPT=$'Translate the following text from Spanish to Hebrew.\n'\
$'Rules:\n'\
$'- ALWAYS respond in Hebrew.\n'\
$'- ONLY output the translated sentence.\n'\
$'- Do NOT add explanations, comments, or extra text.\n\n'"$USER_MESSAGE"

claude \
  --print \
  --model "$MODEL" \
  "$PROMPT" \
  > "$OUTPUT_FILE"
