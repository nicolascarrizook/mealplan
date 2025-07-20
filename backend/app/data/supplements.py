# Base de datos de suplementos con información nutricional
# Valores por porción estándar

SUPPLEMENTS_DATABASE = {
    # Proteínas
    "whey_protein": {
        "name": "Proteína Whey",
        "category": "proteinas",
        "serving_size": "30g (1 scoop)",
        "calories": 120,
        "protein": 24,
        "carbs": 3,
        "fats": 1,
        "notes": "Tomar post-entrenamiento o entre comidas"
    },
    "casein_protein": {
        "name": "Proteína Caseína",
        "category": "proteinas",
        "serving_size": "30g (1 scoop)",
        "calories": 110,
        "protein": 24,
        "carbs": 3,
        "fats": 0.5,
        "notes": "Ideal antes de dormir"
    },
    "plant_protein": {
        "name": "Proteína Vegetal",
        "category": "proteinas",
        "serving_size": "30g (1 scoop)",
        "calories": 110,
        "protein": 20,
        "carbs": 4,
        "fats": 2,
        "notes": "Mezcla de proteínas vegetales"
    },
    "egg_protein": {
        "name": "Proteína de Huevo",
        "category": "proteinas",
        "serving_size": "30g (1 scoop)",
        "calories": 115,
        "protein": 23,
        "carbs": 2,
        "fats": 1,
        "notes": "Alternativa sin lácteos"
    },
    
    # Aminoácidos
    "bcaa": {
        "name": "BCAA (Aminoácidos ramificados)",
        "category": "aminoacidos",
        "serving_size": "10g",
        "calories": 40,
        "protein": 10,
        "carbs": 0,
        "fats": 0,
        "notes": "Durante o post-entrenamiento"
    },
    "glutamine": {
        "name": "Glutamina",
        "category": "aminoacidos",
        "serving_size": "5g",
        "calories": 20,
        "protein": 5,
        "carbs": 0,
        "fats": 0,
        "notes": "Post-entrenamiento o antes de dormir"
    },
    "eaa": {
        "name": "EAA (Aminoácidos esenciales)",
        "category": "aminoacidos",
        "serving_size": "15g",
        "calories": 60,
        "protein": 15,
        "carbs": 0,
        "fats": 0,
        "notes": "Durante entrenamiento"
    },
    
    # Creatina
    "creatine_mono": {
        "name": "Creatina Monohidrato",
        "category": "creatina",
        "serving_size": "5g",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "5g diarios, cualquier momento"
    },
    "creatine_hcl": {
        "name": "Creatina HCL",
        "category": "creatina",
        "serving_size": "3g",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "3g diarios, mejor absorción"
    },
    
    # Pre-entrenos
    "pre_workout": {
        "name": "Pre-entreno estándar",
        "category": "pre_entreno",
        "serving_size": "10g",
        "calories": 20,
        "protein": 0,
        "carbs": 5,
        "fats": 0,
        "notes": "30 min antes del entrenamiento"
    },
    "pre_workout_stim_free": {
        "name": "Pre-entreno sin estimulantes",
        "category": "pre_entreno",
        "serving_size": "10g",
        "calories": 15,
        "protein": 0,
        "carbs": 3,
        "fats": 0,
        "notes": "30 min antes, sin cafeína"
    },
    
    # Carbohidratos
    "maltodextrin": {
        "name": "Maltodextrina",
        "category": "carbohidratos",
        "serving_size": "50g",
        "calories": 200,
        "protein": 0,
        "carbs": 50,
        "fats": 0,
        "notes": "Durante o post-entrenamiento"
    },
    "dextrose": {
        "name": "Dextrosa",
        "category": "carbohidratos",
        "serving_size": "50g",
        "calories": 200,
        "protein": 0,
        "carbs": 50,
        "fats": 0,
        "notes": "Post-entrenamiento inmediato"
    },
    "waxy_maize": {
        "name": "Almidón de maíz ceroso",
        "category": "carbohidratos",
        "serving_size": "50g",
        "calories": 200,
        "protein": 0,
        "carbs": 50,
        "fats": 0,
        "notes": "Carbohidrato de rápida absorción"
    },
    
    # Ganadores de peso
    "mass_gainer": {
        "name": "Ganador de peso",
        "category": "ganadores",
        "serving_size": "100g",
        "calories": 380,
        "protein": 30,
        "carbs": 55,
        "fats": 5,
        "notes": "Entre comidas o post-entreno"
    },
    "lean_gainer": {
        "name": "Ganador magro",
        "category": "ganadores",
        "serving_size": "100g",
        "calories": 350,
        "protein": 35,
        "carbs": 45,
        "fats": 3,
        "notes": "Mayor proporción de proteína"
    },
    
    # Quemadores
    "l_carnitine": {
        "name": "L-Carnitina",
        "category": "quemadores",
        "serving_size": "3g",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "En ayunas o pre-cardio"
    },
    "cla": {
        "name": "CLA (Ácido Linoleico Conjugado)",
        "category": "quemadores",
        "serving_size": "3g",
        "calories": 27,
        "protein": 0,
        "carbs": 0,
        "fats": 3,
        "notes": "Con las comidas"
    },
    "thermogenic": {
        "name": "Termogénico",
        "category": "quemadores",
        "serving_size": "1 cápsula",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "En ayunas, no después de 16hs"
    },
    
    # Vitaminas y minerales
    "multivitamin": {
        "name": "Multivitamínico",
        "category": "vitaminas",
        "serving_size": "1 tableta",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Con el desayuno"
    },
    "vitamin_d": {
        "name": "Vitamina D3",
        "category": "vitaminas",
        "serving_size": "1 cápsula",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Con comida que contenga grasa"
    },
    "omega_3": {
        "name": "Omega 3",
        "category": "vitaminas",
        "serving_size": "2 cápsulas",
        "calories": 20,
        "protein": 0,
        "carbs": 0,
        "fats": 2,
        "notes": "Con las comidas"
    },
    "magnesium": {
        "name": "Magnesio",
        "category": "vitaminas",
        "serving_size": "400mg",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Antes de dormir"
    },
    "zinc": {
        "name": "Zinc",
        "category": "vitaminas",
        "serving_size": "15mg",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Con el estómago vacío o antes de dormir"
    },
    
    # Salud digestiva
    "probiotics": {
        "name": "Probióticos",
        "category": "digestivos",
        "serving_size": "1 cápsula",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "En ayunas o antes de dormir"
    },
    "digestive_enzymes": {
        "name": "Enzimas digestivas",
        "category": "digestivos",
        "serving_size": "1 cápsula",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Con comidas pesadas"
    },
    "fiber": {
        "name": "Fibra",
        "category": "digestivos",
        "serving_size": "10g",
        "calories": 20,
        "protein": 0,
        "carbs": 8,
        "fats": 0,
        "notes": "Con abundante agua"
    },
    
    # Otros
    "collagen": {
        "name": "Colágeno",
        "category": "otros",
        "serving_size": "10g",
        "calories": 35,
        "protein": 9,
        "carbs": 0,
        "fats": 0,
        "notes": "En ayunas o antes de dormir"
    },
    "spirulina": {
        "name": "Espirulina",
        "category": "otros",
        "serving_size": "5g",
        "calories": 20,
        "protein": 3,
        "carbs": 1,
        "fats": 0.5,
        "notes": "Con las comidas"
    },
    "mct_oil": {
        "name": "Aceite MCT",
        "category": "otros",
        "serving_size": "15ml",
        "calories": 130,
        "protein": 0,
        "carbs": 0,
        "fats": 14,
        "notes": "En café o batidos"
    }
}

def calculate_supplement_macros(supplements_list: list) -> dict:
    """
    Calcula los macros totales de una lista de suplementos
    
    Args:
        supplements_list: Lista de tuplas (supplement_key, servings)
    
    Returns:
        dict con totales de macros
    """
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fats = 0
    
    for supplement_key, servings in supplements_list:
        if supplement_key in SUPPLEMENTS_DATABASE:
            supp = SUPPLEMENTS_DATABASE[supplement_key]
            total_calories += supp["calories"] * servings
            total_protein += supp["protein"] * servings
            total_carbs += supp["carbs"] * servings
            total_fats += supp["fats"] * servings
    
    return {
        "calories": round(total_calories),
        "protein": round(total_protein),
        "carbs": round(total_carbs),
        "fats": round(total_fats)
    }