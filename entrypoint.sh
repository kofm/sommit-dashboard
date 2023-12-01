#!/bin/sh

# Wait for the file to be present
while [ ! -f /data/mfa-ind-coord.csv ]; do
  echo "Waiting for data-processor to complete..."
  sleep 5
done

# Start the main process
exec gunicorn --reload -b 0.0.0.0:80 app:server
