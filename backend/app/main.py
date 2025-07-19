from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from .config import settings
from .schemas.meal_plan import (
    NewPatientRequest, 
    ControlPatientRequest, 
    MealReplacementRequest,
    MealPlanResponse
)
from .services.chromadb_service import ChromaDBService
from .services.prompt_generator import PromptGenerator
from .services.openai_service import OpenAIService
from .services.pdf_generator import PDFGenerator

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
chromadb_service = ChromaDBService()
prompt_generator = PromptGenerator()
openai_service = OpenAIService()
pdf_generator = PDFGenerator()

@app.on_event("startup")
async def startup_event():
    """Initialize ChromaDB with recipes on startup"""
    try:
        chromadb_service.initialize()
    except Exception as e:
        print(f"Warning: Could not initialize ChromaDB: {e}")

@app.get("/")
async def root():
    return {"message": "Meal Planner API", "version": settings.app_version}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/meal-plans/new-patient", response_model=MealPlanResponse)
async def generate_new_patient_plan(request: NewPatientRequest):
    """Generate meal plan for new patient (Motor 1)"""
    try:
        # Get filtered recipes from ChromaDB
        filtered_recipes = chromadb_service.search_recipes(
            patient_restrictions=request.no_consume,
            preferences=request.le_gusta,
            economic_level=request.nivel_economico.value,
            patologias=request.patologias
        )
        
        # Generate prompt
        prompt = prompt_generator.generate_motor1_prompt(
            patient_data=request,
            recipes_json=filtered_recipes
        )
        
        # Generate plan with OpenAI
        meal_plan = await openai_service.generate_meal_plan(prompt)
        
        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            meal_plan=meal_plan,
            patient_name=request.nombre,
            plan_type="nuevo"
        )
        
        return MealPlanResponse(
            meal_plan=meal_plan,
            pdf_path=pdf_path
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/meal-plans/control", response_model=MealPlanResponse)
async def generate_control_plan(request: ControlPatientRequest):
    """Generate meal plan for patient control (Motor 2)"""
    try:
        # Get recipes from ChromaDB
        recipes = chromadb_service.get_all_recipes()
        
        # Generate prompt
        prompt = prompt_generator.generate_motor2_prompt(
            control_data=request,
            previous_plan=request.plan_anterior,
            recipes_json=recipes
        )
        
        # Generate plan with OpenAI
        meal_plan = await openai_service.generate_meal_plan(prompt)
        
        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            meal_plan=meal_plan,
            patient_name=request.nombre,
            plan_type="control"
        )
        
        return MealPlanResponse(
            meal_plan=meal_plan,
            pdf_path=pdf_path
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/meal-plans/replace-meal", response_model=MealPlanResponse)
async def replace_meal(request: MealReplacementRequest):
    """Replace specific meal maintaining macros (Motor 3)"""
    try:
        # Search for replacement options
        replacement_options = chromadb_service.search_similar_meals(
            meal_type=request.comida_reemplazar,
            new_meal_description=request.nueva_comida,
            target_macros={
                "proteinas": request.proteinas,
                "carbohidratos": request.carbohidratos,
                "grasas": request.grasas,
                "calorias": request.calorias
            }
        )
        
        # Generate prompt
        prompt = prompt_generator.generate_motor3_prompt(
            meal_data=request,
            current_meal=request.comida_actual,
            recipes_json=replacement_options
        )
        
        # Generate replacement with OpenAI
        meal_plan = await openai_service.generate_meal_plan(prompt)
        
        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            meal_plan=meal_plan,
            patient_name=request.paciente,
            plan_type="reemplazo"
        )
        
        return MealPlanResponse(
            meal_plan=meal_plan,
            pdf_path=pdf_path
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/meal-plans/download/{filename}")
async def download_pdf(filename: str):
    """Download generated PDF"""
    pdf_path = f"./generated_pdfs/{filename}"
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=filename
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)