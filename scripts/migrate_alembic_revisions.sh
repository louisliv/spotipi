#!/bin/bash

DOCKER_CONTAINER_NAME="spotipi-server"

# execute alembic upgrade head in the docker container
docker exec -it $DOCKER_CONTAINER_NAME alembic upgrade head
