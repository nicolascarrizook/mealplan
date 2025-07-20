#!/bin/bash

# Quick setup script for DigitalOcean Droplet
# Copy and paste this in your droplet console

echo "🚀 Starting Meal Planner setup..."

# Update system
apt-get update && apt-get upgrade -y

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Install git if not present
apt-get install -y git

echo "✅ Prerequisites installed!"
echo ""
echo "Next steps:"
echo "1. Clone your repository"
echo "2. Create .env file"
echo "3. Run docker-compose up -d"