# ChromaDB Connection Fix Instructions

## The issue has been identified and fixed ✅

The backend was failing to connect to ChromaDB due to a port conflict. Both the backend and ChromaDB were trying to use port 8000. I've updated the configuration to use port 8001 for ChromaDB.

## Changes made:

1. **docker-compose.prod.yml**: 
   - Changed ChromaDB to expose port 8001 instead of 8000
   - Added `CHROMA_SERVER_HTTP_PORT=8001` environment variable
   - Updated backend `CHROMADB_PORT` to 8001

2. **backend/app/config.py**: 
   - Changed default `chromadb_port` from 8000 to 8001

3. **docker-compose.yml** (development): 
   - Updated for consistency with production

## Steps to apply on the server:

```bash
# 1. Connect to the server (if not already connected)
ssh root@162.243.174.187

# 2. Go to the project directory
cd /opt/apps/mealplan

# 3. Get the latest changes
git pull origin main

# 4. Stop all services
docker-compose -f docker-compose.prod.yml down

# 5. Remove the old ChromaDB container and volume (to ensure clean state)
docker volume rm mealplan_chromadb_data || true

# 6. Rebuild all images
docker-compose -f docker-compose.prod.yml build

# 7. Start all services
docker-compose -f docker-compose.prod.yml up -d

# 8. Initialize ChromaDB with recipe data
docker-compose -f docker-compose.prod.yml exec backend python scripts/load_recipes.py

# 9. Check the logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

## What you should see:

After running these commands, the backend should start successfully and you should see:

```
backend-1  | INFO:     Started server process [1]
backend-1  | INFO:     Waiting for application startup.
backend-1  | INFO:     ChromaDB initialized successfully
backend-1  | INFO:     Application startup complete.
backend-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Note: You should NOT see "Could not connect to a Chroma server" error anymore.

## Final verification:

1. Check all services are running:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

2. Test the application:
   - Frontend: http://162.243.174.187
   - API Docs: http://162.243.174.187/api/docs

3. Test meal plan generation to ensure ChromaDB recipe search is working

## If issues persist:

1. Check ChromaDB container logs:
   ```bash
   docker-compose -f docker-compose.prod.yml logs chromadb
   ```

2. Verify ChromaDB is listening on port 8001:
   ```bash
   docker-compose -f docker-compose.prod.yml exec chromadb netstat -tlnp
   ```

3. Test ChromaDB connection from backend:
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python -c "import chromadb; client = chromadb.HttpClient(host='chromadb', port=8001); print(client.heartbeat())"
   ```