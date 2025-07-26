from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import logging
import aiofiles
from typing import Dict, Optional
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
from .services.recipe_manager import RecipeManager
from .services.meal_plan_processor import MealPlanProcessor
from .services.file_parser import FileParser

logger = logging.getLogger(__name__)

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
recipe_manager = RecipeManager()
meal_plan_processor = MealPlanProcessor(recipe_manager)
file_parser = FileParser(openai_service=openai_service)

@app.on_event("startup")
async def startup_event():
    """Initialize ChromaDB with recipes on startup"""
    try:
        chromadb_service.initialize()
    except Exception as e:
        logger.warning(f"Could not initialize ChromaDB: {e}")

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
        # Define meal types based on patient configuration
        meal_types = ["desayuno", "almuerzo", "merienda", "cena"]
        
        # Calculate daily macros for recipe filtering
        from .utils.calculations import NutritionalCalculator
        daily_calories = NutritionalCalculator.calculate_daily_calories(request)
        macro_distribution = NutritionalCalculator.calculate_macro_distribution(request)
        
        daily_macros = {
            'protein': round((daily_calories * macro_distribution["proteinas"]) / 4),
            'carbs': round((daily_calories * macro_distribution["carbohidratos"]) / 4),
            'fats': round((daily_calories * macro_distribution["grasas"]) / 9)
        }
        
        # Option 1: Use ChromaDB if available for better semantic search
        recipes_by_meal = None
        if chromadb_service.collection:
            recipes_by_meal = chromadb_service.search_recipes_by_meal_type(
                meal_types=meal_types,
                patient_restrictions=request.no_consume,
                preferences=request.le_gusta,
                economic_level=request.nivel_economico.value,
                patologias=request.patologias,
                n_results_per_type=10
            )
        
        # Option 2: Use Recipe Manager as fallback or primary
        if not recipes_by_meal or all(len(recipes) == 0 for recipes in recipes_by_meal.values()):
            recipes_by_meal = recipe_manager.get_recipes_for_meal_plan(
                meal_types=meal_types,
                restrictions=request.no_consume,
                preferences=request.le_gusta,
                economic_level=request.nivel_economico.value,
                daily_macros=daily_macros
            )
        
        # Format recipes for prompt
        recipes_formatted = prompt_generator.format_recipes_by_meal_type(recipes_by_meal)
        
        # Collect all recipe IDs for validation
        all_recipe_ids = []
        for recipes in recipes_by_meal.values():
            all_recipe_ids.extend([r['id'] for r in recipes])
        
        # Generate prompt with recipe IDs
        prompt = prompt_generator.generate_motor1_prompt(
            patient_data=request,
            recipes_json=recipes_formatted
        )
        
        # Generate plan with OpenAI
        meal_plan = await openai_service.generate_meal_plan(prompt)
        
        # Validate recipe usage
        if not prompt_generator.validate_recipe_usage(meal_plan, all_recipe_ids):
            # If validation fails, retry with stronger prompt
            enhanced_prompt = prompt + "\n\nRECORDATORIO IMPORTANTE: Debes usar ÚNICAMENTE los IDs de recetas proporcionados [REC_XXXX]. NO inventes recetas nuevas."
            meal_plan = await openai_service.generate_meal_plan(enhanced_prompt)
        
        # Extract used recipe IDs for potential post-processing
        used_recipe_ids = prompt_generator.extract_used_recipes(meal_plan)
        
        # Check for zero macros
        zero_macro_warnings = meal_plan_processor.check_for_zero_macros(meal_plan)
        if zero_macro_warnings:
            logger.warning(f"Found {len(zero_macro_warnings)} instances of zero macros")
            for warning in zero_macro_warnings:
                logger.warning(warning)
            
            # Retry with enhanced prompt about macros
            enhanced_prompt = prompt + "\n\n⚠️ RECORDATORIO CRÍTICO SOBRE MACROS:\n- NUNCA dejes macros en cero\n- Si ajustás cantidades, recalculá los macros proporcionalmente\n- Cada opción debe tener valores nutricionales reales basados en la receta"
            meal_plan = await openai_service.generate_meal_plan(enhanced_prompt)
        
        # Post-process meal plan to ensure recipe details are complete
        processed_meal_plan = meal_plan_processor.process_meal_plan(meal_plan)
        
        # Add recipe appendix with full details
        processed_meal_plan = meal_plan_processor.add_recipe_appendix(processed_meal_plan)
        
        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            meal_plan=processed_meal_plan,
            patient_name=request.nombre,
            plan_type="nuevo"
        )
        
        return MealPlanResponse(
            meal_plan=processed_meal_plan,
            pdf_path=pdf_path
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/meal-plans/control", response_model=MealPlanResponse)
async def generate_control_plan(request: ControlPatientRequest):
    """Generate meal plan for patient control (Motor 2)"""
    try:
        # Try to get recipes from ChromaDB first
        recipes_formatted = None
        if chromadb_service.collection:
            recipes_formatted = chromadb_service.get_all_recipes()
        
        # If ChromaDB is not available or returns empty, use RecipeManager
        if not recipes_formatted or recipes_formatted == "No hay recetas disponibles en ChromaDB":
            # Get all recipes from RecipeManager
            all_recipes = recipe_manager.get_all_recipes()
            # Format them for the prompt
            recipes_formatted = prompt_generator.format_recipes_by_meal_type({
                "general": all_recipes[:50]  # Limit to 50 recipes to avoid token limits
            })
        
        # Generate prompt
        prompt = prompt_generator.generate_motor2_prompt(
            control_data=request,
            previous_plan=request.plan_anterior,
            recipes_json=recipes_formatted
        )
        
        # Generate plan with OpenAI
        meal_plan = await openai_service.generate_meal_plan(prompt)
        
        # Post-process meal plan
        processed_meal_plan = meal_plan_processor.process_meal_plan(meal_plan)
        processed_meal_plan = meal_plan_processor.add_recipe_appendix(processed_meal_plan)
        
        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            meal_plan=processed_meal_plan,
            patient_name=request.nombre,
            plan_type="control"
        )
        
        return MealPlanResponse(
            meal_plan=processed_meal_plan,
            pdf_path=pdf_path
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/meal-plans/replace-meal", response_model=MealPlanResponse)
async def replace_meal(request: MealReplacementRequest):
    """Replace specific meal maintaining macros (Motor 3)"""
    try:
        # Search for replacement options
        replacement_options = None
        
        # Try ChromaDB first if available
        if chromadb_service.collection:
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
        
        # If ChromaDB is not available, use RecipeManager
        if not replacement_options:
            # Get recipes for the specific meal type
            meal_type_recipes = recipe_manager.get_recipes_by_meal_type(request.comida_reemplazar)
            # Filter by macros similarity
            filtered_recipes = []
            for recipe in meal_type_recipes:
                # Simple macro similarity check
                protein_diff = abs(recipe.get('proteinas_aprox', 0) - request.proteinas)
                carb_diff = abs(recipe.get('carbohidratos_aprox', 0) - request.carbohidratos)
                fat_diff = abs(recipe.get('grasas_aprox', 0) - request.grasas)
                
                # Allow 20% tolerance
                if (protein_diff <= request.proteinas * 0.2 and
                    carb_diff <= request.carbohidratos * 0.2 and
                    fat_diff <= request.grasas * 0.2):
                    filtered_recipes.append(recipe)
            
            # Format for prompt
            replacement_options = prompt_generator.format_recipes_by_meal_type({
                request.comida_reemplazar: filtered_recipes[:10]
            })
        
        # Generate prompt
        prompt = prompt_generator.generate_motor3_prompt(
            meal_data=request,
            current_meal=request.comida_actual,
            recipes_json=replacement_options
        )
        
        # Generate replacement with OpenAI
        meal_plan = await openai_service.generate_meal_plan(prompt)
        
        # Post-process meal plan
        processed_meal_plan = meal_plan_processor.process_meal_plan(meal_plan)
        processed_meal_plan = meal_plan_processor.add_recipe_appendix(processed_meal_plan)
        
        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            meal_plan=processed_meal_plan,
            patient_name=request.paciente,
            plan_type="reemplazo"
        )
        
        return MealPlanResponse(
            meal_plan=processed_meal_plan,
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

@app.post("/api/meal-plans/control/upload")
async def upload_control_file(
    file: UploadFile = File(...),
    method: Optional[str] = "auto"
):
    """Upload and extract data from control file (PDF, Excel, CSV, or Image)
    
    Args:
        file: The uploaded file
        method: Extraction method for images - 'ocr', 'vision', or 'auto' (default)
    """
    try:
        # Validate file type
        allowed_types = ['pdf', 'xlsx', 'xls', 'csv', 'jpg', 'jpeg', 'png']
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de archivo no soportado. Formatos permitidos: {', '.join(allowed_types)}"
            )
        
        # Validate method parameter
        if method not in ['ocr', 'vision', 'auto']:
            raise HTTPException(
                status_code=400,
                detail="Método inválido. Use 'ocr', 'vision', o 'auto'"
            )
        
        # Create temp directory if it doesn't exist
        temp_dir = "./temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded file temporarily
        temp_path = os.path.join(temp_dir, file.filename)
        
        async with aiofiles.open(temp_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        try:
            # Parse file and extract data with specified method
            if file_extension in ['jpg', 'jpeg', 'png']:
                extracted_data = file_parser.parse_file_with_method(temp_path, file_extension, method)
                extraction_method = "vision" if method == "vision" or (method == "auto" and file_parser.openai_service) else "ocr"
            else:
                extracted_data = file_parser.parse_file(temp_path, file_extension)
                extraction_method = "standard"
            
            # Clean up temp file
            os.remove(temp_path)
            
            return {
                "success": True,
                "data": extracted_data,
                "message": f"Archivo procesado exitosamente usando {extraction_method}",
                "method_used": extraction_method
            }
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing uploaded file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )

