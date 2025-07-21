#!/usr/bin/env python3
"""Test script for the improved recipe system"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.recipe_manager import RecipeManager
from app.services.prompt_generator import PromptGenerator
from app.schemas.meal_plan import NewPatientRequest, Objetivo, Sexo, NivelEconomico, TipoColacion, TipoPeso, DistributionType

def test_recipe_manager():
    """Test the recipe manager functionality"""
    print("=== Testing Recipe Manager ===")
    
    rm = RecipeManager()
    
    # Test 1: Check if recipes loaded
    print(f"\nTotal recipes loaded: {len(rm.recipes_by_id)}")
    
    # Test 2: Get recipes by meal type
    for meal_type in ["desayuno", "almuerzo", "merienda", "cena"]:
        recipes = rm.get_recipes_by_meal_type(meal_type)
        print(f"\nRecipes for {meal_type}: {len(recipes)}")
        if recipes:
            print(f"  Example: {recipes[0]['nombre']} (ID: {recipes[0]['id']})")
    
    # Test 3: Filter recipes by requirements
    print("\n\n=== Testing Recipe Filtering ===")
    
    breakfast_recipes = rm.get_recipes_by_meal_type("desayuno")
    filtered = rm.filter_recipes_by_requirements(
        breakfast_recipes,
        restrictions="lácteos",
        preferences="avena",
        economic_level="Medio"
    )
    
    print(f"\nFiltered breakfast recipes (no dairy, with oats): {len(filtered)}")
    for recipe in filtered[:3]:
        print(f"  - {recipe['nombre']} (Score: {recipe.get('preference_score', 0)})")
    
    # Test 4: Get specific recipe
    print("\n\n=== Testing Recipe Lookup ===")
    recipe = rm.get_recipe_by_id("REC_0001")
    if recipe:
        print(f"Found recipe: {recipe['nombre']}")
        print(f"  Calories: {recipe.get('calorias_aprox', 0)}")
        print(f"  Protein: {recipe.get('proteinas_aprox', 0)}g")
    
    return rm

def test_prompt_generator(rm):
    """Test the prompt generator with new format"""
    print("\n\n=== Testing Prompt Generator ===")
    
    pg = PromptGenerator()
    
    # Create sample recipes by meal type
    recipes_dict = {
        "desayuno": rm.get_recipes_by_meal_type("desayuno")[:5],
        "almuerzo": rm.get_recipes_by_meal_type("almuerzo")[:5],
        "merienda": rm.get_recipes_by_meal_type("merienda")[:5],
        "cena": rm.get_recipes_by_meal_type("cena")[:5]
    }
    
    # Test formatting
    formatted = pg.format_recipes_by_meal_type(recipes_dict)
    print("\nFormatted recipes preview:")
    print(formatted[:500] + "...")
    
    # Test recipe validation
    print("\n\n=== Testing Recipe Validation ===")
    
    # Create a sample meal plan with recipe IDs
    sample_meal_plan = """
PLAN ALIMENTARIO - 3 DÍAS IGUALES

DESAYUNO
- Receta seleccionada: [REC_0001] - Pancakes de banana, avena y miel
- Ingredientes con cantidades ajustadas:
  * banana: 1 unidad
  * avena: 30gr
  * huevo: 1 unidad
  * miel: 1 cdita

ALMUERZO
- Receta seleccionada: [REC_0033] - Wrap de pollo y vegetales
- Ingredientes con cantidades ajustadas:
  * tortilla integral: 1 unidad
  * pollo: 100gr
  * lechuga: 50gr
  * tomate: 1/2 unidad
  * queso crema light: 1 cda

MERIENDA
- Receta seleccionada: [REC_0032] - Muffins de banana y avena
- Ingredientes con cantidades ajustadas:
  * banana: 2 unidades
  * avena: 150gr
  * huevos: 2 unidades

CENA
- Receta seleccionada: [REC_0034] - Salmón al horno con limón
- Ingredientes con cantidades ajustadas:
  * salmón: 150gr
  * limón: 1 unidad
  * ajo: 2 dientes
"""
    
    # Get all valid recipe IDs
    all_recipe_ids = list(rm.recipes_by_id.keys())
    
    # Validate the meal plan
    is_valid = pg.validate_recipe_usage(sample_meal_plan, all_recipe_ids)
    print(f"Meal plan validation: {'PASSED' if is_valid else 'FAILED'}")
    
    # Extract used recipes
    used_recipes = pg.extract_used_recipes(sample_meal_plan)
    print(f"Recipes used in meal plan: {used_recipes}")

def test_meal_plan_processor(rm):
    """Test the meal plan processor"""
    from app.services.meal_plan_processor import MealPlanProcessor
    
    print("\n\n=== Testing Meal Plan Processor ===")
    
    mpp = MealPlanProcessor(rm)
    
    # Sample meal plan
    sample_plan = """
DESAYUNO
- Receta seleccionada: [REC_0001]
- Ingredientes...

ALMUERZO  
- Receta seleccionada: [REC_0033]
- Ingredientes...
"""
    
    # Process the meal plan
    processed = mpp.process_meal_plan(sample_plan)
    print("\nProcessed meal plan preview:")
    print(processed[:300] + "...")
    
    # Add appendix
    with_appendix = mpp.add_recipe_appendix(sample_plan)
    print("\n\nMeal plan with appendix preview:")
    print(with_appendix[-500:])

def main():
    """Run all tests"""
    print("Testing Improved Recipe System\n" + "="*50)
    
    # Test recipe manager
    rm = test_recipe_manager()
    
    # Test prompt generator
    test_prompt_generator(rm)
    
    # Test meal plan processor
    test_meal_plan_processor(rm)
    
    print("\n\n✅ All tests completed!")

if __name__ == "__main__":
    main()