# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Meal Planner Pro** application - a web application for generating personalized nutritional meal plans using the "Tres Días y Carga" method. The system creates 3-day meal plans where all days have identical meals to simplify shopping and preparation.

## Tech Stack

- **Backend**: FastAPI (Python 3.11+), OpenAI GPT-4, ChromaDB for recipes, ReportLab for PDFs
- **Frontend**: React 18, TypeScript, Vite, shadcn/ui components, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose, Nginx, DigitalOcean deployment

## Project Structure

```
apptresdiasycarga/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── data/              # Static data modules (pathologies, medications, etc.)
│   │   ├── services/          # Business logic services
│   │   ├── schemas/           # Pydantic models for validation
│   │   ├── utils/             # Utility functions (calculations, validators)
│   │   └── main.py            # FastAPI application entry point
│   ├── data/                  # Recipe data storage
│   │   └── recipes_structured.json
│   ├── scripts/               # Database initialization scripts
│   └── chroma_db/             # ChromaDB persistence directory
├── frontend/                  # React TypeScript frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── forms/         # Form components for each motor
│   │   │   └── ui/            # shadcn/ui components
│   │   ├── services/          # API service layer
│   │   ├── types/             # TypeScript type definitions
│   │   └── utils/             # Frontend utilities
│   └── dist/                  # Build output
├── docker-compose.yml         # Development Docker configuration
├── docker-compose.prod.yml    # Production Docker configuration
├── nginx.conf                 # Nginx reverse proxy configuration
├── install-on-droplet.sh      # Server setup script
└── deploy.sh                  # Deployment update script
```

## Key Architecture

### Three Generation Motors
The application has 3 distinct meal plan generation engines handled by the backend:
1. **Motor 1** (`/api/meal-plans/new`): For new patients
2. **Motor 2** (`/api/meal-plans/control`): For existing patient adjustments  
3. **Motor 3** (`/api/meal-plans/replace`): For specific meal replacements

### Backend Services Architecture
Located in `backend/app/services/`:
- **chromadb_service.py**: Vector database for recipe search and matching
- **prompt_generator.py**: Generates prompts for each motor with pathology support
- **openai_service.py**: Handles GPT-4 API communication
- **pdf_generator.py**: Creates professional PDF reports using ReportLab
- **meal_plan_processor.py**: Post-processes and validates meal plans
- **recipe_manager.py**: Manages recipe loading and formatting

### Recipe Management
- 100+ recipes stored in `backend/data/recipes_structured.json` with unique IDs (REC_XXXX format)
- ChromaDB vector database for intelligent recipe search and matching
- Recipes are embedded using OpenAI embeddings for semantic search
- Automatic filtering based on dietary restrictions and pathologies
- Recipe Manager service provides fast in-memory lookup and filtering
- Optimized prompt format using recipe IDs to reduce token usage by 40%

### API Structure
- Backend: `backend/app/main.py` with FastAPI endpoints for each motor
- Frontend services in `frontend/src/services/` communicate with backend via axios
- Environment-based API configuration (no hardcoded API keys)

## Common Development Tasks

### Running the Application
```bash
# Full stack with Docker
docker-compose up

# Frontend only (development)
cd frontend
npm run dev

# Backend only (development)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Environment Setup
Create `.env` files in both `backend/` and project root:
```bash
# backend/.env
OPENAI_API_KEY=your_key_here
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# .env (root - for Docker)
OPENAI_API_KEY=your_key_here
```

### Testing
```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
python test_recipe_system.py
python test_recipe_format.py
```

### Building for Production
```bash
# Using Docker
docker-compose -f docker-compose.yml up --build

# Manual build
cd frontend && npm run build
```

### Database Initialization
```bash
# Initialize ChromaDB with recipes
cd backend
python scripts/load_recipes.py

# Test recipe system
python test_recipe_system.py
python test_recipe_format.py
```

### Deployment Commands
```bash
# Initial server setup (run on fresh droplet)
./install-on-droplet.sh

