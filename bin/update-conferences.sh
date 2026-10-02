#!/bin/bash

# This script runs a Claude session that researches conferences and updates
# the conference data, then commits the data to master without pushing.
# See app/conference/INSTRUCTIONS.md

set -euo pipefail
IFS=$'\n\t'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"/.. || exit

DATA_FILES=(app/conference/conferences.json app/conference/metadata.json)

if [ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]; then
    echo "Must be run on master" >&2
    exit 1
fi
if [ -n "$(git status --porcelain)" ]; then
    echo "Working tree must be clean" >&2
    exit 1
fi

claude -p "Follow app/conference/INSTRUCTIONS.md" \
    --restricted \
    --strict-mcp-config \
    --permission-mode dontAsk \
    --tools "Read,Glob,Grep,Edit,Write,WebSearch,WebFetch,Agent,Bash" \
    --allowedTools \
        "Read" "Glob" "Grep" "WebSearch" "WebFetch" "Agent" \
        "Edit(/app/conference/conferences.json)" \
        "Edit(/app/conference/metadata.json)" \
        "Write(/app/conference/conferences.json)" \
        "Write(/app/conference/metadata.json)" \
        "Bash(python -m unittest app.conference.tests.test_data)"

CHANGED="$(git status --porcelain | cut -c4-)"
if [ -z "$CHANGED" ]; then
    echo "No changes"
    exit 0
fi
for file in $CHANGED; do
    if [[ ! " ${DATA_FILES[*]} " =~ \ $file\  ]]; then
        echo "Unexpected change to $file; not committing" >&2
        exit 1
    fi
done

python -m unittest discover -s app/conference/tests -t .
git commit -m "Update conference calendar data" -- "${DATA_FILES[@]}"
