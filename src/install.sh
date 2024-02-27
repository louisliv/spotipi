#!/bin/bash

# Install the required packages
sudo apt-get install -y redis-server python3-pip python3-venv sshpass ffmpeg sqlite3
sudo apt-get -y install curl && curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

# Enable and start the redis service
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Set the environment variables
export REDIS_HOST="127.0.0.1"
export REDIS_PORT="6379"

# Install the required python packages
python -m pip install -r requirements.txt --break-system-packages

# Create the database
sqlite3 rfid_spotify.db "VACUUM;"
alembic upgrade head

# Create sim links for the service files
sudo rm /etc/systemd/system/spotipi.service
sudo rm /etc/systemd/system/spotipi-watchers.service
sudo ln -s /home/pi/spotipi/spotipi.service /etc/systemd/system/spotipi.service
sudo ln -s /home/pi/spotipi/spotipi-watchers.service /etc/systemd/system/spotipi-watchers.service

# Enable and start the spotipi services
sudo systemctl daemon-reload
sudo systemctl enable spotipi
sudo systemctl enable spotipi-watchers
sudo systemctl start spotipi
sudo systemctl start spotipi-watchers
sudo systemctl restart spotipi
sudo systemctl restart spotipi-watchers