# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Meal Planner Pro** application - a web application for generating personalized nutritional meal plans using the "Tres Días y Carga" method. The system creates 3-day meal plans where all days have identical meals to simplify shopping and preparation.

## Tech Stack

- **Backend**: FastAPI (Python 3.11+), OpenAI GPT-4, ChromaDB for recipes, ReportLab for PDFs
- **Frontend**: React 18, TypeScript, Vite, shadcn/ui components, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose, Nginx, DigitalOcean deployment

## Key Architecture

### Three Generation Motors
The application has 3 distinct meal plan generation engines:
1. **Motor 1** (`/api/meal-plans/new-patient`): For new patients - complete plans from scratch
2. **Motor 2** (`/api/meal-plans/control`): For existing patient adjustments based on evolution
3. **Motor 3** (`/api/meal-plans/replace-meal`): For specific meal replacements maintaining macros

### Backend Services Architecture
Located in `backend/app/services/`:
- **chromadb_service.py**: Vector database for recipe search using OpenAI embeddings
- **prompt_generator.py**: Generates optimized prompts with pathology support
- **openai_service.py**: Handles GPT-4 API communication
- **pdf_generator.py**: Creates professional PDF reports using ReportLab
- **meal_plan_processor.py**: Post-processes and validates meal plans
- **recipe_manager.py**: In-memory recipe management and filtering

### Recipe Management System
- 100+ recipes in `backend/data/recipes_structured.json` with unique IDs (REC_XXXX format)
- ChromaDB vector database for semantic search
- Automatic filtering based on dietary restrictions and pathologies
- Optimized prompts using recipe IDs (40% token reduction)
- ChromaDB runs on port 8001 to avoid conflicts

## Common Development Tasks

### Running the Application
```bash
# Full stack with Docker
docker-compose up

# Rebuild after changes
docker-compose up -d --build

# Frontend only (development)
cd frontend
npm run dev

# Backend only (development)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Environment Setup
Create `.env` files:
```bash
# backend/.env
OPENAI_API_KEY=your_key_here
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# .env (root - for Docker)
OPENAI_API_KEY=your_key_here
```

### Database Initialization
```bash
# Initialize ChromaDB with recipes (first time only)
cd backend
python scripts/load_recipes.py

# Or via Docker
docker-compose exec backend python scripts/load_recipes.py
```

### Testing
```bash
# Frontend tests
cd frontend
npm test

# Backend recipe system tests
cd backend
python test_recipe_system.py
python test_recipe_format.py
```

### Deployment
```bash
# Initial server setup
./install-on-droplet.sh

# Deploy updates
./deploy.sh

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Debugging
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f chromadb

# Check service status
docker-compose ps

# Restart services
docker-compose restart backend
```

## Code Patterns and Architecture

### Frontend Patterns
- React with TypeScript and react-hook-form
- shadcn/ui components in `src/components/ui/`
- Zod validation schemas
- Custom LoadingOverlay for loading states
- Toast notifications for user feedback
- API services in `frontend/src/services/`

### Backend Patterns
- FastAPI with Pydantic models
- Service-based architecture (SOA)
- Async operations for all I/O
- Comprehensive error handling with HTTPException
- Environment-based configuration
- ChromaDB initialization on startup

### Data Layer Organization
- **app/data/**: Static data modules (pathologies, medications, activities)
- **app/schemas/**: Pydantic models for validation
- **app/utils/**: Utility functions (calculations, validators)
- **app/services/**: Business logic and external integrations

## Critical Implementation Details

### Meal Plan Generation
- **Core Rule**: All 3 days must have identical meals
- Plans include: breakfast, lunch, dinner, optional snacks/drunch
- Detailed nutritional breakdowns required
- Recipe selection respects all patient restrictions

### Pathology System
- Automatic detection from free text
- 20+ pathologies with nutritional adjustments
- Recipe filtering based on restrictions
- Special pregnancy module with trimester support
- Located in `backend/app/data/pathologies.py`

### PDF Generation
- Professional formatting with logos
- Separate sections for plan and recipes
- Temporary storage only (MVP)
- Uses ReportLab library

### ChromaDB Configuration
- Runs on port 8001 (not 8000)
- Persistent volume for recipe embeddings
- Automatic initialization check on startup
- Fallback to empty list if unavailable

## Troubleshooting

### Common Issues
1. **ChromaDB connection fails**: Check port 8001, run initialization script
2. **CORS errors**: Verify BACKEND_CORS_ORIGINS in `.env`
3. **PDF generation fails**: Check ReportLab dependencies
4. **Recipe search empty**: Verify ChromaDB initialization
5. **Import errors**: Check PYTHONPATH and directory context

### Debug Commands
```bash
# Backend detailed errors
DEBUG=true docker-compose up backend

# Check ChromaDB
docker-compose exec backend python -c "import chromadb; client = chromadb.HttpClient(host='chromadb', port=8001); print(client.heartbeat())"

# Verify recipe count
docker-compose exec backend python scripts/test_recipe_system.py
```

## Important Notes

- The "Tres Días y Carga" method is core - all 3 days MUST be identical
- Nutritional precision is critical - maintain exact macro calculations
- Recipe matching must respect ALL patient restrictions
- No patient data persistence in current MVP
- API keys must use environment variables
- Production requires proper CORS configuration