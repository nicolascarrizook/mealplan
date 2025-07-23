# Solución para Error 502 Bad Gateway

## Problema
El error 502 Bad Gateway ocurre cuando nginx no puede comunicarse con los servicios backend (frontend o API). Los problemas principales eran:

1. **Configuración de red**: Los servicios no estaban en la misma red Docker
2. **Puertos incorrectos**: El frontend estaba mapeado a puerto 3000 pero nginx interno usa puerto 80
3. **Upstream incorrecto**: nginx principal esperaba frontend en puerto 3000 en lugar de 80

## Cambios Realizados

### 1. docker-compose.prod.yml
- ✅ Agregada red `app-network` a todos los servicios
- ✅ Cambiado `ports` por `expose` para servicios internos (solo nginx expone puertos al host)
- ✅ Agregada variable de entorno `BACKEND_CORS_ORIGINS` al backend
- ✅ Mejorado el manejo de `VITE_API_URL` con valor por defecto

### 2. nginx.conf (principal)
- ✅ Actualizado upstream del frontend de `frontend:3000` a `frontend:80`

### 3. Verificaciones
- ✅ Confirmado que el Dockerfile del frontend expone puerto 80
- ✅ Confirmado que nginx del frontend escucha en puerto 80

## Pasos para Aplicar la Solución

### En tu servidor:

1. **Detener los servicios actuales**:
   ```bash
   docker-compose -f docker-compose.prod.yml down
   ```

2. **Actualizar el código**:
   ```bash
   git pull origin main
   ```

3. **Verificar las variables de entorno en .env**:
   ```bash
   # Asegúrate de tener estas variables configuradas:
   OPENAI_API_KEY=tu_api_key
   VITE_API_URL=http://tu-ip-droplet
   BACKEND_CORS_ORIGINS=["http://localhost:3000","http://tu-ip-droplet"]
   ```

4. **Reconstruir y reiniciar servicios**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

5. **Verificar que todos los servicios estén corriendo**:
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   ```
   
   Deberías ver algo así:
   ```
   Name                Command               State   Ports
   ---------------------------------------------------------
   backend     uvicorn app.main:app ...   Up      8000/tcp
   chromadb    /bin/sh -c ...            Up      8000/tcp
   frontend    nginx -g daemon off;       Up      80/tcp
   nginx       nginx -g daemon off;       Up      0.0.0.0:80->80/tcp
   ```

6. **Verificar logs para errores**:
   ```bash
   # Ver logs de todos los servicios
   docker-compose -f docker-compose.prod.yml logs -f
   
   # O logs específicos
   docker-compose -f docker-compose.prod.yml logs nginx
   docker-compose -f docker-compose.prod.yml logs frontend
   docker-compose -f docker-compose.prod.yml logs backend
   ```

7. **Inicializar ChromaDB (si es primera vez)**:
   ```bash
   # Esperar 30 segundos para que ChromaDB esté listo
   sleep 30
   
   # Cargar recetas
   docker-compose -f docker-compose.prod.yml exec backend python scripts/load_recipes.py
   ```

## Troubleshooting Adicional

### Si el error 502 persiste:

1. **Verificar conectividad entre contenedores**:
   ```bash
   # Desde el contenedor de nginx, verificar si puede alcanzar frontend
   docker-compose -f docker-compose.prod.yml exec nginx ping frontend
   docker-compose -f docker-compose.prod.yml exec nginx ping backend
   ```

2. **Verificar que los servicios están escuchando**:
   ```bash
   # Verificar frontend
   docker-compose -f docker-compose.prod.yml exec nginx wget -O- http://frontend:80
   
   # Verificar backend
   docker-compose -f docker-compose.prod.yml exec nginx wget -O- http://backend:8000/api/docs
   ```

3. **Revisar configuración de firewall**:
   ```bash
   # Asegurar que el puerto 80 esté abierto
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw status
   ```

4. **Limpiar y reconstruir todo**:
   ```bash
   # Detener y eliminar todo
   docker-compose -f docker-compose.prod.yml down -v
   
   # Eliminar imágenes antiguas
   docker system prune -a
   
   # Reconstruir desde cero
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

## Verificación Final

Una vez aplicados los cambios:
- Accede a `http://tu-ip-droplet` - Deberías ver la aplicación
- Accede a `http://tu-ip-droplet/api/docs` - Deberías ver la documentación de FastAPI

Si todo funciona correctamente, el error 502 debería estar resuelto. 🎉