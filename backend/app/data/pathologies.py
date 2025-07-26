"""
Estructura de datos para patologías y condiciones médicas
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class PathologyType(str, Enum):
    """Tipos de patologías reconocidas por el sistema"""
    DIABETES_TIPO_1 = "diabetes_tipo_1"
    DIABETES_TIPO_2 = "diabetes_tipo_2"
    HIPOTIROIDISMO = "hipotiroidismo"
    HIPERTIROIDISMO = "hipertiroidismo"
    HIPERTENSION = "hipertension"
    CELIAQUIA = "celiaquia"
    RESISTENCIA_INSULINA = "resistencia_insulina"
    HIGADO_GRASO = "higado_graso"
    SINDROME_OVARIO_POLIQUISTICO = "sindrome_ovario_poliquistico"
    COLESTEROL_ALTO = "colesterol_alto"
    TRIGLICERIDOS_ALTOS = "trigliceridos_altos"
    GOTA = "gota"
    ANEMIA = "anemia"
    OSTEOPOROSIS = "osteoporosis"
    OSTEOPENIA = "osteopenia"
    ESOFAGITIS_REFLUJO = "esofagitis_reflujo"
    MENOPAUSIA = "menopausia"
    CANCER_PREQUIMIO = "cancer_prequimio"
    CANCER_POSQUIMIO = "cancer_posquimio"
    CANCER_RADIOTERAPIA = "cancer_radioterapia"
    ANTICANCER_PREQUIMIO = "anticancer_prequimio"
    ANTICANCER_POSTQUIMIO = "anticancer_postquimio"
    ANTICANCER_POSRAYOS = "anticancer_posrayos"
    ANTICANCER_POSTCIRUGIA = "anticancer_postcirugia"
    DESNUTRICION = "desnutricion"
    SARCOPENIA = "sarcopenia"
    HIPOREXIA = "hiporexia"
    BARIATRICO = "bariatrico"
    BALON_GASTRICO = "balon_gastrico"
    POSTOPERATORIO = "postoperatorio"
    POST_CIRUGIA = "post_cirugia"
    BLANDA = "blanda"
    DIGESTIVA = "digestiva"
    MALA_ABSORCION = "mala_absorcion"
    COLONOSCOPIA = "colonoscopia"
    HIPOGLUCEMIA = "hipoglucemia"
    EMBARAZO_PRIMER_TRIMESTRE = "embarazo_primer_trimestre"
    EMBARAZO_SEGUNDO_TRIMESTRE = "embarazo_segundo_trimestre"
    EMBARAZO_TERCER_TRIMESTRE = "embarazo_tercer_trimestre"
    DIABETES_GESTACIONAL = "diabetes_gestacional"
    HIPERTENSION_GESTACIONAL = "hipertension_gestacional"
    PREECLAMPSIA = "preeclampsia"
    

PATHOLOGIES_DATABASE: Dict[str, Dict[str, Any]] = {
    PathologyType.DIABETES_TIPO_1: {
        "name": "Diabetes Tipo 1",
        "description": "Diabetes insulinodependiente",
        "nutritional_adjustments": {
            "calories_adjustment": -100,
            "carbs_percentage": 35,
            "protein_percentage": 35,
            "fat_percentage": 30,
            "fiber_min": 30  # gramos por día
        },
        "dietary_restrictions": [
            "azúcar refinada", "miel", "dulces concentrados", 
            "jugos de fruta", "bebidas azucaradas"
        ],
        "recipe_tags_avoid": ["alto_ig", "dulce", "azucarado"],
        "recipe_tags_prefer": ["bajo_ig", "sin_azucar", "integral", "fibra"],
        "meal_distribution": {
            "breakfast": 20,
            "lunch": 35,
            "dinner": 30,
            "snacks": 15
        },
        "special_considerations": [
            "Mantener horarios regulares de comida",
            "Incluir proteína en cada comida",
            "Priorizar carbohidratos complejos",
            "Monitorear glucemia regularmente"
        ]
    },
    
    PathologyType.DIABETES_TIPO_2: {
        "name": "Diabetes Tipo 2",
        "description": "Diabetes no insulinodependiente",
        "nutritional_adjustments": {
            "calories_adjustment": -100,
            "carbs_percentage": 40,
            "protein_percentage": 30,
            "fat_percentage": 30,
            "fiber_min": 25
        },
        "dietary_restrictions": [
            "azúcar refinada", "harinas blancas", "dulces",
            "bebidas azucaradas", "alcohol en exceso"
        ],
        "recipe_tags_avoid": ["alto_ig", "dulce", "frito"],
        "recipe_tags_prefer": ["bajo_ig", "integral", "sin_azucar", "fibra"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 35,
            "dinner": 25,
            "snacks": 15
        },
        "special_considerations": [
            "Pérdida de peso gradual si hay sobrepeso",
            "Actividad física regular",
            "Control de porciones"
        ]
    },
    
    PathologyType.HIPOTIROIDISMO: {
        "name": "Hipotiroidismo",
        "description": "Función tiroidea disminuida",
        "nutritional_adjustments": {
            "calories_adjustment": -150,
            "carbs_percentage": 45,
            "protein_percentage": 30,
            "fat_percentage": 25,
            "iodine_adequate": True
        },
        "dietary_restrictions": [
            "soja en exceso", "crucíferas crudas en exceso"
        ],
        "recipe_tags_avoid": ["soja_alta"],
        "recipe_tags_prefer": ["yodo", "selenio", "zinc"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 40,
            "dinner": 25,
            "snacks": 10
        },
        "special_considerations": [
            "Tomar medicación en ayunas",
            "Evitar café junto con medicación",
            "Incluir alimentos ricos en yodo"
        ]
    },
    
    PathologyType.HIPERTENSION: {
        "name": "Hipertensión Arterial",
        "description": "Presión arterial elevada",
        "nutritional_adjustments": {
            "calories_adjustment": 0,
            "sodium_max": 1500,  # mg por día
            "potassium_min": 3500,  # mg por día
            "carbs_percentage": 50,
            "protein_percentage": 20,
            "fat_percentage": 30
        },
        "dietary_restrictions": [
            "sal de mesa", "embutidos", "conservas",
            "snacks salados", "caldos comerciales",
            "salsas comerciales", "quesos duros"
        ],
        "recipe_tags_avoid": ["alto_sodio", "procesado", "embutido"],
        "recipe_tags_prefer": ["bajo_sodio", "potasio", "magnesio", "dash"],
        "meal_distribution": {
            "breakfast": 20,
            "lunch": 40,
            "dinner": 30,
            "snacks": 10
        },
        "special_considerations": [
            "Usar hierbas y especias en lugar de sal",
            "Aumentar frutas y verduras",
            "Limitar cafeína",
            "Control de peso"
        ]
    },
    
    PathologyType.CELIAQUIA: {
        "name": "Celiaquía",
        "description": "Intolerancia al gluten",
        "nutritional_adjustments": {
            "calories_adjustment": 0,
            "fiber_min": 25,
            "calcium_min": 1000,  # mg
            "iron_adequate": True
        },
        "dietary_restrictions": [
            "trigo", "cebada", "centeno", "avena contaminada",
            "productos con gluten", "alimentos procesados sin certificar"
        ],
        "recipe_tags_avoid": ["gluten", "trigo", "cebada", "centeno"],
        "recipe_tags_prefer": ["sin_gluten", "certificado_celiacos"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 35,
            "dinner": 30,
            "snacks": 10
        },
        "special_considerations": [
            "Verificar certificación sin gluten",
            "Evitar contaminación cruzada",
            "Suplementar si hay deficiencias"
        ]
    },
    
    PathologyType.RESISTENCIA_INSULINA: {
        "name": "Resistencia a la Insulina",
        "description": "Prediabetes o síndrome metabólico",
        "nutritional_adjustments": {
            "calories_adjustment": -50,
            "carbs_percentage": 35,
            "protein_percentage": 35,
            "fat_percentage": 30,
            "fiber_min": 30
        },
        "dietary_restrictions": [
            "azúcares simples", "harinas refinadas",
            "bebidas azucaradas", "alcohol"
        ],
        "recipe_tags_avoid": ["alto_ig", "refinado", "azucarado"],
        "recipe_tags_prefer": ["bajo_ig", "integral", "fibra", "proteico"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 35,
            "dinner": 25,
            "snacks": 15
        },
        "special_considerations": [
            "Combinar carbohidratos con proteína",
            "Evitar ayunos prolongados",
            "Actividad física regular"
        ]
    },
    
    PathologyType.HIGADO_GRASO: {
        "name": "Hígado Graso No Alcohólico",
        "description": "Esteatosis hepática",
        "nutritional_adjustments": {
            "calories_adjustment": -200,
            "carbs_percentage": 35,
            "protein_percentage": 35,
            "fat_percentage": 30,
            "saturated_fat_max": 7  # % de calorías totales
        },
        "dietary_restrictions": [
            "alcohol", "frituras", "grasas trans",
            "azúcares añadidos", "alimentos ultraprocesados"
        ],
        "recipe_tags_avoid": ["frito", "graso", "alcohol", "azucarado"],
        "recipe_tags_prefer": ["vapor", "horno", "omega3", "antioxidante"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 40,
            "dinner": 25,
            "snacks": 10
        },
        "special_considerations": [
            "Pérdida de peso gradual (0.5-1 kg/semana)",
            "Aumentar omega-3",
            "Incluir antioxidantes"
        ]
    },
    
    # EMBARAZO - PRIMER TRIMESTRE
    PathologyType.EMBARAZO_PRIMER_TRIMESTRE: {
        "name": "Embarazo - Primer Trimestre",
        "description": "Semanas 1-13 de gestación",
        "nutritional_adjustments": {
            "calories_adjustment": 0,  # Sin aumento calórico
            "protein_g_per_kg": 1.2,  # g/kg peso pregestacional
            "carbs_percentage": 50,
            "protein_percentage": 20,
            "fat_percentage": 30,
            "folic_acid_mcg": 600,
            "iron_mg": 27,
            "calcium_mg": 1000,
            "min_carbs_grams": 175  # Evitar cetosis
        },
        "dietary_restrictions": [
            "alcohol", "cafeína excesiva", "pescados alto mercurio",
            "carnes crudas", "huevos crudos", "lácteos no pasteurizados",
            "embutidos no cocidos", "paté"
        ],
        "recipe_tags_avoid": ["crudo", "alcohol", "cafeina_alta", "mercurio"],
        "recipe_tags_prefer": ["folato", "b12", "suave", "facil_digestion"],
        "meal_distribution": {
            "breakfast": 20,
            "mid_morning": 10,
            "lunch": 30,
            "afternoon_snack": 10,
            "dinner": 25,
            "evening_snack": 5
        },
        "special_considerations": [
            "Comidas frecuentes y pequeñas para náuseas",
            "Evitar olores fuertes y grasas pesadas",
            "Priorizar alimentos secos en la mañana",
            "Hidratación adecuada entre comidas",
            "Suplementación con ácido fólico"
        ],
        "nausea_management": {
            "morning_foods": ["galletas secas", "tostadas", "cereales secos"],
            "avoid_textures": ["grasosas", "muy condimentadas", "olores fuertes"],
            "preferred_temps": ["tibio", "frío"],
            "hydration": "Pequeños sorbos frecuentes, evitar con comidas"
        }
    },
    
    # EMBARAZO - SEGUNDO TRIMESTRE
    PathologyType.EMBARAZO_SEGUNDO_TRIMESTRE: {
        "name": "Embarazo - Segundo Trimestre",
        "description": "Semanas 14-27 de gestación",
        "nutritional_adjustments": {
            "calories_adjustment": 300,  # +300 kcal/día
            "protein_g_per_kg": 1.4,  # g/kg peso actual
            "carbs_percentage": 50,
            "protein_percentage": 20,
            "fat_percentage": 30,
            "iron_mg": 27,
            "calcium_mg": 1000,
            "vitamin_d_iu": 600,
            "min_carbs_grams": 175
        },
        "dietary_restrictions": [
            "alcohol", "cafeína excesiva", "pescados alto mercurio",
            "carnes crudas", "huevos crudos", "lácteos no pasteurizados"
        ],
        "recipe_tags_avoid": ["crudo", "alcohol", "mercurio"],
        "recipe_tags_prefer": ["hierro", "calcio", "vitamina_c", "proteico"],
        "meal_distribution": {
            "breakfast": 20,
            "mid_morning": 10,
            "lunch": 35,
            "afternoon_snack": 10,
            "dinner": 20,
            "evening_snack": 5
        },
        "special_considerations": [
            "Aumentar hierro con vitamina C",
            "Incluir lácteos y calcio",
            "Colaciones nutritivas",
            "Prevenir anemia",
            "Control glucemia si hay riesgo"
        ]
    },
    
    # EMBARAZO - TERCER TRIMESTRE
    PathologyType.EMBARAZO_TERCER_TRIMESTRE: {
        "name": "Embarazo - Tercer Trimestre",
        "description": "Semanas 28-40 de gestación",
        "nutritional_adjustments": {
            "calories_adjustment": 450,  # +450 kcal/día
            "protein_g_per_kg": 1.5,  # g/kg peso actual
            "carbs_percentage": 50,
            "protein_percentage": 20,
            "fat_percentage": 30,
            "iron_mg": 27,
            "calcium_mg": 1000,
            "min_carbs_grams": 175
        },
        "dietary_restrictions": [
            "alcohol", "cafeína excesiva", "pescados alto mercurio",
            "carnes crudas", "alimentos que causan reflujo"
        ],
        "recipe_tags_avoid": ["crudo", "alcohol", "acido", "picante"],
        "recipe_tags_prefer": ["facil_digestion", "calcio", "omega3"],
        "meal_distribution": {
            "breakfast": 15,
            "mid_morning": 10,
            "lunch": 30,
            "afternoon_snack": 15,
            "dinner": 20,
            "evening_snack": 10
        },
        "special_considerations": [
            "Comidas más pequeñas y frecuentes",
            "Evitar acostarse después de comer",
            "Preferir líquidos entre comidas",
            "Alimentos blandos si hay saciedad precoz",
            "Preparación para lactancia"
        ],
        "reflux_management": {
            "avoid_foods": ["cítricos", "tomate", "chocolate", "menta", "frituras"],
            "meal_timing": "Cenar 2-3 horas antes de dormir",
            "portions": "Pequeñas y frecuentes"
        }
    },
    
    # DIABETES GESTACIONAL
    PathologyType.DIABETES_GESTACIONAL: {
        "name": "Diabetes Gestacional",
        "description": "Diabetes durante el embarazo",
        "nutritional_adjustments": {
            "calories_adjustment": 300,  # Según trimestre
            "carbs_percentage": 40,
            "protein_percentage": 30,
            "fat_percentage": 30,
            "min_carbs_grams": 175,  # Evitar cetosis
            "carbs_per_meal_max": 45,  # gramos
            "carbs_per_snack_max": 20  # gramos
        },
        "dietary_restrictions": [
            "azúcar refinada", "jugos de fruta", "dulces",
            "harinas refinadas", "bebidas azucaradas"
        ],
        "recipe_tags_avoid": ["alto_ig", "azucarado", "refinado"],
        "recipe_tags_prefer": ["bajo_ig", "integral", "proteico", "fibra"],
        "meal_distribution": {
            "breakfast": 15,
            "mid_morning": 10,
            "lunch": 30,
            "afternoon_snack": 10,
            "dinner": 25,
            "evening_snack": 10
        },
        "special_considerations": [
            "Monitoreo glucemia 4 veces al día",
            "Incluir proteína en cada comida",
            "Evitar ayunos prolongados",
            "Actividad física moderada",
            "Control estricto de carbohidratos"
        ],
        "glucose_targets": {
            "fasting": "< 95 mg/dL",
            "one_hour_post": "< 140 mg/dL",
            "two_hour_post": "< 120 mg/dL"
        }
    },
    
    PathologyType.SINDROME_OVARIO_POLIQUISTICO: {
        "name": "Síndrome de Ovario Poliquístico",
        "description": "SOP - Trastorno hormonal",
        "nutritional_adjustments": {
            "calories_adjustment": -100,
            "carbs_percentage": 40,
            "protein_percentage": 30,
            "fat_percentage": 30,
            "fiber_min": 25
        },
        "dietary_restrictions": [
            "azúcares refinados", "lácteos enteros en exceso",
            "carnes procesadas"
        ],
        "recipe_tags_avoid": ["alto_ig", "lacteo_entero", "procesado"],
        "recipe_tags_prefer": ["bajo_ig", "antiinflamatorio", "omega3"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 35,
            "dinner": 30,
            "snacks": 10
        },
        "special_considerations": [
            "Control de peso si hay sobrepeso",
            "Alimentos antiinflamatorios",
            "Ejercicio regular"
        ]
    },
    
    PathologyType.OSTEOPENIA: {
        "name": "Osteopenia",
        "description": "Disminución de la densidad mineral ósea",
        "nutritional_adjustments": {
            "calories_adjustment": 0,
            "calcium_min": 1200,  # mg por día
            "vitamin_d_min": 800,  # UI por día
            "protein_percentage": 25,
            "carbs_percentage": 50,
            "fat_percentage": 25
        },
        "dietary_restrictions": [
            "exceso de sodio", "exceso de cafeína", 
            "alcohol en exceso", "bebidas carbonatadas en exceso"
        ],
        "recipe_tags_avoid": ["alto_sodio", "cafeina_alta"],
        "recipe_tags_prefer": ["calcio", "vitamina_d", "magnesio", "vitamina_k"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 35,
            "dinner": 30,
            "snacks": 10
        },
        "special_considerations": [
            "Incluir lácteos o alternativas fortificadas",
            "Exposición solar moderada para vitamina D",
            "Ejercicios de fuerza para fortalecer huesos",
            "Evitar dietas muy restrictivas en calorías"
        ]
    },
    
    PathologyType.ESOFAGITIS_REFLUJO: {
        "name": "Esofagitis por Reflujo",
        "description": "Inflamación del esófago por reflujo ácido",
        "nutritional_adjustments": {
            "calories_adjustment": 0,
            "fat_percentage": 25,  # Reducir grasas
            "protein_percentage": 25,
            "carbs_percentage": 50,
            "fiber_min": 20  # Fibra soluble preferentemente
        },
        "dietary_restrictions": [
            "alimentos ácidos", "tomate", "cítricos", "chocolate",
            "menta", "café", "té negro", "alcohol", "frituras",
            "alimentos muy condimentados", "cebolla", "ajo"
        ],
        "recipe_tags_avoid": ["acido", "picante", "frito", "graso", "cafeina"],
        "recipe_tags_prefer": ["suave", "hervido", "vapor", "bajo_grasa", "fibra_soluble"],
        "meal_distribution": {
            "breakfast": 20,
            "mid_morning": 10,
            "lunch": 30,
            "afternoon_snack": 10,
            "dinner": 20,
            "evening_snack": 10
        },
        "special_considerations": [
            "Comidas pequeñas y frecuentes",
            "No acostarse hasta 2-3 horas después de comer",
            "Elevar cabecera de la cama",
            "Masticar bien los alimentos",
            "Preferir preparaciones blandas y suaves"
        ]
    },
    
    PathologyType.MENOPAUSIA: {
        "name": "Menopausia",
        "description": "Cese de la menstruación y cambios hormonales",
        "nutritional_adjustments": {
            "calories_adjustment": -100,  # Metabolismo más lento
            "calcium_min": 1200,  # mg por día
            "vitamin_d_min": 800,  # UI por día
            "protein_percentage": 25,
            "carbs_percentage": 45,
            "fat_percentage": 30,
            "fiber_min": 25
        },
        "dietary_restrictions": [
            "alimentos muy procesados", "exceso de azúcares",
            "grasas trans", "exceso de sal"
        ],
        "recipe_tags_avoid": ["procesado", "azucarado", "alto_sodio"],
        "recipe_tags_prefer": ["calcio", "vitamina_d", "fitoestrogenos", "omega3", "antioxidante"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 35,
            "dinner": 25,
            "snacks": 15
        },
        "special_considerations": [
            "Incluir alimentos con fitoestrógenos (soja, linaza)",
            "Mantener peso saludable",
            "Hidratación adecuada",
            "Ejercicio regular para masa ósea y muscular",
            "Control de síntomas con alimentación"
        ]
    },
    
    # PATOLOGÍAS ONCOLÓGICAS
    PathologyType.CANCER_PREQUIMIO: {
        "name": "Cáncer - Pre Quimioterapia",
        "description": "Preparación nutricional para tratamiento oncológico",
        "nutritional_adjustments": {
            "calories_adjustment": 200,  # 35-40 kcal/kg
            "protein_g_per_kg": 2.0,  # Alta proteína preventiva
            "carbs_percentage": 45,
            "protein_percentage": 30,
            "fat_percentage": 25,
            "fiber_min": 20  # Moderada para evitar molestias
        },
        "dietary_restrictions": [
            "alcohol", "alimentos crudos", "carnes poco cocidas",
            "lácteos no pasteurizados", "alimentos muy condimentados"
        ],
        "recipe_tags_avoid": ["crudo", "alcohol", "muy_condimentado"],
        "recipe_tags_prefer": ["anticancer", "anticancer_prequimio", "alta_proteina", "digestiva"],
        "meal_distribution": {
            "breakfast": 20,
            "mid_morning": 10,
            "lunch": 30,
            "afternoon_snack": 10,
            "dinner": 20,
            "evening_snack": 10
        },
        "special_considerations": [
            "Optimizar estado nutricional antes del tratamiento",
            "Énfasis en proteínas de alto valor biológico",
            "Suplementar con proteína en polvo si es necesario",
            "Hidratación óptima (2-3L/día)",
            "Considerar multivitamínico con minerales"
        ]
    },
    
    PathologyType.CANCER_POSQUIMIO: {
        "name": "Cáncer - Post Quimioterapia",
        "description": "Recuperación nutricional post tratamiento",
        "nutritional_adjustments": {
            "calories_adjustment": 100,  # 30-35 kcal/kg inicial
            "protein_g_per_kg": 1.8,  # Alta proteína para recuperación
            "carbs_percentage": 50,
            "protein_percentage": 25,
            "fat_percentage": 25,
            "fiber_min": 15  # Baja inicialmente
        },
        "dietary_restrictions": [
            "cítricos", "alimentos ácidos", "condimentos fuertes",
            "grasas cocidas", "café", "alcohol", "olores penetrantes"
        ],
        "recipe_tags_avoid": ["acido", "picante", "graso", "cafeina", "olor_fuerte"],
        "recipe_tags_prefer": ["anticancer_posquimio", "bajo_residuo", "digestiva", "bland", "suave"],
        "meal_distribution": {
            "breakfast": 15,
            "mid_morning": 10,
            "lunch": 25,
            "afternoon_snack": 15,
            "dinner": 20,
            "evening_snack": 15
        },
        "special_considerations": [
            "Texturas suaves y temperaturas tibias/frías",
            "Fraccionamiento en 6-8 comidas pequeñas",
            "Evitar líquidos con las comidas principales",
            "Sales de rehidratación si hay vómitos/diarrea",
            "BCAA 5-10g/día para preservar masa muscular"
        ],
        "symptom_management": {
            "nausea": ["jengibre", "comidas frías", "galletas secas"],
            "mucositis": ["texturas líquidas", "evitar ácidos", "temperatura ambiente"],
            "diarrea": ["arroz blanco", "banana", "manzana rallada", "probióticos"]
        }
    },
    
    PathologyType.CANCER_RADIOTERAPIA: {
        "name": "Cáncer - Durante Radioterapia",
        "description": "Soporte nutricional durante radiación",
        "nutritional_adjustments": {
            "calories_adjustment": 150,
            "protein_g_per_kg": 1.8,
            "carbs_percentage": 50,
            "protein_percentage": 25,
            "fat_percentage": 25,
            "selenium_adequate": True,
            "zinc_adequate": True
        },
        "dietary_restrictions": [
            "irritantes locales según zona irradiada",
            "fibra insoluble si radiación abdominal"
        ],
        "recipe_tags_avoid": ["irritante", "alto_residuo"],
        "recipe_tags_prefer": ["anticancer", "antioxidante", "suave"],
        "meal_distribution": {
            "breakfast": 20,
            "mid_morning": 10,
            "lunch": 30,
            "afternoon_snack": 10,
            "dinner": 25,
            "evening_snack": 5
        },
        "special_considerations": [
            "Adaptar según zona irradiada",
            "Hidratación extra importante",
            "Antioxidantes naturales (no megadosis)",
            "Zinc y selenio para cicatrización"
        ]
    },
    
    PathologyType.DESNUTRICION: {
        "name": "Desnutrición",
        "description": "Estado de déficit nutricional severo",
        "nutritional_adjustments": {
            "calories_adjustment": 300,  # Iniciar gradual
            "protein_g_per_kg": 1.5,  # Mínimo, aumentar progresivamente
            "carbs_percentage": 50,
            "protein_percentage": 20,
            "fat_percentage": 30,
            "progression": "gradual"  # 20-25 kcal/kg inicial
        },
        "dietary_restrictions": [
            "volúmenes grandes", "fibra excesiva inicialmente"
        ],
        "recipe_tags_avoid": ["voluminoso", "muy_fibroso"],
        "recipe_tags_prefer": ["desnutricion", "alta_densidad", "facil_digestion"],
        "meal_distribution": {
            "breakfast": 15,
            "mid_morning": 15,
            "lunch": 25,
            "afternoon_snack": 15,
            "dinner": 20,
            "evening_snack": 10
        },
        "special_considerations": [
            "Progresión calórica gradual",
            "Suplementación proteica obligatoria",
            "Multivitamínico con minerales",
            "Monitoreo de síndrome de realimentación"
        ]
    },
    
    PathologyType.SARCOPENIA: {
        "name": "Sarcopenia",
        "description": "Pérdida de masa muscular",
        "nutritional_adjustments": {
            "calories_adjustment": 200,
            "protein_g_per_kg": 2.2,  # Muy alta proteína
            "leucine_min": 3,  # g por comida principal
            "carbs_percentage": 40,
            "protein_percentage": 35,
            "fat_percentage": 25
        },
        "dietary_restrictions": [],
        "recipe_tags_avoid": [],
        "recipe_tags_prefer": ["sarcopenia", "alta_proteina", "leucina"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 35,
            "dinner": 30,
            "snacks": 10
        },
        "special_considerations": [
            "Proteína distribuida uniformemente",
            "BCAA 10g/día, especialmente leucina",
            "Ejercicio de resistencia obligatorio",
            "Vitamina D 2000-4000 UI/día"
        ]
    },
    
    PathologyType.HIPOREXIA: {
        "name": "Hiporexia",
        "description": "Pérdida severa del apetito",
        "nutritional_adjustments": {
            "calories_adjustment": 0,  # Mantener requerimientos
            "texture_preference": "variable",
            "temperature_preference": "fría o tibia",
            "volume": "pequeño"
        },
        "dietary_restrictions": [
            "olores fuertes", "platos muy elaborados"
        ],
        "recipe_tags_avoid": ["olor_fuerte", "voluminoso"],
        "recipe_tags_prefer": ["hiporexia", "apetitoso", "pequeña_porcion"],
        "meal_distribution": {
            "breakfast": 10,
            "mid_morning": 15,
            "lunch": 25,
            "afternoon_snack": 15,
            "dinner": 20,
            "evening_snack": 15
        },
        "special_considerations": [
            "Respetar preferencias del paciente",
            "Presentación atractiva fundamental",
            "Enriquecer preparaciones sin aumentar volumen",
            "Considerar estimulantes del apetito naturales"
        ]
    },
    
    PathologyType.ANTICANCER_PREQUIMIO: {
        "name": "Anticáncer Pre-Quimioterapia",
        "description": "Preparación nutricional previa a quimioterapia",
        "nutritional_adjustments": {
            "calories_adjustment": 200,
            "carbs_percentage": 40,
            "protein_percentage": 30,
            "fat_percentage": 30,
            "protein_per_kg": 2.0,
            "fiber_min": 25
        },
        "dietary_restrictions": [
            "alcohol", "alimentos muy procesados", "azúcares refinados"
        ],
        "recipe_tags_avoid": ["procesado", "frito", "alcohol"],
        "recipe_tags_prefer": ["alta_proteina", "digestiva", "blanda", "sin_soja", "sin_gluten"],
        "meal_distribution": {
            "breakfast": 25,
            "lunch": 30,
            "dinner": 25,
            "snacks": 20
        },
        "special_considerations": [
            "Optimizar estado nutricional",
            "Énfasis en alta proteína (2g/kg)",
            "Mejorar sistema inmune",
            "Hidratación abundante"
        ]
    },
    
    PathologyType.ANTICANCER_POSTQUIMIO: {
        "name": "Anticáncer Post-Quimioterapia",
        "description": "Recuperación nutricional post-quimioterapia",
        "nutritional_adjustments": {
            "calories_adjustment": 300,
            "carbs_percentage": 45,
            "protein_percentage": 25,
            "fat_percentage": 30,
            "protein_per_kg": 1.5,
            "fiber_min": 15
        },
        "dietary_restrictions": [
            "alcohol", "picantes", "ácidos", "muy calientes", "muy fríos"
        ],
        "recipe_tags_avoid": ["picante", "acido", "crudo", "frito"],
        "recipe_tags_prefer": ["blanda", "digestiva", "antiinflamatoria", "sin_lactosa"],
        "meal_distribution": {
            "breakfast": 15,
            "mid_morning": 10,
            "lunch": 25,
            "afternoon": 10,
            "dinner": 25,
            "evening": 15
        },
        "special_considerations": [
            "Texturas suaves",
            "Fraccionamiento 6-8 comidas",
            "Evitar olores fuertes",
            "Temperatura templada"
        ]
    },
    
    PathologyType.ANTICANCER_POSRAYOS: {
        "name": "Anticáncer Post-Radioterapia",
        "description": "Recuperación nutricional post-radioterapia",
        "nutritional_adjustments": {
            "calories_adjustment": 250,
            "carbs_percentage": 45,
            "protein_percentage": 25,
            "fat_percentage": 30,
            "protein_per_kg": 1.5
        },
        "dietary_restrictions": [
            "alcohol", "irritantes", "ácidos", "fibra insoluble"
        ],
        "recipe_tags_avoid": ["irritante", "acido", "alto_fibra", "crudo"],
        "recipe_tags_prefer": ["blanda", "digestiva", "sin_gluten", "sin_lactosa"],
        "meal_distribution": {
            "breakfast": 20,
            "mid_morning": 10,
            "lunch": 25,
            "afternoon": 10,
            "dinner": 25,
            "evening": 10
        },
        "special_considerations": [
            "Evitar irritantes según zona irradiada",
            "Hidratación constante",
            "Suplementación según déficits"
        ]
    },
    
    PathologyType.BARIATRICO: {
        "name": "Cirugía Bariátrica",
        "description": "Post-operatorio de cirugía bariátrica",
        "nutritional_adjustments": {
            "calories_adjustment": -500,
            "carbs_percentage": 30,
            "protein_percentage": 40,
            "fat_percentage": 30,
            "protein_per_kg": 1.5,
            "max_volume_per_meal": 200
        },
        "dietary_restrictions": [
            "azúcares simples", "bebidas con gas", "alimentos duros", "fibrosos"
        ],
        "recipe_tags_avoid": ["azucarado", "carbonatado", "duro", "fibroso"],
        "recipe_tags_prefer": ["bariatrico", "alta_proteina", "blanda", "pequeña_porcion"],
        "meal_distribution": {
            "breakfast": 15,
            "mid_morning": 15,
            "lunch": 20,
            "afternoon": 15,
            "dinner": 20,
            "evening": 15
        },
        "special_considerations": [
            "Volúmenes pequeños (max 200ml)",
            "Masticación exhaustiva",
            "No líquidos con comidas",
            "Proteína prioritaria"
        ]
    },
    
    PathologyType.BALON_GASTRICO: {
        "name": "Balón Gástrico",
        "description": "Paciente con balón intragástrico",
        "nutritional_adjustments": {
            "calories_adjustment": -400,
            "carbs_percentage": 35,
            "protein_percentage": 35,
            "fat_percentage": 30,
            "max_volume_per_meal": 150
        },
        "dietary_restrictions": [
            "bebidas con gas", "alimentos que produzcan gases", "irritantes"
        ],
        "recipe_tags_avoid": ["carbonatado", "flatulento", "irritante"],
        "recipe_tags_prefer": ["balon_gastrico", "digestiva", "pequeña_porcion"],
        "meal_distribution": {
            "breakfast": 15,
            "mid_morning": 15,
            "lunch": 20,
            "afternoon": 15,
            "dinner": 20,
            "evening": 15
        },
        "special_considerations": [
            "Volúmenes muy pequeños",
            "Evitar flatulentos",
            "Comer despacio",
            "Hidratación entre comidas"
        ]
    },
    
    PathologyType.BLANDA: {
        "name": "Dieta Blanda",
        "description": "Textura modificada blanda",
        "nutritional_adjustments": {
            "calories_adjustment": 0,
            "carbs_percentage": 50,
            "protein_percentage": 20,
            "fat_percentage": 30
        },
        "dietary_restrictions": [
            "alimentos duros", "crudos duros", "fibrosos", "con cáscara"
        ],
        "recipe_tags_avoid": ["duro", "crudo", "fibroso", "crujiente"],
        "recipe_tags_prefer": ["blanda", "cocido", "pure", "suave"],
        "special_considerations": [
            "Texturas suaves y fáciles de masticar",
            "Cocción prolongada",
            "Sin trozos duros"
        ]
    },
    
    PathologyType.DIGESTIVA: {
        "name": "Dieta Digestiva",
        "description": "Fácil digestión y bajo residuo",
        "nutritional_adjustments": {
            "calories_adjustment": 0,
            "carbs_percentage": 50,
            "protein_percentage": 20,
            "fat_percentage": 30,
            "fiber_max": 15
        },
        "dietary_restrictions": [
            "frituras", "condimentos fuertes", "fibra insoluble", "lácteos enteros"
        ],
        "recipe_tags_avoid": ["frito", "condimentado", "alto_fibra", "graso"],
        "recipe_tags_prefer": ["digestiva", "bajo_residuo", "cocido", "suave"],
        "special_considerations": [
            "Métodos de cocción simples",
            "Bajo en grasa",
            "Sin irritantes",
            "Fibra soluble preferente"
        ]
    },
    
    PathologyType.MALA_ABSORCION: {
        "name": "Malabsorción",
        "description": "Síndrome de malabsorción intestinal",
        "nutritional_adjustments": {
            "calories_adjustment": 400,
            "carbs_percentage": 50,
            "protein_percentage": 20,
            "fat_percentage": 30,
            "use_mct_oil": True
        },
        "dietary_restrictions": [
            "lactosa", "gluten", "fibra insoluble", "grasas de cadena larga"
        ],
        "recipe_tags_avoid": ["lactosa", "gluten", "alto_fibra", "graso"],
        "recipe_tags_prefer": ["sin_lactosa", "sin_gluten", "mala_absorcion", "fortificado"],
        "special_considerations": [
            "Usar MCT oil si es posible",
            "Suplementación vitamínica",
            "Comidas frecuentes y pequeñas",
            "Alimentos fortificados"
        ]
    },
    
    PathologyType.COLONOSCOPIA: {
        "name": "Preparación Colonoscopía",
        "description": "Dieta para preparación de colonoscopía",
        "nutritional_adjustments": {
            "calories_adjustment": -200,
            "carbs_percentage": 60,
            "protein_percentage": 20,
            "fat_percentage": 20,
            "fiber_max": 5
        },
        "dietary_restrictions": [
            "fibra", "semillas", "cáscaras", "vegetales crudos", "frutas con piel"
        ],
        "recipe_tags_avoid": ["fibra", "integral", "semillas", "crudo"],
        "recipe_tags_prefer": ["colonoscopia", "sin_residuo", "liquido", "blando"],
        "special_considerations": [
            "Sin residuos",
            "Líquidos claros últimas 24h",
            "Evitar colorantes rojos/morados"
        ]
    },
    
    PathologyType.HIPOGLUCEMIA: {
        "name": "Hipoglucemia",
        "description": "Tendencia a hipoglucemias",
        "nutritional_adjustments": {
            "calories_adjustment": 0,
            "carbs_percentage": 45,
            "protein_percentage": 25,
            "fat_percentage": 30,
            "glycemic_index": "bajo"
        },
        "dietary_restrictions": [
            "ayunos prolongados", "azúcares simples solos", "alcohol"
        ],
        "recipe_tags_avoid": ["alto_ig", "azucar_simple", "alcohol"],
        "recipe_tags_prefer": ["bajo_ig", "proteico", "fibra", "hipoglucemia"],
        "meal_distribution": {
            "breakfast": 20,
            "mid_morning": 10,
            "lunch": 25,
            "afternoon": 10,
            "dinner": 25,
            "evening": 10
        },
        "special_considerations": [
            "Comidas frecuentes cada 3 horas",
            "Combinar carbohidratos con proteína",
            "Índice glucémico bajo",
            "Evitar ayunos"
        ]
    }
}


def get_pathology_info(pathology_type: PathologyType) -> Dict[str, Any]:
    """Obtiene la información completa de una patología"""
    return PATHOLOGIES_DATABASE.get(pathology_type, {})


def get_nutritional_adjustments(pathology_types: List[PathologyType]) -> Dict[str, Any]:
    """
    Combina los ajustes nutricionales de múltiples patologías
    Prioriza los valores más restrictivos cuando hay conflictos
    """
    if not pathology_types:
        return {}
    
    combined_adjustments = {
        "calories_adjustment": 0,
        "carbs_percentage": None,
        "protein_percentage": None,
        "fat_percentage": None,
        "min_carbs_grams": 130,  # Mínimo por defecto
        "sodium_max": None,
        "fiber_min": 25
    }
    
    # Recopilar todos los ajustes
    for pathology in pathology_types:
        info = get_pathology_info(pathology)
        if not info:
            continue
            
        adjustments = info.get("nutritional_adjustments", {})
        
        # Sumar ajustes calóricos
        combined_adjustments["calories_adjustment"] += adjustments.get("calories_adjustment", 0)
        
        # Para carbohidratos mínimos, tomar el máximo (más restrictivo)
        if "min_carbs_grams" in adjustments:
            combined_adjustments["min_carbs_grams"] = max(
                combined_adjustments["min_carbs_grams"],
                adjustments["min_carbs_grams"]
            )
        
        # Para sodio máximo, tomar el mínimo (más restrictivo)
        if "sodium_max" in adjustments:
            if combined_adjustments["sodium_max"] is None:
                combined_adjustments["sodium_max"] = adjustments["sodium_max"]
            else:
                combined_adjustments["sodium_max"] = min(
                    combined_adjustments["sodium_max"],
                    adjustments["sodium_max"]
                )
        
        # Para fibra mínima, tomar el máximo
        if "fiber_min" in adjustments:
            combined_adjustments["fiber_min"] = max(
                combined_adjustments["fiber_min"],
                adjustments["fiber_min"]
            )
    
    # Manejar macros - usar los más restrictivos o promediar si hay múltiples
    macro_configs = []
    for pathology in pathology_types:
        info = get_pathology_info(pathology)
        if info and "nutritional_adjustments" in info:
            adj = info["nutritional_adjustments"]
            if all(k in adj for k in ["carbs_percentage", "protein_percentage", "fat_percentage"]):
                macro_configs.append({
                    "carbs": adj["carbs_percentage"],
                    "protein": adj["protein_percentage"],
                    "fat": adj["fat_percentage"]
                })
    
    # Si hay configuraciones de macros, usar la más restrictiva en carbohidratos
    if macro_configs:
        # Ordenar por carbohidratos (menor primero - más restrictivo)
        macro_configs.sort(key=lambda x: x["carbs"])
        selected_macros = macro_configs[0]
        combined_adjustments["carbs_percentage"] = selected_macros["carbs"]
        combined_adjustments["protein_percentage"] = selected_macros["protein"]
        combined_adjustments["fat_percentage"] = selected_macros["fat"]
    
    return combined_adjustments


def get_all_dietary_restrictions(pathology_types: List[PathologyType]) -> List[str]:
    """Obtiene todas las restricciones dietéticas únicas de las patologías"""
    restrictions = set()
    
    for pathology in pathology_types:
        info = get_pathology_info(pathology)
        if info and "dietary_restrictions" in info:
            restrictions.update(info["dietary_restrictions"])
    
    return list(restrictions)


def get_recipe_tags_to_avoid(pathology_types: List[PathologyType]) -> List[str]:
    """Obtiene todos los tags de recetas a evitar"""
    tags = set()
    
    for pathology in pathology_types:
        info = get_pathology_info(pathology)
        if info and "recipe_tags_avoid" in info:
            tags.update(info["recipe_tags_avoid"])
    
    return list(tags)


def get_recipe_tags_to_prefer(pathology_types: List[PathologyType]) -> List[str]:
    """Obtiene todos los tags de recetas preferidas"""
    tags = set()
    
    for pathology in pathology_types:
        info = get_pathology_info(pathology)
        if info and "recipe_tags_prefer" in info:
            tags.update(info["recipe_tags_prefer"])
    
    return list(tags)


def detect_pathologies_from_text(text: str) -> List[PathologyType]:
    """
    Detecta patologías a partir de texto libre
    Usado para mantener compatibilidad con el sistema actual
    """
    if not text:
        return []
    
    text_lower = text.lower()
    detected = []
    
    # Mapeo de palabras clave a patologías
    keyword_mapping = {
        # Diabetes
        ("diabetes tipo 1", "diabetes insulinodependiente", "dbt1"): PathologyType.DIABETES_TIPO_1,
        ("diabetes tipo 2", "diabetes no insulinodependiente", "dbt2", "diabetes"): PathologyType.DIABETES_TIPO_2,
        ("diabetes gestacional", "diabetes embarazo"): PathologyType.DIABETES_GESTACIONAL,
        
        # Tiroides
        ("hipotiroidismo", "tiroides baja", "hashimoto"): PathologyType.HIPOTIROIDISMO,
        ("hipertiroidismo", "tiroides alta", "graves"): PathologyType.HIPERTIROIDISMO,
        
        # Cardiovascular
        ("hipertensión", "hipertenso", "presión alta", "hta"): PathologyType.HIPERTENSION,
        ("colesterol alto", "hipercolesterolemia", "dislipidemia"): PathologyType.COLESTEROL_ALTO,
        ("triglicéridos", "trigliceridos altos"): PathologyType.TRIGLICERIDOS_ALTOS,
        
        # Digestivo
        ("celiaquía", "celíaco", "celiaco", "intolerancia gluten"): PathologyType.CELIAQUIA,
        ("hígado graso", "higado graso", "esteatosis", "nafld"): PathologyType.HIGADO_GRASO,
        
        # Metabólico
        ("resistencia insulina", "prediabetes", "síndrome metabólico"): PathologyType.RESISTENCIA_INSULINA,
        ("síndrome ovario poliquístico", "sop", "ovario poliquistico"): PathologyType.SINDROME_OVARIO_POLIQUISTICO,
        ("gota", "ácido úrico", "hiperuricemia"): PathologyType.GOTA,
        
        # Otros
        ("anemia", "ferropenia", "déficit hierro"): PathologyType.ANEMIA,
        ("osteoporosis", "densidad ósea baja"): PathologyType.OSTEOPOROSIS,
        ("osteopenia", "densidad osea disminuida", "densitometria no salio bien"): PathologyType.OSTEOPENIA,
        ("esofagitis", "reflujo", "erge", "reflujo gastroesofágico"): PathologyType.ESOFAGITIS_REFLUJO,
        ("menopausia", "climaterio"): PathologyType.MENOPAUSIA,
        
        # Oncológicas
        ("cáncer", "cancer", "oncológico", "tumor"): None,  # Procesamiento especial
        ("prequimio", "pre quimio", "antes de quimioterapia"): PathologyType.CANCER_PREQUIMIO,
        ("posquimio", "post quimio", "después de quimioterapia"): PathologyType.CANCER_POSQUIMIO,
        ("radioterapia", "radiación", "rayos"): PathologyType.CANCER_RADIOTERAPIA,
        ("anticancer prequimio", "anticáncer prequimio"): PathologyType.ANTICANCER_PREQUIMIO,
        ("anticancer postquimio", "anticáncer postquimio"): PathologyType.ANTICANCER_POSTQUIMIO,
        ("anticancer posrayos", "anticáncer posrayos", "post radioterapia"): PathologyType.ANTICANCER_POSRAYOS,
        ("anticancer postcirugia", "anticáncer postcirugía", "post cirugía oncológica"): PathologyType.ANTICANCER_POSTCIRUGIA,
        ("desnutrición", "desnutrido", "bajo peso severo"): PathologyType.DESNUTRICION,
        ("sarcopenia", "pérdida muscular", "pérdida de masa muscular"): PathologyType.SARCOPENIA,
        ("hiporexia", "falta de apetito", "pérdida de apetito", "inapetencia"): PathologyType.HIPOREXIA,
        
        # Condiciones digestivas y quirúrgicas
        ("bariátrico", "bariatrico", "cirugía bariátrica", "sleeve", "bypass gástrico"): PathologyType.BARIATRICO,
        ("balón gástrico", "balon gastrico", "balón intragástrico"): PathologyType.BALON_GASTRICO,
        ("postoperatorio", "post operatorio", "post cirugía", "postcirugía"): PathologyType.POSTOPERATORIO,
        ("dieta blanda", "textura blanda", "alimentos blandos"): PathologyType.BLANDA,
        ("digestiva", "fácil digestión", "dieta digestiva"): PathologyType.DIGESTIVA,
        ("malabsorción", "mala absorción", "síndrome malabsorción"): PathologyType.MALA_ABSORCION,
        ("colonoscopía", "colonoscopia", "preparación colonoscopía"): PathologyType.COLONOSCOPIA,
        ("hipoglucemia", "hipoglicemia", "glucemia baja"): PathologyType.HIPOGLUCEMIA,
        
        # Embarazo
        ("embarazada", "gestación", "gestante", "embarazo"): None,  # Procesamiento especial
        ("primer trimestre", "1er trimestre", "semana 1-13"): PathologyType.EMBARAZO_PRIMER_TRIMESTRE,
        ("segundo trimestre", "2do trimestre", "semana 14-27"): PathologyType.EMBARAZO_SEGUNDO_TRIMESTRE,
        ("tercer trimestre", "3er trimestre", "semana 28-40"): PathologyType.EMBARAZO_TERCER_TRIMESTRE,
        ("hipertensión gestacional", "hipertension embarazo"): PathologyType.HIPERTENSION_GESTACIONAL,
        ("preeclampsia", "pre-eclampsia"): PathologyType.PREECLAMPSIA
    }
    
    # Detectar patologías por palabras clave
    for keywords, pathology in keyword_mapping.items():
        if pathology is None:  # Casos especiales
            if any(keyword in text_lower for keyword in keywords):
                # Caso especial para embarazo
                if keywords[0] in ["embarazada", "gestación", "gestante", "embarazo"]:
                    # Buscar trimestre específico
                    if "primer" in text_lower or "1er" in text_lower or "1°" in text_lower:
                        detected.append(PathologyType.EMBARAZO_PRIMER_TRIMESTRE)
                    elif "segundo" in text_lower or "2do" in text_lower or "2°" in text_lower:
                        detected.append(PathologyType.EMBARAZO_SEGUNDO_TRIMESTRE)
                    elif "tercer" in text_lower or "3er" in text_lower or "3°" in text_lower:
                        detected.append(PathologyType.EMBARAZO_TERCER_TRIMESTRE)
                    else:
                        # Si no se especifica trimestre, asumir segundo
                        detected.append(PathologyType.EMBARAZO_SEGUNDO_TRIMESTRE)
                
                # Caso especial para cáncer
                elif keywords[0] in ["cáncer", "cancer", "oncológico", "tumor"]:
                    # Buscar fase específica
                    if "prequimio" in text_lower or "pre quimio" in text_lower or "antes de quimio" in text_lower:
                        detected.append(PathologyType.CANCER_PREQUIMIO)
                    elif "posquimio" in text_lower or "post quimio" in text_lower or "después de quimio" in text_lower:
                        detected.append(PathologyType.CANCER_POSQUIMIO)
                    elif "radioterapia" in text_lower or "radiación" in text_lower:
                        detected.append(PathologyType.CANCER_RADIOTERAPIA)
                    else:
                        # Si no se especifica fase, asumir prequimio
                        detected.append(PathologyType.CANCER_PREQUIMIO)
        else:
            if any(keyword in text_lower for keyword in keywords):
                detected.append(pathology)
    
    # Eliminar duplicados manteniendo orden
    seen = set()
    unique_detected = []
    for item in detected:
        if item not in seen:
            seen.add(item)
            unique_detected.append(item)
    
    return unique_detected


def is_pregnancy_pathology(pathology: PathologyType) -> bool:
    """Determina si una patología es relacionada con embarazo"""
    pregnancy_types = [
        PathologyType.EMBARAZO_PRIMER_TRIMESTRE,
        PathologyType.EMBARAZO_SEGUNDO_TRIMESTRE,
        PathologyType.EMBARAZO_TERCER_TRIMESTRE,
        PathologyType.DIABETES_GESTACIONAL,
        PathologyType.HIPERTENSION_GESTACIONAL,
        PathologyType.PREECLAMPSIA
    ]
    return pathology in pregnancy_types


def get_pregnancy_info(pathology_types: List[PathologyType]) -> Optional[Dict[str, Any]]:
    """
    Obtiene información específica de embarazo si hay alguna patología relacionada
    Retorna None si no hay embarazo
    """
    pregnancy_pathologies = [p for p in pathology_types if is_pregnancy_pathology(p)]
    
    if not pregnancy_pathologies:
        return None
    
    # Determinar trimestre principal
    trimester = None
    for p in pregnancy_pathologies:
        if "TRIMESTRE" in p.value:
            trimester = p
            break
    
    if not trimester:
        # Si hay diabetes o hipertensión gestacional sin trimestre, asumir segundo
        trimester = PathologyType.EMBARAZO_SEGUNDO_TRIMESTRE
    
    # Obtener información base del trimestre
    base_info = get_pathology_info(trimester).copy()
    
    # Agregar condiciones adicionales
    additional_conditions = []
    if PathologyType.DIABETES_GESTACIONAL in pregnancy_pathologies:
        additional_conditions.append("diabetes_gestacional")
    if PathologyType.HIPERTENSION_GESTACIONAL in pregnancy_pathologies:
        additional_conditions.append("hipertension_gestacional")
    if PathologyType.PREECLAMPSIA in pregnancy_pathologies:
        additional_conditions.append("preeclampsia")
    
    base_info["additional_conditions"] = additional_conditions
    base_info["trimester"] = trimester.value
    
    return base_info