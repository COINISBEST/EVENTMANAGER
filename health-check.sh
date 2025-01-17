#!/bin/bash
set -e

# Check frontend
echo "Checking frontend..."
if curl -f http://localhost:80 > /dev/null 2>&1; then
    echo "Frontend is running"
else
    echo "Frontend is down!"
    exit 1
fi

# Check backend
echo "Checking backend..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "Backend is running"
else
    echo "Backend is down!"
    exit 1
fi

# Check database
echo "Checking database..."
if docker-compose -f docker-compose.prod.yml exec db pg_isready -U $DB_USER > /dev/null 2>&1; then
    echo "Database is running"
else
    echo "Database is down!"
    exit 1
fi

echo "All systems are operational!" 