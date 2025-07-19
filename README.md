# Meal Planner Pro - Sistema de Planes Nutricionales

Sistema web para generar planes nutricionales personalizados usando el método "Tres Días y Carga | Dieta Inteligente® & Nutrición Evolutiva".

## 🚀 Características

- **3 Motores de Generación**:
  - **Motor 1**: Paciente Nuevo - Plan completo desde cero
  - **Motor 2**: Control de Paciente - Ajustes basados en evolución
  - **Motor 3**: Reemplazo de Comida - Mantiene macros equivalentes

- **Tecnologías**:
  - Backend: FastAPI + Python 3.11
  - Frontend: React 18 + TypeScript + shadcn/ui
  - AI: OpenAI GPT-4
  - Vector DB: ChromaDB para búsqueda de recetas
  - PDF: Generación automática de planes

## 📋 Requisitos Previos

- Docker y Docker Compose instalados
- API Key de OpenAI (GPT-4)
- Archivo `recipes_structured.json` con las recetas

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone [URL_DEL_REPO]
cd apptresdiasycarga
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` y agregar tu API key de OpenAI:
```
OPENAI_API_KEY=tu_api_key_aqui
```

### 3. Agregar archivo de recetas

Coloca el archivo `recipes_structured.json` en:
```
backend/data/recipes_structured.json
```

### 4. Iniciar la aplicación

```bash
docker-compose up -d
```

Esto iniciará:
- Backend en http://localhost:8000
- Frontend en http://localhost:3000
- ChromaDB en http://localhost:8001

### 5. Cargar recetas en ChromaDB

Primera vez solamente:

```bash
# Esperar que ChromaDB esté listo (30 segundos)
sleep 30

# Cargar recetas
docker-compose exec backend python scripts/load_recipes.py
```

## 🖥️ Uso de la Aplicación

1. Abrir http://localhost:3000 en tu navegador
2. Seleccionar el tipo de plan a generar:
   - **Paciente Nuevo**: Completa todos los datos del paciente
   - **Control**: Ingresa evolución y plan anterior
   - **Reemplazo**: Especifica comida y macros a mantener
3. Completar el formulario correspondiente
4. Click en "Generar Plan"
5. Descargar el PDF generado

## 🔧 Comandos Útiles

### Ver logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Reiniciar servicios
```bash
docker-compose restart backend
docker-compose restart frontend
```

### Detener todo
```bash
docker-compose down
```

### Reconstruir después de cambios
```bash
docker-compose up -d --build
```

## 📁 Estructura del Proyecto

```
apptresdiasycarga/
├── backend/
│   ├── app/
│   │   ├── main.py          # API principal
│   │   ├── services/        # Lógica de negocio
│   │   └── schemas/         # Modelos de datos
│   ├── data/
│   │   └── recipes_structured.json
│   └── scripts/
│       └── load_recipes.py
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── services/        # Llamadas API
│   │   └── types/          # TypeScript types
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🚨 Solución de Problemas

### Error de conexión a ChromaDB
```bash
# Verificar que ChromaDB esté corriendo
docker-compose ps
# Reiniciar si es necesario
docker-compose restart chromadb
```

### Error de OpenAI API
- Verificar que la API key sea correcta en `.env`
- Verificar que tengas acceso a GPT-4

### Frontend no se conecta al backend
- Verificar que ambos servicios estén corriendo
- Revisar CORS en la configuración

## 🔐 Seguridad

- **No commits con credenciales**: El `.gitignore` excluye archivos sensibles
- **Variables de entorno**: Todas las credenciales en `.env`
- **Sin persistencia**: Esta versión MVP no guarda datos de pacientes

## 🚀 Deploy en Producción

Para deployar en un droplet o servidor:

1. Configurar las variables de entorno de producción
2. Cambiar `DEBUG=False` en `.env`
3. Configurar un reverse proxy (nginx)
4. Usar `docker-compose -f docker-compose.prod.yml up -d`

## 📝 Notas Importantes

- Esta es una versión MVP sin autenticación ni base de datos de pacientes
- Los planes se generan en tiempo real con GPT-4
- ChromaDB almacena solo las recetas, no información de pacientes
- Los PDFs se generan temporalmente y no se almacenan permanentemente

## 🤝 Soporte

Para problemas o preguntas sobre el sistema, contactar al desarrollador.