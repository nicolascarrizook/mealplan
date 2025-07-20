# Actividades físicas con gasto calórico estimado
# Formato: kcal/hora para una persona de 70kg aproximadamente

ACTIVITIES_DATABASE = {
    # Cardiovascular
    "caminar_lento": {
        "name": "Caminar (ritmo lento)",
        "category": "cardiovascular",
        "kcal_per_hour": 150,
        "intensity": "baja",
        "met": 2.5
    },
    "caminar_moderado": {
        "name": "Caminar (ritmo moderado)",
        "category": "cardiovascular", 
        "kcal_per_hour": 270,
        "intensity": "moderada",
        "met": 3.5
    },
    "caminar_rapido": {
        "name": "Caminar (ritmo rápido)",
        "category": "cardiovascular",
        "kcal_per_hour": 360,
        "intensity": "moderada",
        "met": 4.5
    },
    "correr_lento": {
        "name": "Correr (8 km/h)",
        "category": "cardiovascular",
        "kcal_per_hour": 480,
        "intensity": "alta",
        "met": 8.0
    },
    "correr_moderado": {
        "name": "Correr (10 km/h)",
        "category": "cardiovascular",
        "kcal_per_hour": 600,
        "intensity": "alta",
        "met": 10.0
    },
    "correr_rapido": {
        "name": "Correr (12 km/h)",
        "category": "cardiovascular",
        "kcal_per_hour": 720,
        "intensity": "muy alta",
        "met": 12.0
    },
    "bicicleta_paseo": {
        "name": "Bicicleta (paseo)",
        "category": "cardiovascular",
        "kcal_per_hour": 240,
        "intensity": "baja",
        "met": 4.0
    },
    "bicicleta_moderado": {
        "name": "Bicicleta (ritmo moderado)",
        "category": "cardiovascular",
        "kcal_per_hour": 420,
        "intensity": "moderada",
        "met": 7.0
    },
    "bicicleta_intenso": {
        "name": "Bicicleta (ritmo intenso)",
        "category": "cardiovascular",
        "kcal_per_hour": 600,
        "intensity": "alta",
        "met": 10.0
    },
    "natacion_suave": {
        "name": "Natación (ritmo suave)",
        "category": "cardiovascular",
        "kcal_per_hour": 360,
        "intensity": "moderada",
        "met": 6.0
    },
    "natacion_moderado": {
        "name": "Natación (ritmo moderado)",
        "category": "cardiovascular",
        "kcal_per_hour": 420,
        "intensity": "moderada",
        "met": 7.0
    },
    "natacion_intenso": {
        "name": "Natación (ritmo intenso)",
        "category": "cardiovascular",
        "kcal_per_hour": 600,
        "intensity": "alta",
        "met": 10.0
    },
    "eliptica": {
        "name": "Elíptica",
        "category": "cardiovascular",
        "kcal_per_hour": 400,
        "intensity": "moderada",
        "met": 6.0
    },
    "remo": {
        "name": "Máquina de remo",
        "category": "cardiovascular",
        "kcal_per_hour": 440,
        "intensity": "moderada",
        "met": 7.0
    },
    "saltar_cuerda": {
        "name": "Saltar la cuerda",
        "category": "cardiovascular",
        "kcal_per_hour": 600,
        "intensity": "alta",
        "met": 10.0
    },
    
    # Fuerza/Gimnasio
    "pesas_ligero": {
        "name": "Pesas (intensidad ligera)",
        "category": "fuerza",
        "kcal_per_hour": 180,
        "intensity": "baja",
        "met": 3.0
    },
    "pesas_moderado": {
        "name": "Pesas (intensidad moderada)",
        "category": "fuerza",
        "kcal_per_hour": 270,
        "intensity": "moderada",
        "met": 4.5
    },
    "pesas_intenso": {
        "name": "Pesas (intensidad alta)",
        "category": "fuerza",
        "kcal_per_hour": 360,
        "intensity": "alta",
        "met": 6.0
    },
    "crossfit": {
        "name": "CrossFit",
        "category": "fuerza",
        "kcal_per_hour": 600,
        "intensity": "muy alta",
        "met": 10.0
    },
    "calistenia": {
        "name": "Calistenia",
        "category": "fuerza",
        "kcal_per_hour": 400,
        "intensity": "moderada",
        "met": 6.5
    },
    
    # Clases grupales
    "spinning": {
        "name": "Spinning/Ciclismo indoor",
        "category": "clases",
        "kcal_per_hour": 500,
        "intensity": "alta",
        "met": 8.5
    },
    "zumba": {
        "name": "Zumba",
        "category": "clases",
        "kcal_per_hour": 400,
        "intensity": "moderada",
        "met": 6.5
    },
    "aerobicos": {
        "name": "Aeróbicos",
        "category": "clases",
        "kcal_per_hour": 360,
        "intensity": "moderada",
        "met": 6.0
    },
    "yoga": {
        "name": "Yoga",
        "category": "clases",
        "kcal_per_hour": 180,
        "intensity": "baja",
        "met": 3.0
    },
    "yoga_power": {
        "name": "Power Yoga",
        "category": "clases",
        "kcal_per_hour": 300,
        "intensity": "moderada",
        "met": 5.0
    },
    "pilates": {
        "name": "Pilates",
        "category": "clases",
        "kcal_per_hour": 210,
        "intensity": "baja",
        "met": 3.5
    },
    "boxeo": {
        "name": "Boxeo (entrenamiento)",
        "category": "clases",
        "kcal_per_hour": 540,
        "intensity": "alta",
        "met": 9.0
    },
    
    # Deportes
    "futbol": {
        "name": "Fútbol",
        "category": "deportes",
        "kcal_per_hour": 500,
        "intensity": "alta",
        "met": 8.0
    },
    "basquet": {
        "name": "Básquetbol",
        "category": "deportes",
        "kcal_per_hour": 440,
        "intensity": "alta",
        "met": 7.5
    },
    "tenis": {
        "name": "Tenis",
        "category": "deportes",
        "kcal_per_hour": 400,
        "intensity": "moderada",
        "met": 7.0
    },
    "paddle": {
        "name": "Paddle",
        "category": "deportes",
        "kcal_per_hour": 350,
        "intensity": "moderada",
        "met": 6.0
    },
    "golf": {
        "name": "Golf (caminando)",
        "category": "deportes",
        "kcal_per_hour": 240,
        "intensity": "baja",
        "met": 4.0
    },
    "voleibol": {
        "name": "Voleibol",
        "category": "deportes",
        "kcal_per_hour": 270,
        "intensity": "moderada",
        "met": 4.5
    },
    
    # Actividades recreativas
    "baile_social": {
        "name": "Baile social",
        "category": "recreativo",
        "kcal_per_hour": 270,
        "intensity": "moderada",
        "met": 4.5
    },
    "senderismo": {
        "name": "Senderismo/Trekking",
        "category": "recreativo",
        "kcal_per_hour": 340,
        "intensity": "moderada",
        "met": 5.5
    },
    "escalada": {
        "name": "Escalada",
        "category": "recreativo",
        "kcal_per_hour": 540,
        "intensity": "alta",
        "met": 9.0
    },
    
    # Actividad personalizada
    "custom": {
        "name": "Actividad personalizada",
        "category": "custom",
        "kcal_per_hour": 0,
        "intensity": "variable",
        "met": 0
    }
}

