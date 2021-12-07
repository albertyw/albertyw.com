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

# Configure nginx
sudo rm /etc/nginx/nginx.conf
sudo rm -rf /etc/nginx/sites-available
sudo cp "/home/albertyw/albertyw.com/config/nginx/nginx.conf" "/etc/nginx/nginx.conf"
sudo cp "/home/albertyw/albertyw.com/config/nginx/gzip.conf" "/etc/nginx/snippets/gzip.conf"
sudo cp "/home/albertyw/albertyw.com/config/nginx/headers.conf" "/etc/nginx/snippets/headers.conf"
sudo cp "/home/albertyw/albertyw.com/config/nginx/ssl.conf" "/etc/nginx/snippets/ssl.conf"
sudo mkdir -p "/var/log/nginx/albertyw.com/"
sudo rm -rf /var/www/html

# Set up directory structures
ln -s .env.production .env
