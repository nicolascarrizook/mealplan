# Deploy File Upload Fix Instructions

## Changes Made to Fix 502 Bad Gateway Error

### 1. Updated nginx.conf
- Added `client_max_body_size 10M;` to allow file uploads up to 10MB
- Added proxy timeout settings (300 seconds) for long-running requests
- Added buffer configurations for handling file uploads
- Disabled request buffering for uploads with `proxy_request_buffering off;`

### 2. Updated docker-compose.yml
- Added volume mappings for temp_uploads and generated_pdfs directories:
  ```yaml
  - ./backend/temp_uploads:/app/temp_uploads
  - ./backend/generated_pdfs:/app/generated_pdfs
  ```

### 3. Updated docker-compose.prod.yml
- Added the same volume mappings for production deployment

### 4. Created necessary directories
- Created `backend/temp_uploads/` for temporary file storage
- Created `backend/generated_pdfs/` for generated PDF storage

## Deployment Steps

### For Local Development:
```bash
# Stop current containers
docker-compose down

# Rebuild and start containers
docker-compose up --build

# Or if already built, just restart
docker-compose up -d
```

### For Production Server:
```bash
# SSH into your server
ssh root@tresdiasycarga

# Navigate to project directory
cd /opt/apps/mealplan

# Pull latest changes
git pull origin main

# Stop current containers
docker-compose -f docker-compose.prod.yml down

# Create directories if they don't exist
mkdir -p backend/temp_uploads backend/generated_pdfs

# Rebuild and start containers
docker-compose -f docker-compose.prod.yml up -d --build

# Check logs to ensure everything is running
docker-compose -f docker-compose.prod.yml logs -f
```

## Verification Steps

1. Check that all containers are running:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

2. Test file upload endpoint:
   - Try uploading a PDF, Excel, or image file through the Control form
   - Try downloading the Excel template

3. Check nginx logs if issues persist:
   ```bash
   docker-compose -f docker-compose.prod.yml logs nginx
   ```

4. Check backend logs for any errors:
   ```bash
   docker-compose -f docker-compose.prod.yml logs backend
   ```

## What This Fixes

1. **502 Bad Gateway on File Upload**: Nginx now properly handles file uploads with appropriate size limits and timeouts
2. **File Storage Issues**: Persistent volumes ensure uploaded files and generated PDFs are properly stored
3. **Timeout Issues**: Extended timeouts prevent premature connection closures during processing
4. **Buffer Issues**: Proper buffer configuration handles multipart form data correctly

## Additional Notes

- The file upload limit is set to 10MB. If you need larger files, update `client_max_body_size` in nginx.conf
- Timeout is set to 300 seconds (5 minutes) for long-running operations like Vision AI processing
- Make sure the OPENAI_API_KEY is properly set in your .env file for Vision AI functionality