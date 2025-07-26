import json
import os
import logging
from typing import Dict, List, Optional, Tuple
from ..schemas.meal_plan import NivelEconomico

logger = logging.getLogger(__name__)

class RecipeManager:
    def __init__(self):
        self.recipes_by_id: Dict[str, Dict] = {}
        self.recipes_by_meal_type: Dict[str, List[Dict]] = {
            "desayuno": [],
            "almuerzo": [],
            "merienda": [],
            "cena": [],
            "colacion": []
        }
        self._load_recipes()
    
    def _load_recipes(self):
        """Load recipes from JSON file into memory for quick access"""
        json_path = os.path.join(os.path.dirname(__file__), "../../data/recipes_structured.json")
        
        if not os.path.exists(json_path):
            logger.warning(f"Recipes file not found at {json_path}")
            return
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for recipe in data.get('recipes', []):
            # Store by ID for quick lookup
            self.recipes_by_id[recipe['id']] = recipe
            
            # Store by meal type for filtering
            for meal_type in recipe.get('tipo_comida', []):
                if meal_type in self.recipes_by_meal_type:
                    self.recipes_by_meal_type[meal_type].append(recipe)
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict]:
        """Get a specific recipe by its ID"""
        return self.recipes_by_id.get(recipe_id)
    
    def get_recipes_by_meal_type(self, meal_type: str) -> List[Dict]:
        """Get all recipes for a specific meal type"""
        return self.recipes_by_meal_type.get(meal_type, [])
    
    def get_all_recipes(self) -> List[Dict]:
        """Get all recipes from all meal types"""
        all_recipes = []
        for meal_type_recipes in self.recipes_by_meal_type.values():
            all_recipes.extend(meal_type_recipes)
        return all_recipes
    
    def filter_recipes_by_pathology_tags(
        self,
        recipes: List[Dict],
        tags_to_prefer: List[str],
        tags_to_avoid: List[str]
    ) -> List[Dict]:
        """Filter recipes based on pathology tags (new format)"""
        filtered = []
        
        for recipe in recipes:
            recipe_tags = recipe.get('tags', [])
            recipe_apto_para = recipe.get('apto_para', [])
            
            # Combine all tags for checking
            all_recipe_tags = set(recipe_tags + recipe_apto_para)
            
            # Check if recipe has any tags to avoid
            if tags_to_avoid and any(tag in all_recipe_tags for tag in tags_to_avoid):
                continue
            
            # Calculate preference score based on preferred tags
            preference_score = 0
            if tags_to_prefer:
                for tag in tags_to_prefer:
                    if tag in all_recipe_tags:
                        preference_score += 10
            
            recipe['pathology_score'] = preference_score
            filtered.append(recipe)
        
        # Sort by pathology score
        filtered.sort(key=lambda x: x.get('pathology_score', 0), reverse=True)
        
        return filtered

    def filter_recipes_by_requirements(
        self,
        recipes: List[Dict],
        restrictions: Optional[str] = None,
        preferences: Optional[str] = None,
        economic_level: str = "Medio",
        target_macros: Optional[Dict[str, float]] = None,
        tags_to_prefer: Optional[List[str]] = None,
        tags_to_avoid: Optional[List[str]] = None
    ) -> List[Dict]:
        """Filter recipes based on patient requirements"""
        filtered = []
        
        # Expensive ingredients to avoid for limited budgets
        expensive_ingredients = [
            'salmón', 'atún rojo', 'lomo', 'bife de chorizo', 'langostinos',
            'queso azul', 'queso brie', 'jamón crudo', 'frutos secos', 'quinoa'
        ]
        
        for recipe in recipes:
            # Check restrictions
            if restrictions and self._contains_restricted_ingredients(recipe, restrictions):
                continue
            
            # Check pathology tags to avoid
            if tags_to_avoid:
                recipe_tags = recipe.get('tags', []) + recipe.get('apto_para', [])
                if any(tag in recipe_tags for tag in tags_to_avoid):
                    continue
            
            # Check economic level
            if economic_level in [NivelEconomico.bajo_recursos.value, NivelEconomico.limitado.value]:
                if self._contains_expensive_ingredients(recipe, expensive_ingredients):
                    continue
            
            # Score by preferences
            score = self._calculate_preference_score(recipe, preferences)
            recipe['preference_score'] = score
            
            # Score by pathology tags
            if tags_to_prefer:
                pathology_score = 0
                recipe_tags = recipe.get('tags', []) + recipe.get('apto_para', [])
                for tag in tags_to_prefer:
                    if tag in recipe_tags:
                        pathology_score += 10
                recipe['pathology_score'] = pathology_score
                score += pathology_score
            
            # If target macros provided, calculate macro similarity
            if target_macros:
                macro_score = self._calculate_macro_similarity(recipe, target_macros)
                recipe['macro_score'] = macro_score
            
            recipe['total_score'] = score
            filtered.append(recipe)
        
        # Sort by total score
        filtered.sort(key=lambda x: x.get('total_score', 0), reverse=True)
        
        return filtered
    
    def _contains_restricted_ingredients(self, recipe: Dict, restrictions: str) -> bool:
        """Check if recipe contains restricted ingredients"""
        if not restrictions:
            return False
            
        restriction_list = [r.strip().lower() for r in restrictions.split(',')]
        ingredients_text = " ".join([
            ing['item'].lower() for ing in recipe.get('ingredientes', [])
        ])
        
        return any(restriction in ingredients_text for restriction in restriction_list)
    
    def _contains_expensive_ingredients(self, recipe: Dict, expensive_list: List[str]) -> bool:
        """Check if recipe contains expensive ingredients"""
        ingredients_text = " ".join([
            ing['item'].lower() for ing in recipe.get('ingredientes', [])
        ])
        
        return any(expensive in ingredients_text for expensive in expensive_list)
    
    def _calculate_preference_score(self, recipe: Dict, preferences: Optional[str]) -> float:
        """Calculate how well a recipe matches preferences"""
        if not preferences:
            return 0.0
            
        score = 0.0
        pref_list = [p.strip().lower() for p in preferences.split(',')]
        
        # Check recipe name
        recipe_name_lower = recipe['nombre'].lower()
        for pref in pref_list:
            if pref in recipe_name_lower:
                score += 5.0
        
        # Check ingredients
        ingredients_text = " ".join([
            ing['item'].lower() for ing in recipe.get('ingredientes', [])
        ])
        for pref in pref_list:
            if pref in ingredients_text:
                score += 2.0
        
        return score
    
    def _calculate_macro_similarity(self, recipe: Dict, target_macros: Dict[str, float]) -> float:
        """Calculate how similar recipe macros are to target"""
        recipe_macros = {
            'proteinas': recipe.get('proteinas_aprox', 0),
            'carbohidratos': recipe.get('carbohidratos_aprox', 0),
            'grasas': recipe.get('grasas_aprox', 0)
        }
        
        # Calculate percentage difference for each macro
        differences = []
        for macro, target_value in target_macros.items():
            if target_value > 0:
                recipe_value = recipe_macros.get(macro, 0)
                diff = abs(recipe_value - target_value) / target_value
                differences.append(diff)
        
        # Convert to similarity score (0-100)
        avg_diff = sum(differences) / len(differences) if differences else 0
        similarity = max(0, 100 - (avg_diff * 100))
        
        return similarity
    
    def format_recipe_summary(self, recipe_id: str) -> str:
        """Format a recipe summary for inclusion in prompts"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return f"Recipe {recipe_id} not found"
        
        return (
            f"ID: {recipe['id']} | {recipe['nombre']} | "
            f"Cal: {recipe.get('calorias_aprox', 0)} | "
            f"P: {recipe.get('proteinas_aprox', 0)}g | "
            f"C: {recipe.get('carbohidratos_aprox', 0)}g | "
            f"G: {recipe.get('grasas_aprox', 0)}g"
        )
    
    def format_recipe_full(self, recipe_id: str) -> str:
        """Format full recipe details"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return f"Recipe {recipe_id} not found"
        
        ingredients = "\n  ".join([
            f"- {ing['item']}: {ing['cantidad']}"
            for ing in recipe.get('ingredientes', [])
        ])
        
        return f"""
RECETA: {recipe['nombre']} (ID: {recipe['id']})
Ingredientes:
  {ingredients}
Preparación: {recipe.get('preparacion', '')}
Nutrición: {recipe.get('calorias_aprox', 0)} kcal | P: {recipe.get('proteinas_aprox', 0)}g | C: {recipe.get('carbohidratos_aprox', 0)}g | G: {recipe.get('grasas_aprox', 0)}g
"""
    
    def get_recipes_for_meal_plan(
        self,
        meal_types: List[str],
        restrictions: Optional[str] = None,
        preferences: Optional[str] = None,
        economic_level: str = "Medio",
        daily_macros: Optional[Dict[str, float]] = None
    ) -> Dict[str, List[Dict]]:
        """Get filtered recipes organized by meal type for meal planning"""
        result = {}
        
        # Calculate target macros per meal if daily macros provided
        meal_target_macros = None
        if daily_macros and len(meal_types) > 0:
            meal_target_macros = {
                'proteinas': daily_macros.get('protein', 0) / len(meal_types),
                'carbohidratos': daily_macros.get('carbs', 0) / len(meal_types),
                'grasas': daily_macros.get('fats', 0) / len(meal_types)
            }
        
        for meal_type in meal_types:
            # Get recipes for this meal type
            recipes = self.get_recipes_by_meal_type(meal_type)
            
            # Filter by requirements
            filtered = self.filter_recipes_by_requirements(
                recipes,
                restrictions=restrictions,
                preferences=preferences,
                economic_level=economic_level,
                target_macros=meal_target_macros
            )
            
            # Take top 10 recipes for each meal type
            result[meal_type] = filtered[:10]
        
        return result