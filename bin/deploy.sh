#!/bin/bash

# This script will build and deploy a new docker image

# Update repository
cd ~/albertyw.com/ || exit 1
git checkout master
git fetch -tp
git pull

# Build and start container
docker build -t albertyw.com:production .
docker stop albertyw.com || echo
docker container prune -f
docker run --detach --restart always -p 127.0.0.1:5000:5000 --name albertyw.com albertyw.com:production

# Cleanup docker
docker image prune -f

# Update nginx
sudo service nginx reload
