#!/usr/bin/env bash
# Hebrew → English agent
# Usage: ./agents/he2en.sh INPUT_FILE OUTPUT_FILE

set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 INPUT_FILE OUTPUT_FILE"
  exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

MODEL="haiku"

USER_MESSAGE="$(cat "$INPUT_FILE")"

PROMPT=$'Translate the following text from Hebrew to English.\n'\
$'Rules:\n'\
$'- ALWAYS respond in English.\n'\
$'- ONLY output the translated sentence.\n'\
$'- Do NOT add explanations, comments, or extra text.\n\n'"$USER_MESSAGE"

claude \
  --print \
  --model "$MODEL" \
  "$PROMPT" \
  > "$OUTPUT_FILE"
