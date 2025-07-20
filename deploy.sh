#!/bin/bash

# Deployment script for Meal Planner Application

set -e

echo "🚀 Starting deployment process..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Please create a .env file based on .env.example"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p pdfs

# Pull latest changes (if using git)
if [ -d .git ]; then
    echo "📥 Pulling latest changes from git..."
    git pull origin main || true
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start containers
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting containers..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "✅ Checking service status..."
docker-compose ps

echo "✨ Deployment completed successfully!"
echo "📱 Frontend is available at http://localhost"
echo "🔌 Backend API is available at http://localhost:8000"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop services: docker-compose down"