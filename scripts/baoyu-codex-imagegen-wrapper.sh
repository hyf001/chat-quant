#!/bin/sh
set -eu

export PATH="/Users/huyufei/.vscode/extensions/openai.chatgpt-26.727.40816-darwin-arm64/bin/macos-aarch64:$PATH"
exec bun /Users/huyufei/Documents/hyf/code/github/baoyu-skills/skills/baoyu-image-gen/scripts/codex-imagegen/main.ts "$@" --retries 0
