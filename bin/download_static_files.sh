#!/usr/bin/env bash

set -exuo pipefail
IFS=$'\n\t'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"/.. || exit

# Download resume
rm -rf resume
git clone git@github.com:albertyw/resume
mv resume/resume.pdf static/gen/resume.pdf
rm -rf resume

# Download timezone map
wget -O static/notes/20260926-0504-timezone-boundaries.png https://github.com/albertyw/localtimezone/blob/master/tzmap/map.png?raw=true
