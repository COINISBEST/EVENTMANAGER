#!/bin/bash
set -e

# Load environment variables
source .env.production

# Get the current version
CURRENT_VERSION=$(git rev-parse HEAD)

# Check if version to rollback to is provided
if [ -z "$1" ]; then
    echo "Please provide the version to rollback to"
    echo "Usage: ./rollback.sh <commit-hash>"
    exit 1
fi

# Checkout the specified version
git checkout $1

# Rebuild and restart containers
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d

# Run database rollback if needed
docker-compose -f docker-compose.prod.yml exec backend alembic downgrade -1

echo "Rollback completed successfully!"
echo "If there are any issues, you can revert back to $CURRENT_VERSION" 