def calculate_activity_calories(
    activity_key: str,
    duration_minutes: int,
    frequency_per_week: int,
    body_weight: float = 70.0,
    custom_kcal: float = 0
) -> dict:
    """
    Calcula las calorías gastadas por actividad
    
    Args:
        activity_key: Clave de la actividad en el diccionario
        duration_minutes: Duración de cada sesión en minutos
        frequency_per_week: Frecuencia semanal
        body_weight: Peso corporal en kg
        custom_kcal: Calorías personalizadas (solo para 'custom')
    
    Returns:
        dict con información de gasto calórico
    """
    if activity_key == "custom" and custom_kcal > 0:
        kcal_per_hour = custom_kcal
    else:
        activity = ACTIVITIES_DATABASE.get(activity_key, ACTIVITIES_DATABASE["caminar_moderado"])
        # Ajustar por peso corporal (la base es 70kg)
        kcal_per_hour = activity["kcal_per_hour"] * (body_weight / 70.0)
    
    # Calcular calorías por sesión
    kcal_per_session = (kcal_per_hour / 60) * duration_minutes
    
    # Calcular calorías semanales
    kcal_per_week = kcal_per_session * frequency_per_week
    
    # Calcular calorías diarias promedio
    kcal_per_day = kcal_per_week / 7
    
    return {
        "kcal_per_session": round(kcal_per_session),
        "kcal_per_week": round(kcal_per_week),
        "kcal_per_day": round(kcal_per_day),
        "total_minutes_per_week": duration_minutes * frequency_per_week
    }