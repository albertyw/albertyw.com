#!/bin/bash

# This is a script that can be run on a freshly setup server (see the README
# for more details) and bring it up to a production-ready state.  This script
# requires sudo privileges to work and it should already be scaffolded using
# bin/scaffold.sh

set -exuo pipefail
IFS=$'\n\t'

# Clone repository
cd ~
git clone "git@github.com:albertyw/albertyw.com"

# Set up directory structures
ln -s .env.production .env
