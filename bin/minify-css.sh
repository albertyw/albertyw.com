#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

css=app/static/css

cleancss \
    -o app/static/gen/bundle.min.css \
    "$css/normalize.css" \
    "$css/bootstrap.css" \
    "$css/syntax.css" \
    "$css/global.css"
