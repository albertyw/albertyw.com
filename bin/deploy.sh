#!/bin/bash

# This script will build and deploy a new docker image

# Update repository
cd /var/www/albertyw.com/ || exit 1
git checkout master
git fetch -tp
git pull

# Build and start container
docker build -t albertyw.com:production .
docker stop $(docker ps -q --filter ancestor=albertyw.com:production )
docker run --detach --restart always -p 127.0.0.1:8080:8080 albertyw.com:production

# Download static files
wget https://github.com/albertyw/resume/raw/master/resume.pdf
mv resume.pdf app/static/gen/resume.pdf

# Cleanup dockeer
docker container prune -f
docker image prune -f
