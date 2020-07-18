#!/bin/bash

# This is a script that can be run on a freshly setup server (see the README
# for more details) and bring it up to a production-ready state.

set -exuo pipefail
IFS=$'\n\t'

# Download resume
curl -L https://github.com/albertyw/resume/raw/master/resume.pdf > static/gen/resume.pdf

# Minify static files
npm run minify

# Run supervisor to run uwsgi
supervisord
