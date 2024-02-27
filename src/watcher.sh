#!/bin/bash

# Define the source and destination directories
src_dir="."
dest_dir="pi@raspberrypi.local:/home/pi/spotipi/"

# Define the file extensions to track
extensions=(py sh json txt html service js css ogg)

# Sync the files to the destination directory
sshpass -p "adtrsf#1" rsync -zarv --delete --prune-empty-dirs --include="*/" --include="*.ini" --include="*.cache" --include="*.map" --include="*.ogg" --include="*.py" --include="*.sh" --include="*.json" --include="*.txt" --include="*.js" --include="*.css" --include="*.service" --include="*.html" --exclude="*" --exclude "__pycache__/" "$src_dir" "$dest_dir"
sshpass -p "adtrsf#1" ssh pi@raspberrypi.local 'sudo systemctl daemon-reload; sudo systemctl restart spotipi-watchers.service'

# Watch for changes in the source directory and sync them to the destination directory

while inotifywait -r -e modify,create,delete,move,move_self $src_dir; do
    sshpass -p "adtrsf#1" rsync -zarv --delete --prune-empty-dirs --include="*/" --include="*.ini" --include="*.cache" --include="*.map" --include="*.ogg"  --include="*.py" --include="*.sh" --include="*.json" --include="*.txt" --include="*.js" --include="*.css" --include="*.service" --include="*.html" --exclude="*" --exclude "__pycache__/" "$src_dir" "$dest_dir"
    sshpass -p "adtrsf#1" ssh pi@raspberrypi.local 'sudo systemctl daemon-reload; sudo systemctl restart spotipi-watchers.service'
done
