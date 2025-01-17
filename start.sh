#!/bin/bash

# Build and start the containers
docker-compose up --build -d

# Wait for the database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run database migrations
docker-compose exec backend alembic upgrade head

# Show logs
docker-compose logs -f 