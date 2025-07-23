import chromadb
from chromadb.utils import embedding_functions
import json
import os
import logging
from typing import List, Dict, Optional, Set
from ..config import settings
from ..schemas.meal_plan import NivelEconomico
from ..data.pathologies import (
    detect_pathologies_from_text,
    get_all_dietary_restrictions,
    get_recipe_tags_to_avoid,
    get_recipe_tags_to_prefer,
    get_pregnancy_info
)
from ..utils.pregnancy import PregnancyManager

# Configure logging
logger = logging.getLogger(__name__)

class ChromaDBService:
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedding_function = None
        
        # Ingredientes caros por categoría (del proyecto anterior)
        self.expensive_ingredients = {
            'carnes': ['lomo', 'solomillo', 'bife de chorizo', 'ojo de bife', 'entraña', 
                      'matambre', 'vacío', 'cordero', 'lechón', 'pato', 'conejo'],
            'pescados': ['salmón', 'atún rojo', 'lenguado', 'merluza negra', 'trucha',
                        'langostinos', 'camarones', 'centolla', 'pulpo', 'calamar'],
            'lácteos': ['queso azul', 'queso brie', 'queso camembert', 'queso parmesano',
                       'queso gruyere', 'ricotta', 'queso de cabra'],
            'otros': ['jamón crudo', 'frutos secos', 'aceite de oliva extra virgen',
                     'quinoa', 'chía', 'almendras', 'nueces', 'pistachos', 'anacardos',
                     'espárragos', 'alcachofas', 'hongos shiitake', 'palta']
        }
        
        # Ingredientes económicos (del proyecto anterior)
        self.economic_ingredients = {
            'proteínas': ['pollo', 'huevo', 'lentejas', 'garbanzos', 'porotos', 
                         'carne picada', 'hígado', 'mondongo'],
            'carbohidratos': ['arroz', 'fideos', 'papa', 'batata', 'polenta', 
                            'avena', 'pan', 'harina'],
            'vegetales': ['zanahoria', 'cebolla', 'tomate', 'lechuga', 'zapallo',
                         'zapallito', 'acelga', 'espinaca', 'repollo'],
            'frutas': ['banana', 'manzana', 'naranja', 'mandarina']
        }
        
    def initialize(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Try different connection methods for ChromaDB compatibility
            try:
                # First try with tenant/database (newer ChromaDB versions)
                self.client = chromadb.HttpClient(
                    host=settings.chromadb_host,
                    port=settings.chromadb_port,
                    tenant="default_tenant",
                    database="default_database"
                )
                self.client.heartbeat()
                logger.info("Connected to ChromaDB with tenant/database")
            except:
                try:
                    # Fallback to simple connection (older ChromaDB versions)
                    self.client = chromadb.HttpClient(
                        host=settings.chromadb_host,
                        port=settings.chromadb_port
                    )
                    self.client.heartbeat()
                    logger.info("Connected to ChromaDB with simple connection")
                except:
                    # Try with default settings
                    self.client = chromadb.HttpClient()
                    logger.info("Connected to ChromaDB with default settings")
            
            # Setup embedding function
            self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key=settings.openai_api_key,
                model_name="text-embedding-ada-002"
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="recipes",
                embedding_function=self.embedding_function
            )
            
            # Check if collection is empty and load recipes if needed
            if self.collection.count() == 0:
                self._load_recipes_from_json()
                
            logger.info("ChromaDB initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            logger.warning("App will continue without ChromaDB recipe search")
            # Don't raise - let the app continue without ChromaDB
            self.client = None
            self.collection = None
    
    def _load_recipes_from_json(self):
        """Load recipes from JSON file into ChromaDB"""
        json_path = os.path.join(os.path.dirname(__file__), "../../data/recipes_structured.json")
        
        if not os.path.exists(json_path):
            logger.warning(f"Recipes file not found at {json_path}")
            return
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        documents = []
        metadatas = []
        ids = []
        
        for recipe in data.get('recipes', []):
            # Create searchable text
            ingredients_text = ", ".join([
                f"{ing['cantidad']} de {ing['item']}"
                for ing in recipe.get('ingredientes', [])
            ])
            
            document = f"""
            Receta: {recipe['nombre']}
            Tipo de comida: {', '.join(recipe.get('tipo_comida', []))}
            Ingredientes: {ingredients_text}
            Preparación: {recipe.get('preparacion', '')}
            Información nutricional: {recipe.get('calorias_aprox', 0)} calorías,
            {recipe.get('proteinas_aprox', 0)}g proteínas,
            {recipe.get('carbohidratos_aprox', 0)}g carbohidratos,
            {recipe.get('grasas_aprox', 0)}g grasas
            Apto para: {', '.join(recipe.get('apto_para', []))}
            Tags: {', '.join(recipe.get('tags', []))}
            """
            
            documents.append(document)
            ids.append(recipe['id'])
            metadatas.append({
                "recipe_id": recipe['id'],
                "nombre": recipe['nombre'],
                "tipo_comida": ",".join(recipe.get('tipo_comida', [])),
                "calorias": recipe.get('calorias_aprox', 0),
                "proteinas": recipe.get('proteinas_aprox', 0),
                "carbohidratos": recipe.get('carbohidratos_aprox', 0),
                "grasas": recipe.get('grasas_aprox', 0),
                "tiempo_preparacion": recipe.get('tiempo_preparacion', 0),
                "apto_para": ",".join(recipe.get('apto_para', [])),
                "tags": ",".join(recipe.get('tags', [])),
                "recipe_json": json.dumps(recipe, ensure_ascii=False)
            })
        
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Loaded {len(documents)} recipes into ChromaDB")
    
    def search_recipes(
        self,
        patient_restrictions: Optional[str] = None,
        preferences: Optional[str] = None,
        economic_level: str = "Medio",
        patologias: Optional[str] = None,
        n_results: int = 50
    ) -> str:
        """Search and filter recipes based on patient criteria"""
        
        # If ChromaDB is not available, return empty JSON
        if not self.collection:
            logger.warning("ChromaDB not available, returning empty recipe list")
            return "[]"
        
        # Build query based on preferences
        query_text = ""
        if preferences:
            query_text += f"Recetas con {preferences}. "
        
        # Add economic level considerations
        if economic_level in ["Bajo recursos", "limitado"]:
            query_text += "Recetas económicas con ingredientes accesibles. "
        elif economic_level == "Sin restricciones":
            query_text += "Recetas variadas con ingredientes premium. "
        
        # Detectar patologías y agregar consideraciones
        detected_pathologies = []
        if patologias:
            detected_pathologies = detect_pathologies_from_text(patologias)
            
            # Obtener tags de recetas preferidas
            prefer_tags = get_recipe_tags_to_prefer(detected_pathologies)
            if prefer_tags:
                tag_descriptions = {
                    'bajo_ig': 'bajo índice glucémico',
                    'sin_azucar': 'sin azúcar',
                    'integral': 'integrales',
                    'fibra': 'ricas en fibra',
                    'bajo_sodio': 'bajas en sodio',
                    'potasio': 'ricas en potasio',
                    'facil_digestion': 'fácil digestión',
                    'hierro': 'ricas en hierro',
                    'calcio': 'ricas en calcio',
                    'folato': 'ricas en ácido fólico',
                    'omega3': 'ricas en omega 3'
                }
                
                for tag in prefer_tags:
                    if tag in tag_descriptions:
                        query_text += f"Recetas {tag_descriptions[tag]}. "
            
            # Verificar si hay embarazo
            pregnancy_info = get_pregnancy_info(detected_pathologies)
            if pregnancy_info:
                query_text += "Recetas nutritivas y seguras para embarazo. "
        
        # Search recipes
        results = self.collection.query(
            query_texts=[query_text] if query_text else ["recetas saludables"],
            n_results=n_results
        )
        
        # Filter results based on restrictions
        filtered_recipes = []
        
        for i, metadata in enumerate(results['metadatas'][0]):
            recipe_json = json.loads(metadata['recipe_json'])
            
            # Skip recipe if doesn't pass filters
            if not self._passes_filters(recipe_json, patient_restrictions, 
                                      economic_level, patologias):
                continue
            
            filtered_recipes.append(recipe_json)
        
        # Sort by relevance and variety
        filtered_recipes = self._sort_recipes_by_relevance(
            filtered_recipes, preferences, economic_level
        )
        
        # Format recipes for prompt
        return self._format_recipes_for_prompt(filtered_recipes[:30])
    
    def search_similar_meals(
        self,
        meal_type: str,
        new_meal_description: str,
        target_macros: Dict[str, float],
        tolerance: float = 0.2
    ) -> str:
        """Search for meals with similar macros"""
        
        # Search based on meal type and description
        query = f"Receta para {meal_type} similar a {new_meal_description}"
        
        results = self.collection.query(
            query_texts=[query],
            n_results=30,
            where={"tipo_comida": {"$contains": meal_type}}
        )
        
        # Filter by macro similarity
        similar_recipes = []
        
        for i, metadata in enumerate(results['metadatas'][0]):
            recipe_json = json.loads(metadata['recipe_json'])
            
            # Check if macros are within tolerance
            protein_diff = abs(recipe_json.get('proteinas_aprox', 0) - target_macros['proteinas'])
            carb_diff = abs(recipe_json.get('carbohidratos_aprox', 0) - target_macros['carbohidratos'])
            fat_diff = abs(recipe_json.get('grasas_aprox', 0) - target_macros['grasas'])
            
            # Allow 20% tolerance
            if (protein_diff <= target_macros['proteinas'] * tolerance and
                carb_diff <= target_macros['carbohidratos'] * tolerance and
                fat_diff <= target_macros['grasas'] * tolerance):
                similar_recipes.append(recipe_json)
        
        return self._format_recipes_for_prompt(similar_recipes[:10])
    
    def search_recipes_by_meal_type(
        self,
        meal_types: List[str],
        patient_restrictions: Optional[str] = None,
        preferences: Optional[str] = None,
        economic_level: str = "Medio",
        patologias: Optional[str] = None,
        n_results_per_type: int = 15
    ) -> Dict[str, List[Dict]]:
        """Search recipes organized by meal type"""
        
        # If ChromaDB is not available, return empty dict
        if not self.collection:
            logger.warning("ChromaDB not available, returning empty recipe dict")
            return {}
        
        result = {}
        
        for meal_type in meal_types:
            # Build query for this meal type
            query_text = f"Recetas para {meal_type}"
            if preferences:
                query_text += f" con {preferences}"
            
            # Search with meal type filter
            try:
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results_per_type * 2,  # Get extra to account for filtering
                    where={"tipo_comida": {"$contains": meal_type}}
                )
            except:
                # Fallback if where clause not supported
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results_per_type * 2
                )
            
            # Filter results
            filtered_recipes = []
            
            for i, metadata in enumerate(results['metadatas'][0]):
                recipe_json = json.loads(metadata['recipe_json'])
                
                # Check if recipe is actually for this meal type
                if meal_type not in recipe_json.get('tipo_comida', []):
                    continue
                
                # Skip if doesn't pass filters
                if not self._passes_filters(recipe_json, patient_restrictions, 
                                          economic_level, patologias):
                    continue
                
                filtered_recipes.append(recipe_json)
            
            # Sort by relevance
            filtered_recipes = self._sort_recipes_by_relevance(
                filtered_recipes, preferences, economic_level
            )
            
            # Take top N recipes for this meal type
            result[meal_type] = filtered_recipes[:n_results_per_type]
        
        return result
    
    def get_all_recipes(self) -> str:
        """Get all recipes formatted for prompt"""
        results = self.collection.get()
        
        recipes = []
        for metadata in results['metadatas']:
            recipe_json = json.loads(metadata['recipe_json'])
            recipes.append(recipe_json)
        
        return self._format_recipes_for_prompt(recipes)
    
    def _passes_filters(
        self, 
        recipe: Dict,
        restrictions: Optional[str],
        economic_level: str,
        patologias: Optional[str]
    ) -> bool:
        """Check if recipe passes all filters"""
        
        ingredients = recipe.get('ingredientes', [])
        ingredients_text = " ".join([ing['item'].lower() for ing in ingredients])
        
        # Check dietary restrictions
        if restrictions:
            restriction_list = [r.strip().lower() for r in restrictions.split(',')]
            for restriction in restriction_list:
                if restriction in ingredients_text:
                    return False
        
        # Check economic level
        if economic_level in [NivelEconomico.bajo_recursos.value, NivelEconomico.limitado.value]:
            # Check if contains expensive ingredients
            all_expensive = []
            for category_items in self.expensive_ingredients.values():
                all_expensive.extend(category_items)
            
            for expensive_item in all_expensive:
                if expensive_item.lower() in ingredients_text:
                    return False
        
        # Check pathology-specific restrictions using new structure
        if patologias:
            detected_pathologies = detect_pathologies_from_text(patologias)
            
            # Obtener todas las restricciones dietéticas
            all_restrictions = get_all_dietary_restrictions(detected_pathologies)
            
            # Verificar cada restricción
            for restriction in all_restrictions:
                restriction_lower = restriction.lower()
                
                # Mapeo de restricciones a ingredientes específicos
                restriction_ingredients = {
                    'azúcar refinada': ['azúcar', 'azucar'],
                    'miel': ['miel'],
                    'dulces': ['dulce', 'mermelada', 'chocolate', 'caramelo'],
                    'bebidas azucaradas': ['gaseosa', 'jugo envasado', 'bebida azucarada'],
                    'harinas blancas': ['harina blanca', 'harina 000', 'harina 0000'],
                    'harinas refinadas': ['harina blanca', 'pan blanco', 'galletas'],
                    'alcohol': ['vino', 'cerveza', 'licor', 'alcohol'],
                    'embutidos': ['salame', 'mortadela', 'bondiola', 'jamón crudo'],
                    'sal de mesa': ['sal'],
                    'quesos duros': ['queso parmesano', 'queso reggianito', 'queso sardo'],
                    'lácteos no pasteurizados': ['leche cruda', 'queso artesanal'],
                    'carnes crudas': ['carpaccio', 'steak tartar', 'carne cruda'],
                    'huevos crudos': ['huevo crudo', 'mayonesa casera'],
                    'pescados alto mercurio': ['pez espada', 'tiburón', 'caballa rey'],
                    'gluten': ['harina', 'pan', 'fideos', 'pasta', 'galletas', 'cebada', 'centeno'],
                    'trigo': ['harina de trigo', 'pan', 'pasta', 'galletas'],
                    'soja en exceso': ['soja texturizada', 'leche de soja', 'tofu'],
                    'frituras': ['frito', 'fritura'],
                    'grasas trans': ['margarina', 'grasa vegetal hidrogenada'],
                    'alimentos ultraprocesados': ['snacks', 'galletitas industriales'],
                    'cafeína excesiva': ['café', 'té negro', 'mate', 'bebidas energizantes']
                }
                
                # Verificar si algún ingrediente restringido está presente
                if restriction_lower in restriction_ingredients:
                    for ingredient in restriction_ingredients[restriction_lower]:
                        if ingredient in ingredients_text:
                            return False
                elif restriction_lower in ingredients_text:
                    # Si no hay mapeo específico, buscar la restricción directamente
                    return False
            
            # Verificar tags de recetas a evitar
            avoid_tags = get_recipe_tags_to_avoid(detected_pathologies)
            recipe_tags = [tag.lower() for tag in recipe.get('tags', [])]
            
            for avoid_tag in avoid_tags:
                if avoid_tag in recipe_tags:
                    return False
            
            # Verificaciones especiales para embarazo
            pregnancy_info = get_pregnancy_info(detected_pathologies)
            if pregnancy_info:
                # Lista expandida de alimentos no seguros en embarazo
                unsafe_pregnancy = [
                    'sushi', 'ceviche', 'ostras', 'almejas crudas',
                    'paté', 'foie gras', 'queso azul', 'queso brie',
                    'queso camembert', 'brotes crudos', 'germinados'
                ]
                if any(unsafe in ingredients_text for unsafe in unsafe_pregnancy):
                    return False
        
        return True
    
    def _sort_recipes_by_relevance(
        self,
        recipes: List[Dict],
        preferences: Optional[str],
        economic_level: str
    ) -> List[Dict]:
        """Sort recipes by relevance and variety"""
        
        # Score each recipe
        scored_recipes = []
        for recipe in recipes:
            score = 0
            ingredients_text = " ".join([
                ing['item'].lower() for ing in recipe.get('ingredientes', [])
            ])
            
            # Preference matching
            if preferences:
                pref_list = [p.strip().lower() for p in preferences.split(',')]
                for pref in pref_list:
                    if pref in recipe['nombre'].lower() or pref in ingredients_text:
                        score += 10
            
            # Economic bonus
            if economic_level in [NivelEconomico.bajo_recursos.value, NivelEconomico.limitado.value]:
                # Bonus for economic ingredients
                for category_items in self.economic_ingredients.values():
                    for economic_item in category_items:
                        if economic_item.lower() in ingredients_text:
                            score += 2
            
            # Nutritional balance bonus
            macros = {
                'protein': recipe.get('proteinas_aprox', 0),
                'carbs': recipe.get('carbohidratos_aprox', 0),
                'fats': recipe.get('grasas_aprox', 0)
            }
            if all(m > 0 for m in macros.values()):
                score += 5
            
            scored_recipes.append((score, recipe))
        
        # Sort by score (descending) and return recipes
        scored_recipes.sort(key=lambda x: x[0], reverse=True)
        return [recipe for score, recipe in scored_recipes]
    
    def _format_recipes_for_prompt(self, recipes: List[Dict]) -> str:
        """Format recipes for inclusion in prompt"""
        formatted = []
        
        for recipe in recipes:
            ing_list = "\n  ".join([
                f"- {ing['item']}: {ing['cantidad']}"
                for ing in recipe.get('ingredientes', [])
            ])
            
            formatted.append(f"""
RECETA: {recipe['nombre']}
ID: {recipe['id']}
Tipo: {', '.join(recipe.get('tipo_comida', []))}
Ingredientes:
  {ing_list}
Preparación: {recipe.get('preparacion', '')}
Nutrición: {recipe.get('calorias_aprox', 0)} kcal | P: {recipe.get('proteinas_aprox', 0)}g | C: {recipe.get('carbohidratos_aprox', 0)}g | G: {recipe.get('grasas_aprox', 0)}g
Apto para: {', '.join(recipe.get('apto_para', []))}
Tags: {', '.join(recipe.get('tags', []))}
""")
        
        return "\n".join(formatted)