# Base de datos de medicamentos comunes y su impacto nutricional

MEDICATIONS_DATABASE = {
    # Antidiabéticos
    "metformina": {
        "name": "Metformina",
        "category": "antidiabeticos",
        "nutritional_impact": "Puede reducir absorción de B12, puede causar pérdida de peso",
        "considerations": "Tomar con comidas para reducir molestias GI"
    },
    "insulina": {
        "name": "Insulina",
        "category": "antidiabeticos",
        "nutritional_impact": "Puede aumentar el apetito y peso",
        "considerations": "Ajustar carbohidratos según dosis"
    },
    
    # Hipertensión
    "enalapril": {
        "name": "Enalapril",
        "category": "antihipertensivos",
        "nutritional_impact": "Puede aumentar potasio",
        "considerations": "Limitar alimentos ricos en potasio"
    },
    "amlodipina": {
        "name": "Amlodipina",
        "category": "antihipertensivos",
        "nutritional_impact": "Puede causar edema",
        "considerations": "Reducir sodio"
    },
    "hidroclorotiazida": {
        "name": "Hidroclorotiazida",
        "category": "diureticos",
        "nutritional_impact": "Pérdida de potasio y magnesio",
        "considerations": "Aumentar ingesta de K y Mg"
    },
    "furosemida": {
        "name": "Furosemida",
        "category": "diureticos",
        "nutritional_impact": "Pérdida de electrolitos",
        "considerations": "Monitorear electrolitos"
    },
    
    # Estatinas
    "atorvastatina": {
        "name": "Atorvastatina",
        "category": "estatinas",
        "nutritional_impact": "Puede reducir CoQ10",
        "considerations": "Evitar pomelo"
    },
    "simvastatina": {
        "name": "Simvastatina",
        "category": "estatinas",
        "nutritional_impact": "Puede reducir CoQ10",
        "considerations": "Evitar pomelo, tomar por la noche"
    },
    "rosuvastatina": {
        "name": "Rosuvastatina",
        "category": "estatinas",
        "nutritional_impact": "Puede reducir CoQ10",
        "considerations": "Se puede tomar a cualquier hora"
    },
    "estatinas": {
        "name": "Estatinas (genérico)",
        "category": "estatinas",
        "nutritional_impact": "Puede reducir CoQ10, control del colesterol",
        "considerations": "Evitar pomelo, considerar suplementación con CoQ10"
    },
    
    # Tiroides
    "levotiroxina": {
        "name": "Levotiroxina",
        "category": "tiroides",
        "nutritional_impact": "Mejora metabolismo",
        "considerations": "Tomar en ayunas, evitar soja y calcio 4h"
    },
    "t4": {
        "name": "T4 (Levotiroxina)",
        "category": "tiroides",
        "nutritional_impact": "Mejora metabolismo, puede afectar peso",
        "considerations": "Tomar en ayunas 30-60 min antes del desayuno, evitar café, soja y calcio por 4h"
    },
    "levotiroxina_75": {
        "name": "Levotiroxina T4 75mg",
        "category": "tiroides",
        "nutritional_impact": "Mejora metabolismo, normaliza función tiroidea",
        "considerations": "Tomar en ayunas, separar de suplementos de calcio y hierro"
    },
    "metimazol": {
        "name": "Metimazol",
        "category": "tiroides",
        "nutritional_impact": "Puede aumentar peso",
        "considerations": "Monitorear peso"
    },
    
    # Psiquiátricos
    "sertralina": {
        "name": "Sertralina",
        "category": "antidepresivos",
        "nutritional_impact": "Puede alterar apetito y peso",
        "considerations": "Monitorear cambios de peso"
    },
    "fluoxetina": {
        "name": "Fluoxetina",
        "category": "antidepresivos",
        "nutritional_impact": "Puede reducir apetito inicialmente",
        "considerations": "Asegurar ingesta adecuada"
    },
    "escitalopram": {
        "name": "Escitalopram",
        "category": "antidepresivos",
        "nutritional_impact": "Puede aumentar peso",
        "considerations": "Control de porciones"
    },
    "quetiapina": {
        "name": "Quetiapina",
        "category": "antipsicoticos",
        "nutritional_impact": "Aumento de peso y apetito común",
        "considerations": "Plan hipocalórico preventivo"
    },
    "alprazolam": {
        "name": "Alprazolam",
        "category": "ansioliticos",
        "nutritional_impact": "Puede aumentar apetito",
        "considerations": "Evitar alcohol"
    },
    "clonazepam": {
        "name": "Clonazepam",
        "category": "ansioliticos",
        "nutritional_impact": "Puede causar somnolencia",
        "considerations": "Evitar alcohol"
    },
    
    # Corticoides
    "prednisona": {
        "name": "Prednisona",
        "category": "corticoides",
        "nutritional_impact": "Aumenta apetito, retención de líquidos, pérdida de K",
        "considerations": "Dieta baja en sodio, alta en K y Ca"
    },
    "betametasona": {
        "name": "Betametasona",
        "category": "corticoides",
        "nutritional_impact": "Similar a prednisona",
        "considerations": "Control de sodio y calorías"
    },
    
    # Antiinflamatorios
    "ibuprofeno": {
        "name": "Ibuprofeno",
        "category": "aines",
        "nutritional_impact": "Puede causar molestias GI",
        "considerations": "Tomar con comidas"
    },
    "diclofenac": {
        "name": "Diclofenac",
        "category": "aines",
        "nutritional_impact": "Puede causar molestias GI",
        "considerations": "Tomar con comidas"
    },
    "celecoxib": {
        "name": "Celecoxib",
        "category": "aines",
        "nutritional_impact": "Menor impacto GI",
        "considerations": "Hidratación adecuada"
    },
    
    # Anticonceptivos
    "anticonceptivos_orales": {
        "name": "Anticonceptivos orales",
        "category": "hormonales",
        "nutritional_impact": "Puede aumentar peso y retención de líquidos",
        "considerations": "Aumentar B6, B12, ácido fólico"
    },
    
    # Gastrointestinales
    "omeprazol": {
        "name": "Omeprazol",
        "category": "ibb",
        "nutritional_impact": "Reduce absorción de B12, Fe, Ca, Mg",
        "considerations": "Suplementar si uso prolongado"
    },
    "pantoprazol": {
        "name": "Pantoprazol",
        "category": "ibb",
        "nutritional_impact": "Similar a omeprazol",
        "considerations": "Monitorear B12"
    },
    "ranitidina": {
        "name": "Ranitidina",
        "category": "antiacidos",
        "nutritional_impact": "Menor impacto que IBP",
        "considerations": "Separar de comidas ricas en Fe"
    },
    
    # Otros
    "allopurinol": {
        "name": "Allopurinol",
        "category": "antigotosos",
        "nutritional_impact": "Ninguno significativo",
        "considerations": "Mantener hidratación"
    },
    "colchicina": {
        "name": "Colchicina",
        "category": "antigotosos",
        "nutritional_impact": "Puede causar diarrea",
        "considerations": "Hidratación adecuada"
    },
    "warfarina": {
        "name": "Warfarina",
        "category": "anticoagulantes",
        "nutritional_impact": "Interactúa con vitamina K",
        "considerations": "Ingesta constante de vitamina K"
    },
    "clopidogrel": {
        "name": "Clopidogrel",
        "category": "antiagregantes",
        "nutritional_impact": "Ninguno significativo",
        "considerations": "Evitar exceso de omega 3"
    }
}

def get_medication_considerations(medications_list: list) -> list:
    """
    Obtiene las consideraciones nutricionales para una lista de medicamentos
    
    Args:
        medications_list: Lista de claves de medicamentos
    
    Returns:
        Lista de consideraciones nutricionales
    """
    considerations = []
    impacts = []
    
    for med_key in medications_list:
        if med_key in MEDICATIONS_DATABASE:
            med = MEDICATIONS_DATABASE[med_key]
            considerations.append(f"• {med['name']}: {med['considerations']}")
            impacts.append(f"• {med['name']}: {med['nutritional_impact']}")
    
    return {
        "considerations": considerations,
        "impacts": impacts
    }