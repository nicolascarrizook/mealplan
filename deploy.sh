#!/bin/bash

# Script de deployment para Meal Planner Pro

echo "🚀 Iniciando deployment de Meal Planner Pro..."

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}Error: No se encuentra docker-compose.yml${NC}"
    echo "Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que existe .env
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: No se encuentra archivo .env${NC}"
    echo "Copia .env.example a .env y configura las variables"
    exit 1
fi

# Verificar que existe el archivo de recetas
if [ ! -f "backend/data/recipes_structured.json" ]; then
    echo -e "${RED}Error: No se encuentra archivo de recetas${NC}"
    echo "Agrega backend/data/recipes_structured.json antes de continuar"
    exit 1
fi

# Pull últimos cambios
echo "📥 Actualizando código desde Git..."
git pull origin main

# Detener servicios existentes
echo "🛑 Deteniendo servicios anteriores..."
docker-compose -f docker-compose.prod.yml down

# Construir imágenes
echo "🔨 Construyendo imágenes Docker..."
docker-compose -f docker-compose.prod.yml build

# Iniciar servicios
echo "🚀 Iniciando servicios..."
docker-compose -f docker-compose.prod.yml up -d

# Esperar a que ChromaDB esté listo
echo "⏳ Esperando a que ChromaDB esté listo..."
sleep 30

# Cargar recetas en ChromaDB
echo "📚 Cargando recetas en ChromaDB..."
docker-compose -f docker-compose.prod.yml exec -T backend python scripts/load_recipes.py

# Verificar estado de los servicios
echo "✅ Verificando estado de los servicios..."
docker-compose -f docker-compose.prod.yml ps

echo -e "${GREEN}✨ Deployment completado!${NC}"
echo ""
echo "📝 Próximos pasos:"
echo "1. Configurar tu dominio apuntando a la IP del droplet"
echo "2. Actualizar nginx.conf con tu dominio"
echo "3. Configurar SSL con Let's Encrypt"
echo ""
echo "🌐 La aplicación está disponible en:"
echo "   - Frontend: http://tu-ip-droplet"
echo "   - Backend API: http://tu-ip-droplet/api"
echo "   - ChromaDB: http://tu-ip-droplet:8001"