#!/bin/bash

# This is a script that can be run on a freshly setup server (see the README
# for more details) and bring it up to a production-ready state.  This script
# requires sudo privileges to work and it should already be scaffolded using
# bin/scaffold.sh

# Setup server
sudo hostnamectl set-hostname "albertyw.com"

# Clone repository
git clone "git@github.com:albertyw/albertyw.com"
sudo mkdir -p /var/www
rm -rf /var/www/albertyw.com
sudo mv "albertyw.com" /var/www/albertyw.com
cd /var/www/albertyw.com || exit 1
ln -s .env.production .env
sudo ln -s /var/www/albertyw.com ~/albertyw.com

# Install nginx
sudo add-apt-repository ppa:nginx/stable
sudo apt update
sudo apt install -y nginx

# Configure nginx
sudo rm -rf /etc/nginx/sites-available
sudo rm -rf /etc/nginx/sites-enabled/*
sudo ln -s /var/www/albertyw.com/config/sites-available/app /etc/nginx/sites-enabled/albertyw.com-app
sudo ln -s /var/www/albertyw.com/config/sites-available/headers /etc/nginx/sites-enabled/albertyw.com-headers
sudo rm -rf /var/www/html

# Secure nginx
sudo mkdir -p /etc/nginx/ssl
sudo openssl dhparam -out /etc/nginx/ssl/dhparams.pem 2048
# Copy server.key and server.pem to /etc/nginx/ssl.  The private/public key
# pair can be generated from Cloudflare or letsencrypt.
sudo service nginx restart

# Setup up docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce
sudo usermod -aG docker ${USER}
