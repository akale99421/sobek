#!/bin/bash
# Run this once: ./fix-docker-perms.sh
# It will fix Docker permissions for the current session

sudo chmod 666 /var/run/docker.sock
echo "✅ Docker permissions fixed!"
echo "Now I can run docker commands automatically."