# Deploy updates
./deploy.sh
```

## Code Patterns and Guidelines

### Frontend Components
- Use shadcn/ui components from `src/components/ui/`
- Form handling with react-hook-form and zod validation
- Loading states managed through custom LoadingOverlay component
- Consistent error handling with toast notifications

### Backend Patterns
- FastAPI endpoints return standardized responses using Pydantic models
- Service-based architecture with clear separation of concerns
- ChromaDB initialization checks on startup event
- PDF generation uses ReportLab with custom formatting
- Comprehensive error handling with HTTPException
- Environment-based configuration using pydantic-settings

### State Management
- React Query for server state (if implemented)
- Local state with useState/useReducer
- Form state with react-hook-form

## Important Implementation Details

### Meal Plan Generation
- All 3 days in a plan have identical meals
- Plans include: breakfast, lunch, dinner, and optional snacks/drunch
- Each meal has detailed nutritional breakdowns
- Recipe selection based on patient restrictions and preferences

### PDF Generation
- Located in `backend/app/services/pdf_generator.py`
- Includes professional formatting with logos and structured tables
- Separate sections for meal plan and detailed recipes
- Generated PDFs stored temporarily for download

### Recipe Database
- ChromaDB persists data in `backend/chroma_db/`
- Recipes loaded from `backend/data/recipes_structured.json`
- Embedded using OpenAI embeddings for semantic search
- Search considers nutritional requirements, restrictions, and pathologies
- Initialization script: `backend/scripts/load_recipes.py`

## Deployment

The application is deployed on DigitalOcean using Docker:
- Frontend served via Nginx on port 80
- Backend API on port 8000 (proxied through Nginx)
- SSL/TLS configured for production domain
- Automated deployment scripts:
  - `install-on-droplet.sh`: Initial server setup and dependencies
  - `deploy.sh`: Updates and restarts the application
- Production configuration in `docker-compose.prod.yml`

## Pathology and Pregnancy Management

### Pathology System
The application now includes a comprehensive pathology management system:
- **Automatic Detection**: Detects pathologies from free text in the patient's "patologias" field
- **Structured Database**: Located in `backend/app/data/pathologies.py` with 20+ pathologies
- **Nutritional Adjustments**: Automatic calorie and macro adjustments per pathology
- **Recipe Filtering**: Filters recipes based on dietary restrictions and preferences
- **Pregnancy Support**: Full support for all trimesters with specific requirements

### Supported Pathologies
- Diabetes (Type 1 & 2, Gestational)
- Thyroid disorders (Hypo/Hyperthyroidism)
- Cardiovascular (Hypertension, High cholesterol)
- Digestive (Celiac disease, Fatty liver)
- Metabolic (Insulin resistance, PCOS)
- Pregnancy (All trimesters + complications)
- Others (Gout, Anemia, Osteoporosis)

### Pregnancy Module
Special handling for pregnancy with:
- Trimester-specific calorie adjustments (+0/+300/+450 kcal)
- Protein requirements by trimester (1.2/1.4/1.5 g/kg)
- Minimum carbohydrate enforcement (175g/day to prevent ketosis)
- Food safety restrictions (no raw foods, unpasteurized dairy)
- Nausea and reflux management strategies
- Micronutrient requirements (folic acid, iron, calcium)

### Integration Points
1. **Detection**: `detect_pathologies_from_text()` in `backend/app/data/pathologies.py`
2. **Calculations**: Auto-adjustments in `backend/app/utils/calculations.py`
3. **Prompt Generation**: Special sections in `backend/app/services/prompt_generator.py`
4. **Recipe Filtering**: Enhanced filtering in `backend/app/services/chromadb_service.py`
5. **Pregnancy Manager**: Complete module in `backend/app/utils/pregnancy.py`

## Additional Features

### Activity and Medication Management
- **Activity Database** (`backend/app/data/activities.py`): Physical activity factors for TDEE calculations
- **Medication Database** (`backend/app/data/medications.py`): Common medications with dietary interactions
- **Supplement Recommendations** (`backend/app/data/supplements.py`): Pathology-specific supplement suggestions
- **Drug-Nutrient Interactions** (`backend/app/data/interactions.py`): Comprehensive interaction warnings

### Frontend Features
- **Activity Selector**: Dropdown with common physical activities
- **Medication Selector**: Multi-select for patient medications
- **T4 Timing Selector**: Special handling for thyroid medication timing
- **Loading Animations**: Professional medical-themed loading overlays
- **Form Validation**: Comprehensive validation with helpful error messages

## Current Limitations (MVP)

1. No user authentication system
2. No persistent patient data storage
3. No meal plan history tracking
4. Limited to Spanish language
5. No real-time collaboration features

## Future Enhancements to Consider

When implementing new features:
1. **Authentication**: Consider NextAuth.js or FastAPI-Users
2. **Database**: PostgreSQL for patient data persistence
3. **Caching**: Redis for API response caching
4. **Monitoring**: Sentry for error tracking
5. **Analytics**: Patient usage patterns and plan effectiveness

## Troubleshooting

### Common Issues
1. **ChromaDB not initialized**: Run `python scripts/load_recipes.py` from backend directory
2. **CORS errors**: Verify frontend URL in `backend/.env` BACKEND_CORS_ORIGINS
3. **PDF generation fails**: Ensure ReportLab dependencies are installed
4. **Recipe search returns no results**: Check ChromaDB persistence and embeddings
5. **Import errors**: Ensure running from correct directory with proper PYTHONPATH

### Debug Mode
- Frontend: Check browser console for API calls and responses
- Backend: Set `DEBUG=true` in environment for detailed FastAPI errors
- Docker: Use `docker-compose logs -f backend` for real-time logs
- ChromaDB: Check `backend/chroma_db/` directory for persistence files

## AI Assistant Notes

When working with this codebase:
1. The "Tres Días y Carga" method is the core methodology - all 3 days are identical
2. Nutritional calculations are critical - maintain precision in macros
3. Recipe matching must consider patient restrictions carefully
4. PDF formatting follows specific professional standards
5. The UI uses a medical/professional design aesthetic

## Security Considerations

- API keys must never be committed (use environment variables)
- Patient data is not stored persistently (current MVP)
- CORS settings must be updated for production domains
- Input validation is critical for prompt injection prevention
- All user inputs are validated using Pydantic models
- Sensitive operations require proper error handling

## Backend Architecture Details

### Service Layer (`backend/app/services/`)
- **Separation of Concerns**: Each service has a single responsibility
- **Dependency Injection**: Services initialized at app startup
- **Error Handling**: Consistent HTTPException usage across all endpoints
- **Async Operations**: All OpenAI and I/O operations are async

### Data Layer (`backend/app/data/`)
- **pathologies.py**: Comprehensive pathology database with nutritional adjustments
- **activities.py**: Physical activity database for TDEE calculations
- **medications.py**: Medication interactions and considerations
- **supplements.py**: Supplement recommendations by pathology
- **interactions.py**: Drug-nutrient and food-pathology interactions

### Utils Layer (`backend/app/utils/`)
- **calculations.py**: Core nutritional calculations (Harris-Benedict, macro distribution)
- **pregnancy.py**: Specialized pregnancy handling across all trimesters
- **validators.py**: Input validation and sanitization functions