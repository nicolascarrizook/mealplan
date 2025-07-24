# Production Deployment Commands

## Quick Fix for Port Conflict

You're using the wrong docker-compose file. Here are the correct commands:

```bash
# Stop any running containers from the development compose file
docker compose down

# Use the production compose file instead
docker-compose -f docker-compose.prod.yml up -d --build
```

## Full Production Deployment Process

```bash
# 1. Navigate to project directory
cd /opt/apps/mealplan

# 2. Pull latest changes
git pull origin main

# 3. Create required directories if they don't exist
mkdir -p backend/temp_uploads backend/generated_pdfs

# 4. Stop any existing containers
docker-compose -f docker-compose.prod.yml down

# 5. Build and start production containers
docker-compose -f docker-compose.prod.yml up -d --build

# 6. Check container status
docker-compose -f docker-compose.prod.yml ps

# 7. Monitor logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Important Notes

- Always use `docker-compose.prod.yml` on the production server
- The development `docker-compose.yml` is only for local development
- Production setup uses nginx as reverse proxy on port 80
- Backend runs on port 8000 internally, proxied through nginx
- ChromaDB runs on port 8001 internally

## Verify Everything is Working

After deployment, check:
1. All containers are running: `docker-compose -f docker-compose.prod.yml ps`
2. Backend is healthy: `docker-compose -f docker-compose.prod.yml logs backend | tail -50`
3. File upload works by testing on the website