#!/usr/bin/env python3
"""
Script para migrar las recetas existentes al nuevo formato de etiquetas
compatible con el prompt proporcionado.
"""

import json
import os
import sys
from typing import Dict, List, Set

# Mapeo de tags antiguos a nuevos tags de patología
TAG_MAPPING = {
    # Tags existentes que mapean a nuevas patologías
    "sin_azucar": ["sin_azucar", "hipoglucemia", "diabetes_tipo_1", "diabetes_tipo_2"],
    "sin_gluten": ["sin_gluten", "celiaquia", "anticancer_prequimio", "anticancer_postquimio"],
    "sin_lactosa": ["sin_lactosa", "anticancer_postquimio", "mala_absorcion"],
    "bajo_ig": ["bajo_ig", "hipoglucemia", "diabetes_tipo_1", "diabetes_tipo_2"],
    "integral": ["integral", "fibra", "diabetes_tipo_2"],
    "portable": ["portable", "viandas"],
    "vegetariano": ["vegetariano", "vegano"],
    "proteico": ["alta_proteina", "bariatrico", "anticancer_prequimio"],
    "light": ["bajo_calorias", "bariatrico", "balon_gastrico"],
    "rapido": ["rapido", "facil_preparacion"],
    "economico": ["economico", "bajo_costo"],
    
    # Nuevas etiquetas basadas en el prompt
    "antioxidante": ["antioxidante", "antiinflamatoria"],
    "refrescante": ["refrescante", "verano"],
}

# Mapeo de apto_para a etiquetas de patología
APTO_PARA_MAPPING = {
    "general": [],  # No mapea a ninguna patología específica
    "vegetariano": ["vegetariano", "sin_carne"],
    "vegano": ["vegano", "sin_lactosa", "sin_huevo", "sin_carne"],
    "celiaquia": ["celiaquia", "sin_gluten"],
    "diabetes": ["diabetes_tipo_2", "bajo_ig", "sin_azucar"],
    "hipertension": ["hipertension", "bajo_sodio"],
    "colesterol": ["colesterol_alto", "bajo_grasa_saturada"],
}

# Análisis de contenido para agregar etiquetas automáticamente
INGREDIENT_TAGS = {
    # Ingredientes que indican ciertas características
    "avena": ["fibra", "digestiva", "sin_gluten"],
    "banana": ["potasio", "energia_rapida"],
    "chía": ["omega_3", "fibra", "sin_gluten"],
    "quinoa": ["alta_proteina", "sin_gluten"],
    "pollo": ["alta_proteina", "bajo_grasa"],
    "pescado": ["omega_3", "alta_proteina"],
    "huevo": ["alta_proteina", "con_lactosa"],
    "yogur": ["con_lactosa", "probiotico"],
    "leche": ["con_lactosa"],
    "queso": ["con_lactosa", "alta_proteina"],
    "frutos secos": ["rica_en_grasas_saludables", "alta_densidad_calorica"],
    "aceite de oliva": ["rica_en_grasas_saludables", "antiinflamatoria"],
    "vegetales": ["fibra", "bajo_calorias", "antioxidante"],
    "frutas": ["fibra", "vitaminas", "antioxidante"],
}

# Tipos de comida que indican ciertas características
MEAL_TYPE_TAGS = {
    "desayuno": ["desayuno"],
    "almuerzo": ["almuerzo", "principal"],
    "cena": ["cena", "principal"],
    "merienda": ["merienda", "colacion"],
    "colacion": ["colacion", "snack"],
    "postre": ["postre", "dulce"],
}

def analyze_recipe_content(recipe: Dict) -> Set[str]:
    """Analiza el contenido de la receta para agregar etiquetas automáticamente"""
    new_tags = set()
    
    # Analizar ingredientes
    for ingredient in recipe.get('ingredientes', []):
        item_lower = ingredient['item'].lower()
        for key, tags in INGREDIENT_TAGS.items():
            if key in item_lower:
                new_tags.update(tags)
    
    # Analizar tipo de comida
    for meal_type in recipe.get('tipo_comida', []):
        if meal_type in MEAL_TYPE_TAGS:
            new_tags.update(MEAL_TYPE_TAGS[meal_type])
    
    # Analizar características nutricionales
    calorias = recipe.get('calorias_aprox', 0)
    proteinas = recipe.get('proteinas_aprox', 0)
    carbohidratos = recipe.get('carbohidratos_aprox', 0)
    grasas = recipe.get('grasas_aprox', 0)
    
    # Etiquetas basadas en macros
    if calorias > 0:
        if calorias < 200:
            new_tags.add("bajo_calorias")
        elif calorias > 500:
            new_tags.add("alta_densidad_calorica")
    
    if proteinas > 0:
        protein_percentage = (proteinas * 4) / calorias * 100 if calorias > 0 else 0
        if protein_percentage > 30:
            new_tags.add("alta_proteina")
    
    # Analizar preparación para texturas
    prep_lower = recipe.get('preparacion', '').lower()
    if any(word in prep_lower for word in ['puré', 'pure', 'licuar', 'procesar']):
        new_tags.update(["blanda", "digestiva"])
    if any(word in prep_lower for word in ['horno', 'hornear']):
        new_tags.add("al_horno")
    if any(word in prep_lower for word in ['hervir', 'cocinar', 'vapor']):
        new_tags.update(["cocido", "digestiva"])
    
    # Tiempo de preparación
    tiempo = recipe.get('tiempo_preparacion', 0)
    if tiempo > 0 and tiempo <= 15:
        new_tags.add("rapido")
    
    return new_tags

