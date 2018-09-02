#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $DIR/..

curl https://github.com/albertyw/resume/raw/master/resume.pdf > app/static/gen/resume.pdf
