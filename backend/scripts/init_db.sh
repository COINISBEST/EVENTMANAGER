#!/bin/bash
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Creating initial data..."
python -m app.initial_data 