#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
css="$DIR/../app/static/css"

cleancss \
    -o app/static/gen/bundle.min.css \
    "$css/normalize.css" \
    "$css/bootstrap.css" \
    "$css/syntax.css" \
    "$css/global.css"
