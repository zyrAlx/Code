#!/bin/bash

# Get the path to the DOCKBASE environment variable
DOCKBASE_PATH="$DOCKBASE"

# Create a file to store all the commands
command_file="blastermaster_commands.txt"
touch "$command_file"

# Loop over all directories in the current directory
for dir in ./*/
do
  # Add the command to the file
  echo "cd ${dir} && ${DOCKBASE_PATH}/proteins/blastermaster/blastermaster.py --addhOptions=' -HIS -FLIPs ' -v && cd .." >> "$command_file"
done