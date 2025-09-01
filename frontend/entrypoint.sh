#!/bin/bash

# Exit on any error
set -e

echo "Installing Node.js dependencies..."
npm install -g pnpm
pnpm install --shamefully-hoist

echo "Building the application..."
pnpm run build

echo "Starting the application..."
exec pnpm start
