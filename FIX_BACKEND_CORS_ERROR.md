# Solución para Error de Backend CORS

## Problema
El backend está fallando con el error:
```
pydantic_settings.sources.SettingsError: error parsing value for field "backend_cors_origins" from source "EnvSettingsSource"
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

Esto significa que la variable `BACKEND_CORS_ORIGINS` está vacía o tiene un formato incorrecto en el archivo `.env`.

## Solución Inmediata

### 1. Verificar el archivo .env actual
```bash
# En tu servidor, ejecuta:
cd /opt/apps/mealplan
cat .env
```

### 2. Crear o actualizar el archivo .env
Si no existe o está incompleto, créalo basándote en `.env.example`:

```bash
# Crear el archivo .env si no existe
cp .env.example .env

# Editar el archivo
nano .env
```

### 3. Configurar las variables correctamente
Asegúrate de que tu archivo `.env` contenga EXACTAMENTE esto (reemplaza con tus valores reales):

```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXX

# Frontend Configuration
VITE_API_URL=http://157.230.67.89

# Backend CORS Settings - IMPORTANTE: Usar comillas dobles y formato JSON válido
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://157.230.67.89"]

# ChromaDB Configuration
CHROMADB_HOST=chromadb
CHROMADB_PORT=8000

# Application Settings
DEBUG=false
```

⚠️ **IMPORTANTE**: 
- `BACKEND_CORS_ORIGINS` debe ser un array JSON válido con comillas dobles
- NO uses comillas simples
- NO dejes espacios extra
- Incluye la IP de tu droplet en la lista

### 4. Reiniciar los servicios
```bash
# Detener los servicios
docker-compose -f docker-compose.prod.yml down

# Volver a construir y levantar
docker-compose -f docker-compose.prod.yml up -d --build

# Ver los logs para verificar que el backend arrancó correctamente
docker-compose -f docker-compose.prod.yml logs backend
```

## Solución Alternativa (Si el problema persiste)

Si continúas teniendo problemas con el formato JSON, puedes usar una lista separada por comas:

```bash
# En .env, usa este formato alternativo:
BACKEND_CORS_ORIGINS=http://localhost:3000,http://157.230.67.89
```

El código en `config.py` ya maneja este formato automáticamente.

## Verificación

Después de reiniciar, verifica que todo esté funcionando:

```bash
# Verificar que todos los servicios estén corriendo
docker-compose -f docker-compose.prod.yml ps

# El backend debe mostrar "Up" y no reiniciarse constantemente
# Deberías ver algo como:
# mealplan-backend-1    Up    8000/tcp
```

## Prevención futura

Para evitar este problema en futuros deployments:

1. **Siempre verifica el .env antes de iniciar**:
   ```bash
   # Verificar que las variables estén configuradas
   grep -E "^(OPENAI_API_KEY|BACKEND_CORS_ORIGINS|VITE_API_URL)" .env
   ```

2. **Usa el script de verificación**:
   ```bash
   # En tu máquina local antes de deployar
   ./verify_deployment.sh
   ```

3. **Documenta tu configuración**:
   Guarda una copia segura de tu `.env` de producción (sin la API key) para referencia futura.

## Si necesitas más ayuda

Si el error persiste después de estos pasos:

1. Verifica que no haya caracteres invisibles en el archivo .env:
   ```bash
   cat -A .env | grep BACKEND_CORS_ORIGINS
   ```

2. Intenta con el valor por defecto más simple:
   ```bash
   BACKEND_CORS_ORIGINS=["*"]
   ```
   (Solo para pruebas, no recomendado para producción)

3. Revisa los logs completos del backend:
   ```bash
   docker-compose -f docker-compose.prod.yml logs --tail=50 backend
   ```