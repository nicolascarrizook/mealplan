#!/usr/bin/env python3
"""
Script para detectar recetas duplicadas en el archivo recipes_structured.json
"""

import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple

def load_recipes(file_path: str) -> Dict:
    """Cargar el archivo de recetas"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_duplicates_by_id(recipes: List[Dict]) -> Dict[str, List[int]]:
    """Encontrar recetas con IDs duplicados"""
    id_map = defaultdict(list)
    for idx, recipe in enumerate(recipes):
        recipe_id = recipe.get('id', '')
        id_map[recipe_id].append(idx)
    
    # Filtrar solo los IDs duplicados
    duplicates = {k: v for k, v in id_map.items() if len(v) > 1}
    return duplicates

def find_duplicates_by_name(recipes: List[Dict]) -> Dict[str, List[int]]:
    """Encontrar recetas con nombres duplicados o muy similares"""
    name_map = defaultdict(list)
    for idx, recipe in enumerate(recipes):
        name = recipe.get('nombre', '').lower().strip()
        name_map[name].append(idx)
    
    # Filtrar solo los nombres duplicados
    duplicates = {k: v for k, v in name_map.items() if len(v) > 1}
    return duplicates

def find_similar_names(recipes: List[Dict], threshold: float = 0.8) -> List[Tuple[int, int, str, str]]:
    """Encontrar recetas con nombres muy similares"""
    from difflib import SequenceMatcher
    
    similar_pairs = []
    for i in range(len(recipes)):
        for j in range(i + 1, len(recipes)):
            name1 = recipes[i].get('nombre', '')
            name2 = recipes[j].get('nombre', '')
            
            # Calcular similitud
            similarity = SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
            
            if similarity >= threshold and similarity < 1.0:  # No incluir duplicados exactos
                similar_pairs.append((i, j, name1, name2))
    
    return similar_pairs

def analyze_duplicate_content(recipes: List[Dict], indices: List[int]) -> Dict:
    """Analizar el contenido de recetas duplicadas"""
    analysis = {
        'indices': indices,
        'ids': [],
        'names': [],
        'calories': [],
        'ingredients_count': [],
        'meal_types': []
    }
    
    for idx in indices:
        recipe = recipes[idx]
        analysis['ids'].append(recipe.get('id', 'NO_ID'))
        analysis['names'].append(recipe.get('nombre', 'NO_NAME'))
        analysis['calories'].append(recipe.get('calorias_aprox', 0))
        analysis['ingredients_count'].append(len(recipe.get('ingredientes', [])))
        analysis['meal_types'].append(recipe.get('tipo_comida', []))
    
    return analysis

def main():
    # Ruta del archivo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    recipes_path = os.path.join(script_dir, "../data/recipes_structured.json")
    
    if not os.path.exists(recipes_path):
        print(f"Error: No se encontró el archivo en {recipes_path}")
        return
    
    print("🔍 Analizando recetas para detectar duplicados...\n")
    
    # Cargar datos
    data = load_recipes(recipes_path)
    recipes = data.get('recipes', [])
    total_recipes = len(recipes)
    
    print(f"📊 Total de recetas: {total_recipes}\n")
    
    # 1. Buscar duplicados por ID
    print("1️⃣ DUPLICADOS POR ID:")
    print("-" * 50)
    id_duplicates = find_duplicates_by_id(recipes)
    
    if id_duplicates:
        for recipe_id, indices in id_duplicates.items():
            print(f"\n❌ ID duplicado: {recipe_id}")
            analysis = analyze_duplicate_content(recipes, indices)
            for i, idx in enumerate(indices):
                print(f"   Índice {idx}: {analysis['names'][i]} (Cal: {analysis['calories'][i]})")
    else:
        print("✅ No se encontraron IDs duplicados")
    
    # 2. Buscar duplicados por nombre exacto
    print("\n\n2️⃣ DUPLICADOS POR NOMBRE EXACTO:")
    print("-" * 50)
    name_duplicates = find_duplicates_by_name(recipes)
    
    if name_duplicates:
        for name, indices in name_duplicates.items():
            print(f"\n❌ Nombre duplicado: '{name}'")
            analysis = analyze_duplicate_content(recipes, indices)
            for i, idx in enumerate(indices):
                print(f"   Índice {idx}: ID={analysis['ids'][i]} (Cal: {analysis['calories'][i]})")
    else:
        print("✅ No se encontraron nombres exactamente duplicados")
    
    # 3. Buscar nombres similares
    print("\n\n3️⃣ NOMBRES MUY SIMILARES (>80% similitud):")
    print("-" * 50)
    similar_names = find_similar_names(recipes, threshold=0.8)
    
    if similar_names:
        for idx1, idx2, name1, name2 in similar_names[:10]:  # Mostrar solo los primeros 10
            print(f"\n⚠️  Posible duplicado:")
            print(f"   [{idx1}] {name1} (ID: {recipes[idx1].get('id', 'NO_ID')})")
            print(f"   [{idx2}] {name2} (ID: {recipes[idx2].get('id', 'NO_ID')})")
    else:
        print("✅ No se encontraron nombres similares")
    
    # 4. Estadísticas de IDs
    print("\n\n4️⃣ ANÁLISIS DE IDs:")
    print("-" * 50)
    id_counts = defaultdict(int)
    missing_ids = 0
    
    for recipe in recipes:
        recipe_id = recipe.get('id', '')
        if recipe_id:
            prefix = recipe_id.split('_')[0] if '_' in recipe_id else 'OTROS'
            id_counts[prefix] += 1
        else:
            missing_ids += 1
    
    print(f"IDs por prefijo:")
    for prefix, count in sorted(id_counts.items()):
        print(f"   {prefix}: {count} recetas")
    
    if missing_ids > 0:
        print(f"\n❌ Recetas sin ID: {missing_ids}")
    
    # 5. Resumen
    print("\n\n📋 RESUMEN:")
    print("-" * 50)
    total_id_duplicates = sum(len(indices) - 1 for indices in id_duplicates.values())
    total_name_duplicates = sum(len(indices) - 1 for indices in name_duplicates.values())
    
    print(f"Total de recetas con ID duplicado: {total_id_duplicates}")
    print(f"Total de recetas con nombre duplicado: {total_name_duplicates}")
    print(f"Total de pares con nombres similares: {len(similar_names)}")
    
    # Generar reporte de duplicados para eliminar
    if id_duplicates or name_duplicates:
        print("\n\n🗑️  RECETAS RECOMENDADAS PARA ELIMINAR:")
        print("-" * 50)
        indices_to_remove = set()
        
        # Para cada grupo de duplicados, mantener solo el primero
        for indices in id_duplicates.values():
            indices_to_remove.update(indices[1:])  # Eliminar todos menos el primero
        
        for indices in name_duplicates.values():
            # Solo agregar si no está ya marcado por ID duplicado
            for idx in indices[1:]:
                indices_to_remove.add(idx)
        
        print(f"Se recomienda eliminar {len(indices_to_remove)} recetas duplicadas")
        print(f"Índices a eliminar: {sorted(indices_to_remove)}")
        
        # Crear archivo con recetas limpias
        output_path = os.path.join(script_dir, "../data/recipes_cleaned.json")
        cleaned_recipes = [recipe for i, recipe in enumerate(recipes) if i not in indices_to_remove]
        
        cleaned_data = data.copy()
        cleaned_data['recipes'] = cleaned_recipes
        cleaned_data['metadata']['total_recipes'] = len(cleaned_recipes)
        cleaned_data['metadata']['duplicates_removed'] = len(indices_to_remove)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Archivo limpio creado en: {output_path}")
        print(f"   Recetas originales: {total_recipes}")
        print(f"   Recetas después de limpieza: {len(cleaned_recipes)}")

if __name__ == "__main__":
    main()