def migrate_recipe_tags(recipe: Dict) -> Dict:
    """Migra las etiquetas de una receta al nuevo formato"""
    # Mantener una copia de la receta
    migrated = recipe.copy()
    
    # Conjunto para todas las nuevas etiquetas
    all_tags = set()
    
    # Migrar tags existentes
    existing_tags = recipe.get('tags', [])
    for tag in existing_tags:
        if tag in TAG_MAPPING:
            all_tags.update(TAG_MAPPING[tag])
        else:
            all_tags.add(tag)  # Mantener tags no mapeados
    
    # Migrar apto_para
    apto_para = recipe.get('apto_para', [])
    for apt in apto_para:
        if apt in APTO_PARA_MAPPING:
            all_tags.update(APTO_PARA_MAPPING[apt])
    
    # Analizar contenido para agregar más etiquetas
    content_tags = analyze_recipe_content(recipe)
    all_tags.update(content_tags)
    
    # Agregar etiquetas especiales basadas en el nombre
    nombre_lower = recipe['nombre'].lower()
    if 'budín' in nombre_lower or 'budin' in nombre_lower:
        all_tags.update(["blanda", "digestiva", "viandas"])
    if 'batido' in nombre_lower or 'smoothie' in nombre_lower:
        all_tags.update(["liquido", "rapido", "sin_masticacion"])
    if 'ensalada' in nombre_lower:
        all_tags.update(["crudo", "fresco", "bajo_calorias"])
    if 'sopa' in nombre_lower or 'caldo' in nombre_lower:
        all_tags.update(["liquido", "digestiva", "reconfortante"])
    
    # Convertir a lista ordenada y actualizar
    migrated['tags'] = sorted(list(all_tags))
    
    # Mantener apto_para con las patologías principales
    pathology_tags = []
    for tag in all_tags:
        if tag in ['celiaquia', 'diabetes_tipo_1', 'diabetes_tipo_2', 'hipertension',
                   'hipotiroidismo', 'bariatrico', 'balon_gastrico', 'anticancer_prequimio',
                   'anticancer_postquimio', 'anticancer_posrayos', 'blanda', 'digestiva',
                   'mala_absorcion', 'colonoscopia', 'hipoglucemia']:
            pathology_tags.append(tag)
    
    if pathology_tags:
        migrated['apto_patologias'] = sorted(pathology_tags)
    
    return migrated

def main():
    # Ruta del archivo de recetas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    recipes_path = os.path.join(script_dir, "../data/recipes_structured.json")
    backup_path = os.path.join(script_dir, "../data/recipes_structured_backup.json")
    
    # Verificar que el archivo existe
    if not os.path.exists(recipes_path):
        print(f"Error: No se encontró el archivo de recetas en {recipes_path}")
        sys.exit(1)
    
    # Cargar recetas
    print("Cargando recetas...")
    with open(recipes_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Hacer backup
    print(f"Creando backup en {backup_path}...")
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Migrar cada receta
    print("Migrando etiquetas...")
    migrated_recipes = []
    for i, recipe in enumerate(data.get('recipes', [])):
        print(f"  Procesando receta {i+1}/{len(data['recipes'])}: {recipe['nombre']}")
        migrated = migrate_recipe_tags(recipe)
        migrated_recipes.append(migrated)
    
    # Actualizar data
    data['recipes'] = migrated_recipes
    data['metadata']['migration_note'] = "Etiquetas migradas para compatibilidad con nuevo formato de patologías"
    
    # Guardar archivo actualizado
    print(f"Guardando archivo actualizado en {recipes_path}...")
    with open(recipes_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Migración completada exitosamente!")
    print(f"   - {len(migrated_recipes)} recetas procesadas")
    print(f"   - Backup guardado en: {backup_path}")
    
    # Mostrar algunas estadísticas
    all_tags = set()
    for recipe in migrated_recipes:
        all_tags.update(recipe.get('tags', []))
    
    print(f"\n📊 Estadísticas:")
    print(f"   - Total de etiquetas únicas: {len(all_tags)}")
    print(f"   - Etiquetas más comunes:")
    
    tag_count = {}
    for recipe in migrated_recipes:
        for tag in recipe.get('tags', []):
            tag_count[tag] = tag_count.get(tag, 0) + 1
    
    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in sorted_tags:
        print(f"     • {tag}: {count} recetas")

if __name__ == "__main__":
    main()