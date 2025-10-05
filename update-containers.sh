#!/bin/bash

# Define Docker Hub images
BACKEND_IMAGE="<ник>/backend:latest"
FRONTEND_IMAGE="<ник>/frontend:latest"

# Define container names
BACKEND_CONTAINER="backend_container"
FRONTEND_CONTAINER="frontend_container"

# Log file for updates
LOG_FILE="update-log.txt"

# Function to check and update a container
update_container() {
  local IMAGE=$1
  local CONTAINER=$2

  echo "Checking for updates for $IMAGE..." | tee -a $LOG_FILE

  # Pull the latest image
  docker pull $IMAGE > /dev/null 2>&1

  # Check if the image was updated
  UPDATED=$(docker images --filter=reference="$IMAGE" --format "{{.ID}}" | head -n 1)
  RUNNING=$(docker inspect --format='{{.Image}}' $CONTAINER 2>/dev/null || echo "")

  if [ "$UPDATED" != "$RUNNING" ]; then
    echo "Updating $CONTAINER..." | tee -a $LOG_FILE
    docker-compose down > /dev/null 2>&1
    docker-compose up -d > /dev/null 2>&1
    echo "$CONTAINER updated successfully." | tee -a $LOG_FILE
  else
    echo "$CONTAINER is already up-to-date." | tee -a $LOG_FILE
  fi
}

# Update backend and frontend containers
update_container $BACKEND_IMAGE $BACKEND_CONTAINER
update_container $FRONTEND_IMAGE $FRONTEND_CONTAINER

# Log completion time
echo "Update check completed at $(date)" | tee -a $LOG_FILE