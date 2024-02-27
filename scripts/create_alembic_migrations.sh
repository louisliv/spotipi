#!/bin/bash

DOCKER_CONTAINER_NAME="spotipi-server"

# execute alembic revision --autogenerate in the docker container
docker exec -it $DOCKER_CONTAINER_NAME alembic revision --autogenerate