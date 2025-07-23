# Deployment Checklist - Meal Planner Pro

## Pre-Deployment Verification

### ✅ Cambios realizados en esta sesión:
- [x] Creado `.env.example` con todas las variables necesarias
- [x] Actualizada configuración de CORS para soportar variables de entorno
- [x] Cambiado `debug=False` por defecto en `backend/app/config.py`
- [x] Eliminado archivo de test con console.logs (`test-interactions.ts`)
- [x] Reemplazados todos los `print()` con `logging` apropiado en backend
- [x] Actualizado `nginx.conf` para deployment inicial sin SSL
- [x] Creado script `verify_deployment.sh` para validación pre-deploy

### 📋 Antes de subir al droplet:

1. **Crear archivo `.env` en el servidor basado en `.env.example`**:
   ```bash
   cp .env.example .env
   # Editar .env y agregar:
   # - Tu OPENAI_API_KEY real
   # - La IP de tu droplet en BACKEND_CORS_ORIGINS y VITE_API_URL
   ```

2. **Actualizar `docker-compose.prod.yml`**:
   - Línea 22: Cambiar `VITE_API_URL=http://tu-dominio.com` por tu IP/dominio real

3. **Verificar localmente**:
   ```bash
   ./verify_deployment.sh
   ```

## Pasos de Deployment

### 1. Preparación del servidor (Primera vez)
```bash
# Conectar al droplet
ssh root@your-droplet-ip

# Clonar repositorio
git clone https://github.com/tu-usuario/apptresdiasycarga.git
cd apptresdiasycarga

# Ejecutar script de instalación
chmod +x install-on-droplet.sh
./install-on-droplet.sh
```

### 2. Configuración
```bash
# Crear y configurar .env
cp .env.example .env
nano .env  # Agregar tu OPENAI_API_KEY y actualizar URLs

# Actualizar docker-compose.prod.yml
nano docker-compose.prod.yml  # Actualizar VITE_API_URL
```

### 3. Deploy inicial
```bash
# Construir y lanzar servicios
docker-compose -f docker-compose.prod.yml up -d --build

# Verificar que todo esté corriendo
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 4. Inicializar ChromaDB
```bash
# Esperar a que ChromaDB esté listo (30 segundos)
sleep 30

# Cargar recetas
docker-compose -f docker-compose.prod.yml exec backend python scripts/load_recipes.py
```

### 5. Verificación
- Acceder a `http://your-droplet-ip` - Debería mostrar la aplicación
- Acceder a `http://your-droplet-ip/api/docs` - Debería mostrar la documentación de FastAPI
- Probar generación de un plan de comidas

## Updates posteriores

Para actualizar la aplicación después del deployment inicial:
```bash
./deploy.sh
```

## Configuración SSL (Opcional)

Una vez que tengas un dominio:

1. Actualizar `nginx.conf` con tu dominio
2. Instalar certbot:
   ```bash
   apt-get update
   apt-get install certbot python3-certbot-nginx
   ```
3. Obtener certificado:
   ```bash
   certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
   ```
4. Descomentar la configuración HTTPS en `nginx.conf`
5. Reiniciar nginx:
   ```bash
   docker-compose -f docker-compose.prod.yml restart nginx
   ```

## Troubleshooting

### ChromaDB no se conecta
- Verificar que el servicio esté corriendo: `docker ps`
- Revisar logs: `docker-compose logs chromadb`
- Asegurar que el puerto interno sea 8000 (no 8001)

### CORS errors
- Verificar que la IP/dominio esté en BACKEND_CORS_ORIGINS
- Reiniciar backend después de cambios en .env

### PDF generation fails
- Verificar que el directorio `/app/pdfs` exista en el container
- Revisar permisos de escritura

### API no responde
- Verificar nginx proxy configuration
- Revisar logs del backend: `docker-compose logs backend`

## Monitoreo

Comandos útiles para monitorear la aplicación:
```bash
# Ver estado de servicios
docker-compose -f docker-compose.prod.yml ps

# Ver logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f

# Ver uso de recursos
docker stats

# Entrar a un container
docker-compose -f docker-compose.prod.yml exec backend bash
```