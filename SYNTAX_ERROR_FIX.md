# Syntax Error Fix for Backend

## Issue
The backend was failing to start with a SyntaxError in `image_extractor.py` on line 187:
```
SyntaxError: invalid syntax
elif current_meal and line and not any(k in line for keywords in meal_keywords.values() for k in keywords):
                                                                                              ^^^^
```

## Root Cause
The nested generator expression had an invalid syntax. The variable `k` was being used but then `keywords` was being referenced instead of `k`.

## Fix Applied
Changed line 187 from:
```python
elif current_meal and line and not any(k in line for keywords in meal_keywords.values() for k in keywords):
```

To:
```python
elif current_meal and line and not any(keyword in line for keywords in meal_keywords.values() for keyword in keywords):
```

## Deployment Steps

1. Pull the latest changes on your server:
   ```bash
   cd /opt/apps/mealplan
   git pull origin main
   ```

2. Rebuild the backend container:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build backend
   ```

3. Verify the backend is running:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   docker-compose -f docker-compose.prod.yml logs backend
   ```

The backend should now start successfully and the file upload functionality should work properly.