@app.get("/api/meal-plans/control/template")
async def download_control_template():
    """Download Excel template for control data"""
    try:
        # Generate template
        template_path = "./generated_pdfs/control_template.xlsx"
        file_parser.generate_excel_template(template_path)
        
        return FileResponse(
            template_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="plantilla_control_pacientes.xlsx"
        )
        
    except Exception as e:
        logger.error(f"Error generating template: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar la plantilla: {str(e)}"
        )

@app.post("/api/meal-plans/control/extract-text")
async def extract_text_from_file(file: UploadFile = File(...)):
    """Extract raw text from uploaded file (for debugging/preview)"""
    try:
        # Validate file type
        allowed_types = ['pdf', 'jpg', 'jpeg', 'png']
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Solo se permite extraer texto de: {', '.join(allowed_types)}"
            )
        
        content = await file.read()
        
        if file_extension == 'pdf':
            # Save temporarily and extract
            temp_path = f"./temp_uploads/{file.filename}"
            os.makedirs("./temp_uploads", exist_ok=True)
            
            with open(temp_path, 'wb') as f:
                f.write(content)
            
            text = file_parser.pdf_extractor.extract_text_from_pdf(temp_path)
            os.remove(temp_path)
            
        else:  # Image
            text = file_parser.image_extractor.extract_text_from_bytes(content)
        
        return {
            "success": True,
            "text": text,
            "length": len(text)
        }
        
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al extraer texto: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)