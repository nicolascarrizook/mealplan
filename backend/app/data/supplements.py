# Base de datos de suplementos comunes en Argentina
# IMPORTANTE: Ajustar cada suplemento a peso corporal, objetivo calórico y nivel de entrenamiento

SUPPLEMENTS_DATABASE = {
    # Proteínas
    "whey_protein": {
        "name": "Proteína Whey (Star Nutrition, ENA, UltraTech, Xtrenght)",
        "category": "proteinas",
        "serving_size": "30g (1 scoop)",
        "calories": 120,
        "protein": 24,
        "carbs": 2,
        "fats": 2,
        "notes": "Dosis recomendada: 1.5-2.2 g proteína/kg peso. Se utiliza para completar requerimientos diarios"
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
        "name": "BCAA (Aminoácidos de cadena ramificada)",
        "category": "aminoacidos",
        "serving_size": "5-10g",
        "calories": 40,
        "protein": 10,
        "carbs": 0,
        "fats": 0,
        "notes": "Dosis: 5-10 g/día (formulación 2:1:1). Puede sumarse a proteína total si reemplaza comidas"
    },
    "glutamine": {
        "name": "Glutamina",
        "category": "aminoacidos",
        "serving_size": "5-10g",
        "calories": 30,  # Promedio entre 20-40 kcal
        "protein": 7.5,  # Promedio
        "carbs": 0,
        "fats": 0,
        "notes": "Dosis: 5-10 g/día. No se contabiliza en macros; favorece recuperación y salud digestiva"
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
        "name": "Creatina Monohidratada",
        "category": "creatina",
        "serving_size": "3-5g",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Dosis estándar: 3-5 g/día (independiente del peso). No influye en los macros, se usa para rendimiento"
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
        "name": "Ganador de peso (Mutant Mass, Star Nutrition Gainer)",
        "category": "ganadores",
        "serving_size": "100g",
        "calories": 400,
        "protein": 20,
        "carbs": 65,
        "fats": 7,
        "notes": "Usado en dietas >3000 kcal o déficit de peso corporal. Evaluar tolerancia digestiva"
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
        "name": "Colágeno hidrolizado",
        "category": "otros",
        "serving_size": "10g",
        "calories": 40,
        "protein": 10,
        "carbs": 0,
        "fats": 0,
        "notes": "Dosis: 10 g/día. Sumar al total proteico si se consume habitualmente"
    },
    "cafeina": {
        "name": "Cafeína (pastillas o polvo)",
        "category": "otros",
        "serving_size": "200mg",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Dosis: 3-6 mg/kg peso corporal (ej: 70kg = 210-420mg). Útil como estimulante pre-entreno o ayuno"
    },
    "beta_alanina": {
        "name": "Beta-alanina",
        "category": "otros",
        "serving_size": "3.2-6g",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Dosis: 3.2-6 g/día. Mejora resistencia anaeróbica y muscular"
    },
    "citrulina_malato": {
        "name": "Citrulina Malato (2:1)",
        "category": "otros",
        "serving_size": "6-8g",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "Dosis: 6-8 g pre-entreno. Vasodilatador, mejora el flujo y reduce fatiga"
    },
    "sales_hidratacion": {
        "name": "Sales de hidratación (Hydrate UP, Total Magnesiano, Suero Mix)",
        "category": "otros",
        "serving_size": "1 sobre",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "notes": "No tienen calorías ni macros. Aportan sodio, potasio, cloruro, magnesio. Uso: deportes de resistencia, calor"
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
    },
    
    # Nuevos suplementos con información clínica detallada
    "fiber_supplement": {
        "name": "Fibra Dietaria (Psyllium, Inulina, Salvado de avena)",
        "category": "fibra",
        "serving_size": "5-10g por toma",
        "calories": 20,
        "protein": 0,
        "carbs": 8,
        "fats": 0,
        "dosis_general": "25-30 g/día (mínimo)",
        "dosis_max_single": "10g (con GLP-1)",
        "forms": ["Psyllium", "Inulina", "Salvado de avena"],
        "notes": "Aumentar hidratación 500-1000 mL/día extra",
        "interactions": {
            "levotiroxina": "Separar al menos 4h para no interferir absorción",
            "glp1": "No exceder 10g en una sola ingesta para evitar náuseas"
        },
        "clinical_relevance": True
    },
    "collagen_hydrolyzed": {
        "name": "Colágeno Hidrolizado",
        "category": "proteinas",
        "serving_size": "10g",
        "calories": 35,
        "protein": 9,
        "carbs": 0,
        "fats": 0,
        "dosis_standard": "10 g/día",
        "synergy": "Mejores resultados con 50-100mg vitamina C",
        "benefits": "Mejora articular, elasticidad cutánea y masa magra con entrenamiento",
        "notes": "Compatible con hipotiroidismo, sin interferencia medicamentosa",
        "interactions": {},
        "clinical_relevance": False
    },
    "omega3_epa_dha": {
        "name": "Omega 3 (EPA/DHA)",
        "category": "grasas",
        "serving_size": "1000-3000mg aceite de pescado",
        "calories": 10,
        "protein": 0,
        "carbs": 0,
        "fats": 1,
        "dosis_general": "1-2g EPA+DHA/día",
        "dosis_max": "3-4g/día (bajo supervisión)",
        "benefits": "Mejora perfil lipídico y sensibilidad hormona tiroidea",
        "notes": "En dislipidemias o inflamación crónica hasta 3-4g/día",
        "interactions": {
            "levotiroxina": "Separar 1h de la toma"
        },
        "clinical_relevance": True
    },
    "magnesium_supplement": {
        "name": "Magnesio (Citrato, Bisglicinato, Malato)",
        "category": "minerales",
        "serving_size": "300-400mg",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "dosis_general": "300-400 mg/día",
        "forms": ["Citrato", "Bisglicinato", "Malato"],
        "avoid_forms": ["Óxido"],
        "benefits": "Mejora sueño, función muscular, tránsito intestinal",
        "notes": "Frecuente déficit en hipotiroidismo. Útil en constipación/calambres",
        "interactions": {
            "levotiroxina": "Separar 4h"
        },
        "clinical_relevance": True
    },
    "vitamin_c_supplement": {
        "name": "Vitamina C",
        "category": "vitaminas",
        "serving_size": "500-1000mg",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "dosis_standard": "500-1000 mg/día",
        "dosis_max_tolerable": "2000mg (puede causar diarrea)",
        "benefits": "Antioxidante, soporte inmunológico, mejora absorción hierro no hemo",
        "synergy": "Potencia efecto del colágeno",
        "notes": "No tóxica en altas dosis",
        "interactions": {},
        "clinical_relevance": False
    },
    "vitamin_d3_k2": {
        "name": "Vitamina D3 + K2",
        "category": "vitaminas",
        "serving_size": "D3: 2000-4000 UI + K2: 90-180 mcg",
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fats": 0,
        "dosis_d3": "2000-4000 UI/día",
        "dosis_k2": "90-180 mcg/día (menaquinona-7)",
        "benefits": "Mejora salud ósea y distribución del calcio",
        "notes": "Frecuente déficit en hipotiroidismo, especialmente Hashimoto. Evaluar niveles séricos",
        "interactions": {},
        "clinical_relevance": True
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