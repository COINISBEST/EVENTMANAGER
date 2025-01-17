#!/bin/bash
set -e

# Load environment variables
set -a
source .env.production
set +a

# Deploy frontend
echo "Deploying frontend..."
cd frontend
npm install
npm run build:prod
cd ..

# Start Docker containers
echo "Starting Docker containers..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d

# Run migrations
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

echo "Deployment completed successfully!" 