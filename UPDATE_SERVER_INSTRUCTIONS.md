# Instrucciones para actualizar el servidor

## El error ha sido corregido ✅

He arreglado el error de importación en `calculations.py`. Ahora necesitas ejecutar estos comandos en tu servidor para aplicar los cambios:

```bash
# 1. Conectarte al servidor (si no estás conectado)
ssh root@162.243.174.187

# 2. Ir al directorio del proyecto
cd /opt/apps/mealplan

# 3. Obtener los últimos cambios
git pull origin main

# 4. Reconstruir la imagen del backend
docker-compose -f docker-compose.prod.yml build backend

# 5. Reiniciar los servicios
docker-compose -f docker-compose.prod.yml up -d

# 6. Verificar que el backend esté funcionando
docker-compose -f docker-compose.prod.yml logs -f backend
```

## Qué deberías ver

Después de ejecutar estos comandos, el backend debería arrancar correctamente y verás algo como:

```
backend-1  | INFO:     Started server process [1]
backend-1  | INFO:     Waiting for application startup.
backend-1  | INFO:     Application startup complete.
backend-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Verificación final

Una vez que el backend esté funcionando:

1. Verifica que todos los servicios estén "Up":
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```

2. Prueba acceder a tu aplicación:
   - Frontend: http://162.243.174.187
   - API Docs: http://162.243.174.187/api/docs

## Si aún hay problemas

Si encuentras más errores, ejecuta:
```bash
docker-compose -f docker-compose.prod.yml logs --tail=50
```

Esto mostrará los últimos 50 logs de todos los servicios para ayudar a diagnosticar cualquier problema restante.