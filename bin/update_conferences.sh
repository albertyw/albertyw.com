#!/bin/bash

# This script runs a Claude session that researches conferences and updates
# the conference data, then commits the data to the current branch without
# pushing.
# See app/conference/INSTRUCTIONS.md

set -euo pipefail
IFS=$'\n\t'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"/.. || exit

DATA_FILES=(app/conference/conferences.json app/conference/metadata.json)

# Summarize each stream-json event as one timestamped progress line.
# Lines that aren't JSON (e.g. plain-text errors) are printed as-is.
# Control characters are stripped from every printed line, since text can
# come from fetched web pages.
# shellcheck disable=SC2016
PROGRESS='
def clean: tostring | gsub("[\u0000-\u0009\u000b-\u001f\u007f-\u009f]"; "");
def clip($n): clean | gsub("\\s+"; " ") | .[0:$n];
def prefix: if .parent_tool_use_id then "  [subagent] " else "" end;
def progress:
  if .type == "system" and .subtype == "init" then
    "session started, model \(.model)"
  elif .type == "assistant" then
    prefix as $p | .message.content[] |
    if .type == "text" then $p + "says: " + (.text | clip(200))
    elif .type == "tool_use" then $p + .name + " " + (
      .input | (.url // .query // .file_path // .command // .description // "")
      | clip(150))
    else empty end
  elif .type == "user" then
    prefix as $p | .message.content[]? |
    select(type == "object" and .type == "tool_result" and .is_error == true) |
    $p + "error: " + (.content | clip(200))
  elif .type == "result" then
    "finished: \(.subtype), \(.num_turns) turns, \(.duration_ms / 1000 | floor)s, $\(.total_cost_usd)\n\(.result)"
  else empty end;
(now | strflocaltime("%H:%M:%S")) as $time |
. as $line | (try fromjson catch $line) as $event |
if ($event | type) == "object" then $event | progress else $event end |
"\($time) \(clean)"'

if [ -n "$(git status --porcelain)" ]; then
    echo "Working tree must be clean" >&2
    exit 1
fi

LOG="$(mktemp -t update_conferences.XXXXXX.jsonl)"
echo "Full log: $LOG"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
claude -p "Follow app/conference/INSTRUCTIONS.md. The current UTC time is $NOW." \
    --output-format stream-json \
    --verbose \
    --forward-subagent-text \
    --model claude-sonnet-5-5 \
    --agents app/conference/agents.json \
    --restricted \
    --strict-mcp-config \
    --permission-mode dontAsk \
    --tools "Read,Edit,Write,WebSearch,WebFetch,Agent" \
    --allowedTools \
        "Read(/app/conference/**)" "WebSearch" "WebFetch" \
        "Agent(conference-researcher)" \
        "Edit(/app/conference/conferences.json)" \
        "Edit(/app/conference/metadata.json)" \
    --disallowedTools \
        "Read(/.env*)" "Read(/env/**)" "Read(/.git/**)" \
        "Read(/logs/**)" "Read(/claude/**)" "Read(/config/**)" \
        "Agent(model:*)" "Agent(general-purpose)" "Agent(Explore)" \
        "Agent(Plan)" "Agent(claude-code-guide)" "Agent(statusline-setup)" \
        "Agent(claude)" \
    | tee "$LOG" | jq --unbuffered -R -r "$PROGRESS"

CHANGED="$(git status --porcelain | cut -c4-)"
if [ -z "$CHANGED" ]; then
    echo "No changes"
    exit 0
fi
set -f  # Split $CHANGED on newlines only; don't expand changed paths as globs
for file in $CHANGED; do
    case "$file" in
        app/conference/conferences.json|app/conference/metadata.json) ;;
        *)
            echo "Unexpected change to $file; not committing" >&2
            exit 1
            ;;
    esac
done

python -m unittest discover -s app/conference/tests -t .
git commit -m "Update conference calendar data" -- "${DATA_FILES[@]}"
