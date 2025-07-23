#!/bin/bash

echo "=== Meal Planner Pro - Deployment Verification ==="
echo ""

# Check if .env file exists
echo "1. Checking environment configuration..."
if [ -f .env ]; then
    echo "✓ .env file found"
    # Check for required variables
    if grep -q "OPENAI_API_KEY=" .env; then
        echo "✓ OPENAI_API_KEY is set"
    else
        echo "✗ OPENAI_API_KEY is missing in .env"
        exit 1
    fi
else
    echo "✗ .env file not found"
    echo "  Please create a .env file based on .env.example"
    exit 1
fi

# Check Docker installation
echo ""
echo "2. Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed"
    docker --version
else
    echo "✗ Docker is not installed"
    exit 1
fi

if command -v docker-compose &> /dev/null; then
    echo "✓ Docker Compose is installed"
    docker-compose --version
else
    echo "✗ Docker Compose is not installed"
    exit 1
fi

# Check if recipes file exists
echo ""
echo "3. Checking recipe data..."
if [ -f backend/data/recipes_structured.json ]; then
    echo "✓ Recipe file found"
    recipe_count=$(grep -o '"id":' backend/data/recipes_structured.json | wc -l)
    echo "  Found $recipe_count recipes"
else
    echo "✗ Recipe file not found at backend/data/recipes_structured.json"
    exit 1
fi

# Check Docker images can be built
echo ""
echo "4. Testing Docker build..."
echo "  This will take a few minutes on first run..."

# Build backend
echo "  Building backend..."
if docker build -q ./backend > /dev/null 2>&1; then
    echo "✓ Backend build successful"
else
    echo "✗ Backend build failed"
    exit 1
fi

# Build frontend
echo "  Building frontend..."
if docker build -q ./frontend > /dev/null 2>&1; then
    echo "✓ Frontend build successful"
else
    echo "✗ Frontend build failed"
    exit 1
fi

echo ""
echo "=== All checks passed! ==="
echo ""
echo "To deploy to production:"
echo "1. Update the VITE_API_URL in docker-compose.prod.yml with your domain/IP"
echo "2. Update BACKEND_CORS_ORIGINS in your .env file"
echo "3. Run: ./deploy.sh"
echo ""
echo "For initial deployment on a new server:"
echo "1. Copy this repository to your server"
echo "2. Run: ./install-on-droplet.sh"
echo "3. Follow the prompts to configure your domain"