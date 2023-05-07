#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 port_number"
  exit 1
fi

port=$1

# Find the process running on the specified port
process=$(sudo netstat -ltnp | grep LISTEN | grep ":$port " | awk '{print $7}' | cut -d '/' -f 1)

if [ -n "$process" ]; then
  echo "Process running on port $port: $process"

  # Force kill the process
  sudo kill -9 $process

  echo "Process terminated."
else
  echo "No process found running on port $port"
fi