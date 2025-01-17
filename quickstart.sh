#!/bin/bash

# Make scripts executable
chmod +x deploy-prod.sh
chmod +x deploy.sh

# Create necessary directories
mkdir -p nginx/ssl
mkdir -p nginx/conf.d

# Copy configuration files
cp nginx/conf.d/default.conf.example nginx/conf.d/default.conf

# Generate self-signed SSL certificate for development
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Start the application
docker-compose up --build -d

echo "Application is running!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000" 