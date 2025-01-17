#!/bin/bash

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Clear npm cache
npm cache clean --force

# Install dependencies
npm install

# Build the project
npm run build 