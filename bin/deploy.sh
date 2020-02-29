#!/bin/bash

# This script will build and deploy a new docker image

set -exuo pipefail
IFS=$'\n\t'

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
docker pull "$(grep FROM Dockerfile | awk '{print $2}')"
docker build -t "albertyw:$ENV" .
docker network inspect "albertyw" &>/dev/null ||
    docker network create --driver bridge "albertyw"
docker stop "albertyw" || true
docker container prune --force --filter "until=168h"
docker image prune --force --filter "until=168h"
docker volume prune --force
docker container rm "albertyw" || true
docker run \
    --detach \
    --restart=always \
    --publish="127.0.0.1:5000:5000" \
    --network="albertyw" \
    --mount type=bind,source="$(pwd)"/app/static,target=/var/www/app/app/static \
    --mount type=bind,source="$(pwd)"/logs,target=/var/www/app/logs \
    --name "albertyw" "albertyw:$ENV"

if [ "$ENV" = "production" ]; then
    # Cleanup docker
    docker image prune --force --filter "until=168h"

    # Update nginx
    sudo service nginx reload
fi
