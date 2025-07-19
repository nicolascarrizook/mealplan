import chromadb
from chromadb.utils import embedding_functions
import json
import os
from typing import List, Dict, Optional
from ..config import settings

class ChromaDBService:
    def __init__(self):
        self.client = None
        self.collection = None
        self.embedding_function = None
        
    def initialize(self):
        """Initialize ChromaDB client and collection"""
        try:
            # Connect to ChromaDB
            self.client = chromadb.HttpClient(
                host=settings.chromadb_host,
                port=settings.chromadb_port
            )
            
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
                
        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            raise
    
    def _load_recipes_from_json(self):
        """Load recipes from JSON file into ChromaDB"""
        json_path = os.path.join(os.path.dirname(__file__), "../../data/recipes_structured.json")
        
        if not os.path.exists(json_path):
            print(f"Warning: recipes file not found at {json_path}")
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
            print(f"Loaded {len(documents)} recipes into ChromaDB")
    
    def search_recipes(
        self,
        patient_restrictions: Optional[str] = None,
        preferences: Optional[str] = None,
        economic_level: str = "Medio",
        n_results: int = 50
    ) -> str:
        """Search and filter recipes based on patient criteria"""
        
        # Build query based on preferences
        query_text = ""
        if preferences:
            query_text += f"Recetas con {preferences}. "
        
        # Add economic level considerations
        if economic_level == "Bajo recursos":
            query_text += "Recetas económicas sin ingredientes caros. "
        
        # Search recipes
        results = self.collection.query(
            query_texts=[query_text] if query_text else ["recetas saludables"],
            n_results=n_results
        )
        
        # Filter results based on restrictions
        filtered_recipes = []
        
        for i, metadata in enumerate(results['metadatas'][0]):
            recipe_json = json.loads(metadata['recipe_json'])
            
            # Check restrictions
            if patient_restrictions:
                ingredients_text = " ".join([
                    ing['item'] for ing in recipe_json.get('ingredientes', [])
                ])
                
                # Skip if contains restricted ingredients
                if any(restricted.lower() in ingredients_text.lower() 
                      for restricted in patient_restrictions.split(',')):
                    continue
            
            # Economic filter
            if economic_level == "Bajo recursos":
                expensive_ingredients = ['salmón', 'lomo', 'camarones', 'langostinos', 'trucha']
                ingredients_text = " ".join([
                    ing['item'] for ing in recipe_json.get('ingredientes', [])
                ])
                
                if any(exp in ingredients_text.lower() for exp in expensive_ingredients):
                    continue
            
            filtered_recipes.append(recipe_json)
        
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
    
    def get_all_recipes(self) -> str:
        """Get all recipes formatted for prompt"""
        results = self.collection.get()
        
        recipes = []
        for metadata in results['metadatas']:
            recipe_json = json.loads(metadata['recipe_json'])
            recipes.append(recipe_json)
        
        return self._format_recipes_for_prompt(recipes)
    
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