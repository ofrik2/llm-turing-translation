#!/usr/bin/env bash
# English → Spanish agent
# Usage: ./agents/en2es.sh INPUT_FILE OUTPUT_FILE

set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 INPUT_FILE OUTPUT_FILE"
  exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

MODEL="haiku"

# Read the input file content as the user message
USER_MESSAGE="$(cat "$INPUT_FILE")"

PROMPT=$'Translate the following text from English to Spanish.\n'\
$'Rules:\n'\
$'- ALWAYS respond in Spanish.\n'\
$'- ONLY output the translated sentence.\n'\
$'- Do NOT add explanations, comments, or extra text.\n\n'"$USER_MESSAGE"

claude \
  --print \
  --model "$MODEL" \
  "$PROMPT" \
  > "$OUTPUT_FILE"
