from typing import Dict, List, Optional
from ..utils.calculations import NutritionalCalculator
from ..utils.validators import InputValidator
from ..schemas.meal_plan import NewPatientRequest, Objetivo
import json

class PromptGenerator:
    def __init__(self):
        self.base_rules = """
REGLAS FUNDAMENTALES DEL MÉTODO:
1. Plan de 3 días iguales
2. Todas las cantidades en GRAMOS
3. Verduras tipo C (papa, batata, choclo) en gramos específicos
4. Otras verduras: porción libre pero coherente
5. Frutas siempre en gramos
6. Incluir forma de preparación para cada comida
7. No usar suplementos salvo indicación expresa
8. Usar léxico argentino
9. Adaptarse al nivel económico
"""

    def generate_motor1_prompt(self, patient_data: NewPatientRequest, recipes_json: str):
        """Motor 1: Paciente Nuevo con cálculos nutricionales integrados"""
        
        # Calcular requerimientos nutricionales
        daily_calories = NutritionalCalculator.calculate_daily_calories(patient_data)
        macro_distribution = NutritionalCalculator.calculate_macro_distribution(patient_data)
        meal_distribution = NutritionalCalculator.calculate_meal_distribution(
            daily_calories,
            patient_data.comidas_principales,
            patient_data.distribution_type.value,
            patient_data.colaciones != "No",
            patient_data.custom_meal_distribution
        )
        
        # Calcular gramos de macros
        protein_g = round((daily_calories * macro_distribution["proteinas"]) / 4)
        carbs_g = round((daily_calories * macro_distribution["carbohidratos"]) / 4)
        fat_g = round((daily_calories * macro_distribution["grasas"]) / 9)
        
        # Formatear objetivo para mostrar
        objetivo_text = self._format_objetivo(patient_data.objetivo)
        
        # Preparar strings que contienen saltos de línea
        meal_distribution_text = self._format_meal_distribution(meal_distribution)
        macro_note_text = self._get_macro_customization_note(patient_data)
        custom_distribution_text = self._format_custom_meal_distribution(patient_data.custom_meal_distribution) if patient_data.distribution_type.value == "custom" and patient_data.custom_meal_distribution else ""
        
        # Formatear actividades, suplementos y medicamentos
        activities_text = self._format_activities(patient_data.activities) if patient_data.activities else '- Tipo: ' + patient_data.tipo_actividad + '\n- Frecuencia: ' + str(patient_data.frecuencia_semanal) + 'x por semana\n- Duración: ' + str(patient_data.duracion_sesion) + ' minutos'
        supplements_text = self._format_supplements(patient_data.supplements) if patient_data.supplements else '- Suplementación: ' + (patient_data.suplementacion or 'Ninguna')
        medications_text = self._format_medications(patient_data.medications) if patient_data.medications else '- Patologías/Medicación: ' + (patient_data.patologias or 'Sin patologías')
        
        prompt = f"""
{self.base_rules}

MOTOR 1 - PACIENTE NUEVO
Generá un plan alimentario de 3 días iguales siguiendo el método.

DATOS DEL PACIENTE:
- Nombre: {patient_data.nombre}
- Edad: {patient_data.edad} años
- Sexo: {patient_data.sexo.value}
- Estatura: {patient_data.estatura} cm
- Peso: {patient_data.peso} kg
- IMC: {patient_data.imc} ({patient_data.imc_category})
- Objetivo: {objetivo_text}

ACTIVIDAD FÍSICA:
{activities_text}

ESPECIFICACIONES MÉDICAS:
{supplements_text}
{medications_text}
- NO consume: {patient_data.no_consume or 'Sin restricciones'}
- Le gusta: {patient_data.le_gusta or 'Sin preferencias específicas'}
- Nivel económico: {patient_data.nivel_economico.value}

REQUERIMIENTOS NUTRICIONALES CALCULADOS:
- Calorías diarias: {daily_calories} kcal
- Proteínas: {protein_g}g ({round(macro_distribution['proteinas']*100)}%)
- Carbohidratos: {carbs_g}g ({round(macro_distribution['carbohidratos']*100)}%)
- Grasas: {fat_g}g ({round(macro_distribution['grasas']*100)}%)

DISTRIBUCIÓN DE CALORÍAS POR COMIDA:
{meal_distribution_text}

{macro_note_text}

{custom_distribution_text}

CONFIGURACIÓN DEL PLAN:
- Comidas principales: {patient_data.comidas_principales}
- Colaciones: {patient_data.colaciones}
- Tipo de peso: Gramos en {patient_data.tipo_peso}

RECETAS DISPONIBLES:
{recipes_json}

INSTRUCCIONES PARA LA GENERACIÓN:
1. USAR ÚNICAMENTE las recetas proporcionadas arriba
2. Adaptar las cantidades según los objetivos
3. Respetar las restricciones alimentarias
4. Cada día debe tener exactamente las mismas comidas
5. Incluir preparación detallada
6. Calcular macros totales al final

FORMATO DE SALIDA ESPERADO:

PLAN ALIMENTARIO - 3 DÍAS IGUALES

DESAYUNO
- [Nombre de la receta de la base de datos]
- Ingredientes con cantidades ajustadas:
  * Ingrediente 1: XXg
  * Ingrediente 2: XXg
- Preparación: [de la receta]

ALMUERZO
[Mismo formato]

MERIENDA
[Mismo formato]

CENA
[Mismo formato]

COLACIÓN PRE/POST ENTRENO (si aplica)
[Mismo formato]

RESUMEN NUTRICIONAL DIARIO:
- Proteínas: XXg
- Carbohidratos: XXg
- Grasas: XXg
- Calorías totales: XXXX kcal
- Déficit/Superávit: apropiado para objetivo

RECOMENDACIONES PERSONALIZADAS:
- Hidratación
- Timing de suplementos
- Tips de preparación
"""
        return prompt

    def generate_motor2_prompt(self, control_data, previous_plan, recipes_json):
        """Motor 2: Control y Ajuste"""
        
        prompt = f"""
{self.base_rules}

MOTOR 2 - CONTROL DE PACIENTE
Reformulá el plan completo con base en los nuevos requerimientos.

DATOS ACTUALIZADOS:
- Nombre: {control_data.nombre}
- Fecha del control: {control_data.fecha_control}
- Peso anterior: {control_data.peso_anterior} kg
- Peso actual: {control_data.peso_actual} kg
- Diferencia: {control_data.diferencia_peso} kg
- Objetivo actualizado: {control_data.objetivo_actualizado}

CAMBIOS EN ACTIVIDAD:
- Tipo actual: {control_data.tipo_actividad_actual}
- Frecuencia: {control_data.frecuencia_actual}
- Duración: {control_data.duracion_actual}

AJUSTES SOLICITADOS:
- AGREGAR: {control_data.agregar}
- SACAR: {control_data.sacar}
- DEJAR: {control_data.dejar}

PLAN ANTERIOR:
{previous_plan}

RECETAS DISPONIBLES:
{recipes_json}

INSTRUCCIONES:
1. Analizar la evolución del paciente
2. Ajustar calorías según nuevo objetivo
3. Implementar los cambios solicitados
4. Mantener la estructura de 3 días iguales
5. Usar solo recetas de la base de datos

FORMATO DE SALIDA:

PLAN ALIMENTARIO ACTUALIZADO - 3 DÍAS IGUALES

[Seguir el mismo formato del Motor 1]

CAMBIOS IMPLEMENTADOS:
- Lista de modificaciones realizadas
- Justificación de los cambios
- Nuevos macros vs anteriores
"""
        return prompt

    def generate_motor3_prompt(self, meal_data, current_meal, recipes_json):
        """Motor 3: Reemplazo de Comida"""
        
        prompt = f"""
{self.base_rules}

MOTOR 3 - REEMPLAZO DE COMIDA ESPECÍFICA
Reemplazá una comida manteniendo los mismos macros y calorías.

DATOS:
- Paciente: {meal_data.paciente}
- Comida a reemplazar: {meal_data.comida_reemplazar}
- Nueva comida deseada: {meal_data.nueva_comida}
- Condiciones especiales: {meal_data.condiciones}
- Tipo de peso: Gramos en {meal_data.tipo_peso}

COMIDA ACTUAL:
{current_meal}

MACROS A MANTENER:
- Proteínas: {meal_data.proteinas}g ±5g
- Carbohidratos: {meal_data.carbohidratos}g ±5g
- Grasas: {meal_data.grasas}g ±3g
- Calorías: {meal_data.calorias} kcal ±50 kcal

RECETAS DISPONIBLES:
{recipes_json}

INSTRUCCIONES:
1. Buscar en las recetas una opción similar a lo solicitado
2. Ajustar cantidades para mantener macros
3. Respetar el método de preparación
4. Incluir comparación de macros (original vs nuevo)

FORMATO DE SALIDA:

REEMPLAZO DE {meal_data.comida_reemplazar.upper()}

OPCIÓN NUEVA:
- [Nombre de la receta]
- Ingredientes ajustados:
  * [Lista con cantidades]
- Preparación: [Detallada]

COMPARACIÓN NUTRICIONAL:
Original | Nuevo
Proteínas: XXg | XXg
Carbohidratos: XXg | XXg
Grasas: XXg | XXg
Calorías: XXX | XXX

✓ Diferencia dentro de rangos aceptables
"""
        return prompt
    
    def _format_objetivo(self, objetivo: Objetivo) -> str:
        """Formatea el objetivo de manera legible"""
        objetivo_map = {
            Objetivo.mantener: "Mantener peso",
            Objetivo.bajar_025: "Bajar 0.25 kg por semana",
            Objetivo.bajar_05: "Bajar 0.5 kg por semana",
            Objetivo.bajar_075: "Bajar 0.75 kg por semana",
            Objetivo.bajar_1: "Bajar 1 kg por semana",
            Objetivo.subir_025: "Subir 0.25 kg por semana",
            Objetivo.subir_05: "Subir 0.5 kg por semana",
            Objetivo.subir_075: "Subir 0.75 kg por semana",
            Objetivo.subir_1: "Subir 1 kg por semana",
        }
        return objetivo_map.get(objetivo, objetivo.value)
    
    def _format_meal_distribution(self, distribution: Dict[str, float]) -> str:
        """Formatea la distribución de calorías por comida"""
        formatted = []
        for meal, calories in distribution.items():
            formatted.append(f"- {meal.capitalize()}: {int(calories)} kcal")
        return "\n".join(formatted)
    
    def _get_macro_customization_note(self, patient_data: NewPatientRequest) -> str:
        """Genera nota sobre personalización de macros si aplica"""
        notes = []
        
        if patient_data.protein_level:
            protein_map = {
                "muy_baja": "Muy baja (0.5-0.8 g/kg) - Adaptada para patologías renales",
                "conservada": "Conservada (0.8-1.2 g/kg) - Nivel normal",
                "moderada": "Moderada (1.2-1.6 g/kg) - Para personas activas",
                "alta": "Alta (1.6-2.2 g/kg) - Uso deportivo",
                "muy_alta": "Muy alta (2.2-2.8 g/kg) - Alto rendimiento",
                "extrema": "Extrema (3.0-3.5 g/kg) - Requerimientos especiales"
            }
            notes.append(f"NIVEL DE PROTEÍNA: {protein_map.get(patient_data.protein_level.value, patient_data.protein_level.value)}")
        
        if patient_data.carbs_percentage is not None:
            notes.append(f"CARBOHIDRATOS PERSONALIZADOS: {patient_data.carbs_percentage}% del total calórico")
        
        if patient_data.fat_percentage is not None:
            notes.append(f"GRASAS PERSONALIZADAS: {patient_data.fat_percentage}% del total calórico")
        
        if patient_data.distribution_type.value == "equitable":
            notes.append("DISTRIBUCIÓN EQUITATIVA: Todas las comidas tienen las mismas calorías")
        
        return "\n".join(notes) if notes else ""
    
    def _format_custom_meal_distribution(self, custom_distribution: Dict[str, Dict[str, float]]) -> str:
        """Formatea la distribución personalizada de macros por comida"""
        if not custom_distribution:
            return ""
        
        formatted = ["DISTRIBUCIÓN PERSONALIZADA POR COMIDA:"]
        for meal, data in custom_distribution.items():
            formatted.append(f"\n{meal.upper()}:")
            formatted.append(f"  - Calorías: {int(data.get('calories', 0))} kcal")
            formatted.append(f"  - Proteínas: {int(data.get('protein_g', 0))}g")
            formatted.append(f"  - Carbohidratos: {int(data.get('carbs_g', 0))}g")
            formatted.append(f"  - Grasas: {int(data.get('fats_g', 0))}g")
        
        return "\n".join(formatted)
    
    def _format_activities(self, activities: List[Dict]) -> str:
        """Formatea las actividades físicas para el prompt"""
        if not activities:
            return ""
        
        formatted = []
        total_calories = 0
        
        for activity in activities:
            if activity.get('isManual'):
                formatted.append(f"- {activity['name']}: {activity['calories']} kcal/día")
            else:
                formatted.append(f"- {activity['name']}: {activity['duration']} min, {activity['frequency']}x/semana = {activity['calories']} kcal/día")
            total_calories += activity.get('calories', 0)
        
        formatted.append(f"- GASTO CALÓRICO TOTAL POR ACTIVIDAD: {total_calories} kcal/día")
        formatted.append("- Nota: Este gasto calórico YA está incluido en el cálculo de calorías diarias")
        
        return "\n".join(formatted)
    
    def _format_supplements(self, supplements: List[Dict]) -> str:
        """Formatea los suplementos para el prompt"""
        if not supplements:
            return ""
        
        formatted = ["SUPLEMENTACIÓN:"]
        total_macros = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}
        
        for supp in supplements:
            formatted.append(f"- {supp['name']}: {supp['servings']} porción(es) diarias ({supp['serving_size']})")
            formatted.append(f"  Aporta: {supp['calories']} kcal, P: {supp['protein']}g, C: {supp['carbs']}g, G: {supp['fats']}g")
            
            total_macros['calories'] += supp.get('calories', 0)
            total_macros['protein'] += supp.get('protein', 0)
            total_macros['carbs'] += supp.get('carbs', 0)
            total_macros['fats'] += supp.get('fats', 0)
        
        formatted.append(f"\nAPORTE TOTAL DE SUPLEMENTOS:")
        formatted.append(f"- Calorías: {total_macros['calories']} kcal")
        formatted.append(f"- Proteínas: {total_macros['protein']}g")
        formatted.append(f"- Carbohidratos: {total_macros['carbs']}g")
        formatted.append(f"- Grasas: {total_macros['fats']}g")
        formatted.append("- Nota: Estos macros YA están incluidos en los totales diarios calculados")
        
        return "\n".join(formatted)
    
    def _format_medications(self, medications: List[Dict]) -> str:
        """Formatea los medicamentos para el prompt"""
        if not medications:
            return ""
        
        formatted = ["MEDICACIÓN:"]
        impacts = []
        considerations = []
        
        for med in medications:
            formatted.append(f"- {med['name']}")
            if med.get('impact'):
                impacts.append(f"  • {med['name']}: {med['impact']}")
            if med.get('considerations'):
                considerations.append(f"  • {med['name']}: {med['considerations']}")
        
        if impacts:
            formatted.append("\nIMPACTOS NUTRICIONALES:")
            formatted.extend(impacts)
        
        if considerations:
            formatted.append("\nCONSIDERACIONES DIETÉTICAS:")
            formatted.extend(considerations)
        
        return "\n".join(formatted)