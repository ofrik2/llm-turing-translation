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

MODEL="opus"

SYSTEM_PROMPT="You are a professional translator. Translate the user's text from Hebrew to English. Only output the translated sentence, without any explanations or extra text."

USER_MESSAGE="$(cat "$INPUT_FILE")"

claude \
  --model "$MODEL" \
  --system-prompt "$SYSTEM_PROMPT" \
  -p "$USER_MESSAGE" \
  > "$OUTPUT_FILE"
