import re
import logging
from typing import Dict, List, Optional
from .recipe_manager import RecipeManager

logger = logging.getLogger(__name__)

class MealPlanProcessor:
    def __init__(self, recipe_manager: RecipeManager):
        self.recipe_manager = recipe_manager
    
    def process_meal_plan(self, meal_plan_text: str) -> str:
        """Process a meal plan to ensure recipe details are complete"""
        
        # Find all recipe IDs in the meal plan
        recipe_id_pattern = r'\[REC_\d{4}\]'
        recipe_ids = re.findall(recipe_id_pattern, meal_plan_text)
        
        # Get unique IDs
        unique_ids = list(set([id.strip('[]') for id in recipe_ids]))
        
        # For each unique recipe ID, ensure full details are present
        processed_plan = meal_plan_text
        
        for recipe_id in unique_ids:
            recipe = self.recipe_manager.get_recipe_by_id(recipe_id)
            if recipe:
                # Check if recipe details are missing in the plan
                if not self._has_recipe_details(processed_plan, recipe_id):
                    # Add recipe details after the ID mention
                    recipe_details = self._format_recipe_details(recipe)
                    pattern = f'\\[{recipe_id}\\]'
                    replacement = f'[{recipe_id}] - {recipe["nombre"]}'
                    processed_plan = re.sub(pattern, replacement, processed_plan, count=1)
        
        return processed_plan
    
    def _has_recipe_details(self, meal_plan_text: str, recipe_id: str) -> bool:
        """Check if recipe details are already present in the meal plan"""
        # Simple check for recipe name after ID
        recipe = self.recipe_manager.get_recipe_by_id(recipe_id)
        if recipe and recipe['nombre'] in meal_plan_text:
            return True
        return False
    
    def _format_recipe_details(self, recipe: Dict) -> str:
        """Format recipe details for insertion"""
        return f"{recipe['nombre']}"
    
    def add_recipe_appendix(self, meal_plan_text: str) -> str:
        """Add a recipe appendix with full details of all used recipes"""
        
        # Extract used recipe IDs
        recipe_id_pattern = r'\[REC_\d{4}\]'
        recipe_ids = re.findall(recipe_id_pattern, meal_plan_text)
        unique_ids = list(set([id.strip('[]') for id in recipe_ids]))
        
        if not unique_ids:
            return meal_plan_text
        
        # Create appendix
        appendix = ["\n\n=== DETALLES DE RECETAS UTILIZADAS ===\n"]
        
        for recipe_id in sorted(unique_ids):
            recipe = self.recipe_manager.get_recipe_by_id(recipe_id)
            if recipe:
                appendix.append(self._format_full_recipe(recipe))
        
        return meal_plan_text + "\n".join(appendix)
    
    def _format_full_recipe(self, recipe: Dict) -> str:
        """Format a complete recipe for the appendix"""
        ingredients = "\n  ".join([
            f"• {ing['item']}: {ing['cantidad']}"
            for ing in recipe.get('ingredientes', [])
        ])
        
        return f"""
📋 [{recipe['id']}] {recipe['nombre']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tipo de comida: {', '.join(recipe.get('tipo_comida', []))}
Tiempo de preparación: {recipe.get('tiempo_preparacion', 'No especificado')} minutos
Apto para: {', '.join(recipe.get('apto_para', []))}

INGREDIENTES:
{ingredients}

PREPARACIÓN:
{recipe.get('preparacion', 'No especificada')}

INFORMACIÓN NUTRICIONAL (por porción):
• Calorías: {recipe.get('calorias_aprox', 0)} kcal
• Proteínas: {recipe.get('proteinas_aprox', 0)}g
• Carbohidratos: {recipe.get('carbohidratos_aprox', 0)}g
• Grasas: {recipe.get('grasas_aprox', 0)}g

Tags: {', '.join(recipe.get('tags', []))}
"""
    
    def validate_and_fix_recipes(self, meal_plan_text: str, valid_recipe_ids: List[str]) -> tuple[str, bool]:
        """Validate recipe IDs and attempt to fix invalid ones"""
        
        # Find all recipe IDs in the meal plan
        recipe_id_pattern = r'\[REC_\d{4}\]'
        found_ids = re.findall(recipe_id_pattern, meal_plan_text)
        
        fixed_plan = meal_plan_text
        has_errors = False
        
        for found_id in found_ids:
            clean_id = found_id.strip('[]')
            if clean_id not in valid_recipe_ids:
                has_errors = True
                # Try to find a similar valid recipe
                similar_recipe = self._find_similar_recipe(clean_id, valid_recipe_ids)
                if similar_recipe:
                    fixed_plan = fixed_plan.replace(found_id, f'[{similar_recipe}]')
                    logger.info(f"Fixed invalid recipe ID {clean_id} -> {similar_recipe}")
        
        return fixed_plan, has_errors
    
    def _find_similar_recipe(self, invalid_id: str, valid_ids: List[str]) -> Optional[str]:
        """Try to find a similar valid recipe ID"""
        # Simple strategy: find ID with similar number
        invalid_num = int(invalid_id.split('_')[1])
        
        closest_id = None
        closest_diff = float('inf')
        
        for valid_id in valid_ids:
            valid_num = int(valid_id.split('_')[1])
            diff = abs(valid_num - invalid_num)
            if diff < closest_diff:
                closest_diff = diff
                closest_id = valid_id
        
        return closest_id if closest_diff < 10 else None