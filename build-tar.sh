#!/bin/bash

# This assumes that the spotipi wheels have been built and are in the dist directory

# Check if the dist directory is present
if [ ! -d dist ]; then
    echo "dist directory not found"
    exit 1
fi

# Remove the spotipi-build.tar.gz file if present
rm -f spotipi-build.tar.gz

# Wipe the spotipi-build directory
rm -rf spotipi-build/*

# Create spotipi-build directory if not present
mkdir -p spotipi-build
mkdir -p spotipi-build/service-files

# Copy the spotipi wheels to the spotipi-build directory
cp dist/*.whl spotipi-build

# Copy the install.sh script to the spotipi-build directory
cp scripts/install.sh spotipi-build

# Copy the spotipi systemd service files to the spotipi-build directory
cp service-files/spotipi*.service spotipi-build/service-files

# build the tar file
tar -czvf spotipi-build.tar.gz spotipi-build
