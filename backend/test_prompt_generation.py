#!/usr/bin/env python3
"""
Test script to verify prompt generation with recipes
"""

import asyncio
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.prompt_generator import PromptGenerator
from app.services.recipe_manager import RecipeManager
from app.schemas.meal_plan import NewPatientRequest, Objetivo, Sexo, TipoActividad, NivelEconomico, DistributionType, Frecuencia

def create_test_patient():
    """Create a test patient request"""
    return NewPatientRequest(
        nombre="Test Patient",
        edad=30,
        sexo=Sexo.mujer,
        estatura=165,
        peso=65,
        imc=23.9,
        imc_category="Normal",
        objetivo=Objetivo.mantener,
        tipo_actividad=TipoActividad.sedentario,
        frecuencia_semanal=0,
        duracion_sesion=0,
        patologias="Sin patologías",
        medicacion="Sin medicación",
        suplementacion="Sin suplementación",
        no_consume="",
        le_gusta="",
        antecedentes_personales="",
        antecedentes_familiares="",
        medicacion_detallada="",
        nivel_economico=NivelEconomico.medio,
        almuerzo_transportable=False,
        timing_desayuno="",
        caracteristicas_menu="",
        comidas_principales=4,
        tipo_peso="crudo",
        distribution_type=DistributionType.standard,
        activities=[],
        supplements=[],
        medications=[]
    )

def main():
    """Test prompt generation"""
    print("Testing prompt generation with recipes...")
    
    # Initialize services
    recipe_manager = RecipeManager()
    prompt_generator = PromptGenerator()
    
    # Create test patient
    patient = create_test_patient()
    
    # Get recipes for meal plan
    meal_types = ["desayuno", "almuerzo", "merienda", "cena"]
    recipes_by_meal = recipe_manager.get_recipes_for_meal_plan(
        meal_types=meal_types,
        restrictions=patient.no_consume,
        preferences=patient.le_gusta,
        economic_level=patient.nivel_economico.value,
        daily_macros=None
    )
    
    # Format recipes
    recipes_formatted = prompt_generator.format_recipes_by_meal_type(recipes_by_meal)
    
    print(f"\n✅ Recipes loaded and formatted successfully!")
    print(f"📊 Recipe count by meal type:")
    for meal_type, recipes in recipes_by_meal.items():
        print(f"   - {meal_type}: {len(recipes)} recipes")
    
    # Count total recipes in formatted string
    recipe_count = recipes_formatted.count('[REC_')
    print(f"\n📋 Total recipe references in prompt: {recipe_count}")
    
    # Show a sample of the formatted recipes
    print("\n📝 Sample of formatted recipes:")
    print(recipes_formatted[:1000] + "...")
    
    # Generate prompt
    prompt = prompt_generator.generate_motor1_prompt(
        patient_data=patient,
        recipes_json=recipes_formatted
    )
    
    print(f"\n✅ Prompt generated successfully!")
    print(f"📏 Prompt length: {len(prompt)} characters")
    print(f"🔢 Recipe references in prompt: {prompt.count('[REC_')}")
    
    # Check if recipes are properly placed
    if "CATÁLOGO COMPLETO DE RECETAS DISPONIBLES:" in prompt:
        print("✅ Recipe catalog section found in prompt")
        
        # Find the position of recipes in prompt
        recipe_section_start = prompt.find("CATÁLOGO COMPLETO DE RECETAS DISPONIBLES:")
        recipe_section_end = prompt.find("🔑 CÓMO USAR EL CATÁLOGO:")
        
        if recipe_section_start > 0 and recipe_section_end > recipe_section_start:
            print(f"✅ Recipe section properly positioned at characters {recipe_section_start}-{recipe_section_end}")
        else:
            print("❌ Recipe section positioning issue")
    else:
        print("❌ Recipe catalog section NOT found in prompt")
    
    # Save prompt to file for inspection
    with open("test_prompt_output.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    print("\n💾 Full prompt saved to test_prompt_output.txt for inspection")

if __name__ == "__main__":
    main()