#!/bin/bash

# This script will build and deploy a new docker image

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"/..

# Update repository
git checkout master
git fetch -tp
git pull

# Build and start container
docker build -t albertyw.com:production .
docker stop albertyw.com || echo
docker container prune -f
docker run --detach --restart always -p 127.0.0.1:5000:5000 --name albertyw.com albertyw.com:production

# Cleanup docker
docker image prune -f --filter "until=14d"

# Update nginx
sudo service nginx reload
