#!/bin/bash

RASPBERRYPI_HOST=$1
RASPBERRYPI_USERNAME="${2:-pi}"
SHOULD_BUILD_WHLS="${3:-true}"
BUILD_RETURN_VALUE=0

# Return an error if the Raspberry Pi host is not provided
if [ -z "$RASPBERRYPI_HOST" ]; then
    echo "Raspberry Pi host not provided"
    exit 1
fi

if [ "$SHOULD_BUILD_WHLS" = "true" ]; then
    # Call the build_whls.sh script
    BUILD_RETURN_VALUE=$(./build_whls.sh)
fi

# Return an error if the build failed
if [ $BUILD_RETURN_VALUE -ne 0 ]; then
    echo "Build failed"
    exit 1
fi

# Return an an error if the build succeeded but no whl files were found
if [ ! -f dist/*.whl ]; then
    echo "No whl files found"
    exit 1
fi

# Copy the whl files to the Raspberry Pi
scp dist/*.whl $RASPBERRYPI_USERNAME@$RASPBERRYPI_HOST:/tmp

# Install the whl files on the Raspberry Pi
ssh $RASPBERRYPI_USERNAME@$RASPBERRYPI_HOST "pip3 install /tmp/*.whl"

# Stop and remove all spotipi systemd services
ssh $RASPBERRYPI_USERNAME@$RASPBERRYPI_HOST "sudo systemctl stop spotipi*"

# Copy the spotipi systemd service files to the Raspberry Pi
scp service-files/spotipi*.service $RASPBERRYPI_USERNAME@$RASPBERRYPI_HOST:/tmp

# Move the spotipi systemd service files to the systemd directory
ssh $RASPBERRYPI_USERNAME@$RASPBERRYPI_HOST "sudo mv /tmp/spotipi*.service /etc/systemd/system"

# Reload the systemd daemon
ssh $RASPBERRYPI_USERNAME@$RASPBERRYPI_HOST "sudo systemctl daemon-reload"

# Start all spotipi systemd services
ssh $RASPBERRYPI_USERNAME@$RASPBERRYPI_HOST "sudo systemctl start spotipi*"

# Enable all spotipi systemd services
ssh $RASPBERRYPI_USERNAME@$RASPBERRYPI_HOST "sudo systemctl enable spotipi*"

exit 0
