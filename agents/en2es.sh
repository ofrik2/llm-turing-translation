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

# You can use an alias like "opus" / "sonnet" or full model name
MODEL="opus"

SYSTEM_PROMPT="You are a professional translator. Translate the user's text from English to Spanish. Only output the translated sentence, without any explanations or extra text."

# Read the input file content as the user message
USER_MESSAGE="$(cat "$INPUT_FILE")"

claude \
  --model "$MODEL" \
  --system-prompt "$SYSTEM_PROMPT" \
  -p "$USER_MESSAGE" \
  > "$OUTPUT_FILE"
