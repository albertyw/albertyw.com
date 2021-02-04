#!/bin/bash

# This is a script that can be run on a freshly setup server (see the README
# for more details) and bring it up to a production-ready state.  This script
# requires sudo privileges to work and it should already be scaffolded using
# bin/scaffold.sh

set -exuo pipefail
IFS=$'\n\t'

# Setup server
sudo hostnamectl set-hostname "albertyw.com"

# Clone repository
cd ~
git clone "git@github.com:albertyw/albertyw.com"

# Setup up docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
sudo usermod -aG docker "${USER}"

# Set up directory structures
ln -s .env.production .env
