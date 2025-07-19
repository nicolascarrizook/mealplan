#!/usr/bin/env python3
"""
Script to load recipes into ChromaDB
Run this after starting ChromaDB container
"""

import json
import chromadb
from chromadb.utils import embedding_functions
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

def load_recipes_to_chromadb():
    """Load recipes from JSON file into ChromaDB"""
    
    # Configuration
    CHROMADB_HOST = os.getenv("CHROMADB_HOST", "localhost")
    CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", 8001))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found in environment variables")
        sys.exit(1)
    
    # Load recipes from JSON
    json_path = os.path.join(os.path.dirname(__file__), "../data/recipes_structured.json")
    
    if not os.path.exists(json_path):
        print(f"Error: recipes file not found at {json_path}")
        print("Please add the recipes_structured.json file to the backend/data/ directory")
        sys.exit(1)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Connect to ChromaDB
    try:
        client = chromadb.HttpClient(
            host=CHROMADB_HOST,
            port=CHROMADB_PORT
        )
        print(f"Connected to ChromaDB at {CHROMADB_HOST}:{CHROMADB_PORT}")
    except Exception as e:
        print(f"Error connecting to ChromaDB: {e}")
        print("Make sure ChromaDB is running (docker-compose up chromadb)")
        sys.exit(1)
    
    # Setup embedding function
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-ada-002"
    )
    
    # Create or get collection
    try:
        # Delete existing collection if it exists
        try:
            client.delete_collection(name="recipes")
            print("Deleted existing recipes collection")
        except:
            pass
        
        collection = client.create_collection(
            name="recipes",
            embedding_function=embedding_function
        )
        print("Created new recipes collection")
    except Exception as e:
        print(f"Error creating collection: {e}")
        sys.exit(1)
    
    # Prepare documents
    documents = []
    metadatas = []
    ids = []
    
    recipes = data.get('recipes', [])
    print(f"Found {len(recipes)} recipes to load")
    
    for recipe in recipes:
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
    
    # Load into ChromaDB in batches
    batch_size = 20
    for i in range(0, len(documents), batch_size):
        batch_end = min(i + batch_size, len(documents))
        
        collection.add(
            documents=documents[i:batch_end],
            metadatas=metadatas[i:batch_end],
            ids=ids[i:batch_end]
        )
        
        print(f"Loaded batch {i//batch_size + 1}/{(len(documents) + batch_size - 1)//batch_size}")
    
    print(f"\n✅ Successfully loaded {len(documents)} recipes into ChromaDB")
    
    # Verify
    count = collection.count()
    print(f"Collection now contains {count} recipes")
    
    # Test query
    print("\nTesting search functionality...")
    results = collection.query(
        query_texts=["desayuno saludable"],
        n_results=3
    )
    
    print(f"Found {len(results['ids'][0])} results for 'desayuno saludable'")
    for i, name in enumerate(results['metadatas'][0]):
        print(f"  - {name['nombre']}")

if __name__ == "__main__":
    load_recipes_to_chromadb()