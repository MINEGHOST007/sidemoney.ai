#!/bin/bash

# Exit on any error
set -e

echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Creating uploads directory..."
mkdir -p uploads

echo "Starting the application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
