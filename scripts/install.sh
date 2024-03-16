#!/bin/bash

# Install spotipi wheels
sudo pip3 install *.whl --break-system-packages --force-reinstall

# Copy the frontend build to the /var/www/spotipi directory
sudo rm -rf /var/www/spotipi
sudo mkdir -p /var/www/spotipi
sudo cp -r client/build/* /var/www/spotipi

# Copy the nginx configuration file to the /etc/nginx/sites-enabled directory
sudo cp spotipi-nginx.conf /etc/nginx/sites-enabled

# Remove the default nginx configuration file from the /etc/nginx/sites-enabled directory
sudo rm -f /etc/nginx/sites-enabled/default

# Stop and remove all spotipi systemd services if present
sudo systemctl stop spotipiservice-player
sudo systemctl stop spotipiservice-reader
sudo systemctl stop spotipiservice-scanner
sudo systemctl stop spotipiservice-server

sudo systemctl disable spotipiservice-player
sudo systemctl disable spotipiservice-reader
sudo systemctl disable spotipiservice-scanner
sudo systemctl disable spotipiservice-server

sudo rm /etc/systemd/system/spotipi*

# Copy the spotipi systemd service files to the systemd directory
sudo cp service-files/spotipiservice* /etc/systemd/system

# Reload the systemd daemon
sudo systemctl daemon-reload

# Enable all spotipi systemd services
sudo systemctl enable spotipiservice-player
sudo systemctl enable spotipiservice-reader
sudo systemctl enable spotipiservice-scanner
sudo systemctl enable spotipiservice-server

# Start all spotipi systemd services
sudo systemctl start spotipiservice-player
sudo systemctl start spotipiservice-reader
sudo systemctl start spotipiservice-scanner
sudo systemctl start spotipiservice-server

# Restart the nginx service
sudo systemctl restart nginx
