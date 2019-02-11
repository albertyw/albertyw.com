#!/bin/bash

# This script will build and deploy a new docker image

set -ex

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"/..

source .env

if [ "$ENV" = "production" ]; then
    # Update repository
    git checkout master
    git fetch -tp
    git pull
fi

# Build and start container
docker build -t albertyw.com:$ENV .
docker stop albertyw.com || true
docker container prune --force --filter "until=336h"
docker container rm albertyw.com || true
docker run \
    --detach \
    --restart=always \
    --publish=127.0.0.1:5000:5000 \
    --mount type=bind,source="$(pwd)"/app/static,target=/var/www/app/app/static \
    --mount type=bind,source="$(pwd)"/logs,target=/var/www/app/logs \
    --name albertyw.com albertyw.com:$ENV

if [ "$ENV" = "production" ]; then
    # Cleanup docker
    docker image prune --force --filter "until=336h"

    # Update nginx
    sudo service nginx reload
fi
