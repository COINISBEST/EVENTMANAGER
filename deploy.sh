#!/bin/bash

# Exit on error
set -e

# Load environment variables
source .env

# Check if running in production
if [ "$NODE_ENV" != "production" ]; then
    echo "Error: This script should only be run in production"
    exit 1
fi

# Pull latest changes
git pull origin main

# Build and start containers
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Clean up old images
docker image prune -f

echo "Deployment completed successfully!" 