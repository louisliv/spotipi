#!/bin/bash

# Globals
CONTAINER_NAME="rfid-reader"

# Return an error if the container is not running
if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
  echo "Error: The container is not running"
  exit 1
fi

# Execute the command to scan a fake RFID tag
docker exec -it $CONTAINER_NAME python3 /usr/src/app/spotipi/fake_mfrc.py
