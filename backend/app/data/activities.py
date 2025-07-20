# Actividades físicas con gasto calórico estimado
# Formato: kcal/minuto para una persona de 70kg
# Fórmula general: Gasto total semanal = (Kcal/min x peso paciente / 70) x duración en minutos x frecuencia semanal

ACTIVITIES_DATABASE = {
    # Cardiovascular
    "caminar_lento": {
        "name": "Caminata lenta (recreativa)",
        "category": "cardiovascular",
        "kcal_per_minute": 3.5,  # 3-4 kcal/min
        "kcal_per_hour": 210,
        "intensity": "baja",
        "notes": "Recreativa"
    },
    "caminar_rapido": {
        "name": "Caminata rápida",
        "category": "cardiovascular",
        "kcal_per_minute": 4.5,  # 4-5 kcal/min
        "kcal_per_hour": 270,
        "intensity": "moderada",
        "notes": "Uso cardiovascular"
    },
    "running_moderado": {
        "name": "Running (trote medio, 8-10 km/h)",
        "category": "cardiovascular",
        "kcal_per_minute": 11,  # 10-12 kcal/min
        "kcal_per_hour": 660,
        "intensity": "alta",
        "notes": "Ritmo sostenido"
    },
    "running_intenso": {
        "name": "Running (fondo o competitivo)",
        "category": "cardiovascular",
        "kcal_per_minute": 13.5,  # 12-15 kcal/min
        "kcal_per_hour": 810,
        "intensity": "muy alta",
        "notes": "Carreras o entrenamientos intensos"
    },
    "bicicleta_urbana": {
        "name": "Bicicleta urbana (traslado)",
        "category": "cardiovascular",
        "kcal_per_minute": 5.5,  # 5-6 kcal/min
        "kcal_per_hour": 330,
        "intensity": "baja",
        "notes": "Uso recreativo o transporte"
    },
    "bicicleta_entrenamiento": {
        "name": "Bicicleta entrenamiento (ritmo moderado)",
        "category": "cardiovascular",
        "kcal_per_minute": 10.5,  # 9-12 kcal/min
        "kcal_per_hour": 630,
        "intensity": "moderada",
        "notes": "Ejercicio sostenido"
    },
    "bicicleta_fondo": {
        "name": "Bicicleta fondo (>80 km)",
        "category": "cardiovascular",
        "kcal_per_minute": 14.5,  # 13-16 kcal/min
        "kcal_per_hour": 870,
        "intensity": "muy alta",
        "notes": "Alta duración, carga cardiovascular"
    },
    "natacion_recreativa": {
        "name": "Natación recreativa",
        "category": "cardiovascular",
        "kcal_per_minute": 8,  # 7-9 kcal/min
        "kcal_per_hour": 480,
        "intensity": "moderada",
        "notes": "Estilo libre, ritmo medio"
    },
    "natacion_competicion": {
        "name": "Natación de competición",
        "category": "cardiovascular",
        "kcal_per_minute": 11.5,  # 10-13 kcal/min
        "kcal_per_hour": 690,
        "intensity": "muy alta",
        "notes": "Alta exigencia física"
    },
    "trekking": {
        "name": "Trekking (moderado)",
        "category": "cardiovascular",
        "kcal_per_minute": 6,  # 5-7 kcal/min
        "kcal_per_hour": 360,
        "intensity": "moderada",
        "notes": "Caminatas en pendiente o terreno irregular"
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
    "pesas_aparatos": {
        "name": "Pesas / Aparatos",
        "category": "fuerza",
        "kcal_per_minute": 5.5,  # 5-6 kcal/min
        "kcal_per_hour": 330,
        "intensity": "moderada",
        "notes": "Intensidad moderada, sin pausas prolongadas"
    },
    "calistenia": {
        "name": "Calistenia",
        "category": "fuerza",
        "kcal_per_minute": 6.5,  # 6-7 kcal/min
        "kcal_per_hour": 390,
        "intensity": "moderada",
        "notes": "Actividad con peso corporal"
    },
    "crossfit": {
        "name": "CrossFit",
        "category": "fuerza",
        "kcal_per_minute": 11,  # 10-12 kcal/min
        "kcal_per_hour": 660,
        "intensity": "muy alta",
        "notes": "Alta intensidad, ejercicios funcionales con poco descanso"
    },
    "funcional_hiit": {
        "name": "Entrenamiento Funcional / HIIT",
        "category": "fuerza",
        "kcal_per_minute": 9,  # 8-10 kcal/min
        "kcal_per_hour": 540,
        "intensity": "alta",
        "notes": "Circuitos activos"
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
    },
    
    # Sedentarismo
    "sedentario": {
        "name": "Sedentario (trabajo en oficina)",
        "category": "otros",
        "kcal_per_hour": 0,
        "intensity": "sedentario",
        "notes": "TMB x 1.2 - Actividad física mínima",
        "activity_factor": 1.2
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
    Fórmula: (Kcal/min x peso paciente / 70) x duración en minutos x frecuencia semanal
    
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
        kcal_per_session = custom_kcal
    else:
        activity = ACTIVITIES_DATABASE.get(activity_key, ACTIVITIES_DATABASE["caminar_rapido"])
        
        # Usar kcal_per_minute si está disponible, sino calcular desde kcal_per_hour
        if "kcal_per_minute" in activity:
            # Fórmula del contexto: (Kcal/min x peso paciente / 70) x duración
            kcal_per_session = (activity["kcal_per_minute"] * body_weight / 70.0) * duration_minutes
        else:
            # Fallback para actividades sin kcal_per_minute
            kcal_per_hour = activity.get("kcal_per_hour", 300) * (body_weight / 70.0)
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