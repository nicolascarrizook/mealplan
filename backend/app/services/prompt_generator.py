from typing import Dict, List, Optional
from ..utils.calculations import NutritionalCalculator
from ..utils.validators import InputValidator
from ..schemas.meal_plan import NewPatientRequest, Objetivo
from ..data.interactions import check_interactions, check_max_doses, get_synergies
from ..data.pathologies import (
    detect_pathologies_from_text,
    get_pathology_info,
    get_all_dietary_restrictions,
    get_recipe_tags_to_avoid,
    get_recipe_tags_to_prefer,
    get_pregnancy_info
)
from ..utils.pregnancy import PregnancyManager
import json
import re
import logging

logger = logging.getLogger(__name__)

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
10. OBLIGATORIO: Usar ÚNICAMENTE recetas del catálogo proporcionado mediante sus IDs
"""
        
        self.recipe_format_rules = """
FORMATO OBLIGATORIO PARA CADA COMIDA:
- Proporcionar 3 OPCIONES de recetas para cada comida
- Cada opción debe incluir ID de receta: [REC_XXXX]
- Ajustes de cantidades si es necesario
- NO inventar recetas nuevas
- NO combinar recetas sin que esté especificado
- Las 3 opciones deben tener macros similares (±10%)
"""

    def generate_motor1_prompt(self, patient_data: NewPatientRequest, recipes_json: str):
        """Motor 1: Paciente Nuevo con cálculos nutricionales integrados"""
        
        # Verificar si hay embarazo
        pregnancy_requirements = NutritionalCalculator.calculate_pregnancy_adjusted_requirements(patient_data)
        
        if pregnancy_requirements:
            # Usar requerimientos ajustados para embarazo
            daily_calories = pregnancy_requirements['adjusted_calories']
            macro_distribution = {
                "proteinas": pregnancy_requirements['macros']['protein_percentage'] / 100,
                "carbohidratos": pregnancy_requirements['macros']['carbs_percentage'] / 100,
                "grasas": pregnancy_requirements['macros']['fat_percentage'] / 100
            }
            protein_g = pregnancy_requirements['macros']['protein_g']
            carbs_g = pregnancy_requirements['macros']['carbs_g']
            fat_g = pregnancy_requirements['macros']['fat_g']
            
            # Usar distribución de comidas especial para embarazo
            meal_distribution = pregnancy_requirements.get('meal_distribution', {})
            if meal_distribution:
                # Convertir porcentajes a calorías
                meal_distribution = {
                    meal: round(daily_calories * (percentage / 100))
                    for meal, percentage in meal_distribution.items()
                }
            else:
                meal_distribution = NutritionalCalculator.calculate_meal_distribution(
                    daily_calories,
                    patient_data.comidas_principales,
                    patient_data.distribution_type.value,
                    False,
                    patient_data.custom_meal_distribution
                )
        else:
            # Cálculos normales si no hay embarazo
            daily_calories = NutritionalCalculator.calculate_daily_calories(patient_data)
            macro_distribution = NutritionalCalculator.calculate_macro_distribution(patient_data)
            meal_distribution = NutritionalCalculator.calculate_meal_distribution(
                daily_calories,
                patient_data.comidas_principales,
                patient_data.distribution_type.value,
                False,
                patient_data.custom_meal_distribution
            )
            
            # Calcular gramos de macros
            protein_g = round((daily_calories * macro_distribution["proteinas"]) / 4)
            carbs_g = round((daily_calories * macro_distribution["carbohidratos"]) / 4)
            fat_g = round((daily_calories * macro_distribution["grasas"]) / 9)
        
        # Verificar si el objetivo de proteína es alcanzable
        protein_warning_text = self._check_protein_feasibility(patient_data, protein_g)
        
        # Formatear objetivo para mostrar
        objetivo_text = self._format_objetivo(patient_data.objetivo)
        
        # Preparar strings que contienen saltos de línea
        meal_distribution_text = self._format_meal_distribution(meal_distribution)
        macro_note_text = self._get_macro_customization_note(patient_data)
        custom_distribution_text = self._format_custom_meal_distribution(patient_data.custom_meal_distribution) if patient_data.distribution_type.value == "custom" and patient_data.custom_meal_distribution else ""
        
        # Formatear actividades, suplementos y medicamentos
        activities_text = self._format_activities(patient_data.activities) if patient_data.activities else '- Tipo: ' + patient_data.tipo_actividad + '\n- Frecuencia: ' + str(patient_data.frecuencia_semanal) + 'x por semana\n- Duración: ' + str(patient_data.duracion_sesion) + ' minutos'
        supplements_text = self._format_supplements(patient_data.supplements, patient_data.medications) if patient_data.supplements else '- Suplementación: ' + (patient_data.suplementacion or 'Ninguna')
        
        # Procesar patologías y medicamentos
        pathologies_section = self._format_pathologies_and_medications(patient_data)
        
        meal_config_text = self._format_meal_configuration(patient_data.meal_configuration.dict()) if patient_data.meal_configuration else ''
        
        # Sección de embarazo si aplica
        pregnancy_section = ""
        if pregnancy_requirements:
            pregnancy_manager = PregnancyManager()
            pregnancy_section = pregnancy_manager.get_pregnancy_prompt_section(
                pregnancy_requirements['pregnancy_info'],
                pregnancy_requirements
            )
        
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
{pathologies_section}
- NO consume: {patient_data.no_consume or 'Sin restricciones'}
- Le gusta: {patient_data.le_gusta or 'Sin preferencias específicas'}
- Nivel económico: {patient_data.nivel_economico.value}

{pregnancy_section}

REQUERIMIENTOS NUTRICIONALES CALCULADOS:
- Calorías diarias: {daily_calories} kcal
- Proteínas: {protein_g}g ({round(macro_distribution['proteinas']*100)}%)
- Carbohidratos: {carbs_g}g ({round(macro_distribution['carbohidratos']*100)}%)
- Grasas: {fat_g}g ({round(macro_distribution['grasas']*100)}%)

DISTRIBUCIÓN DE CALORÍAS POR COMIDA:
{meal_distribution_text}

{macro_note_text}

{protein_warning_text}

{custom_distribution_text}

CONFIGURACIÓN DEL PLAN:
- Comidas principales: {patient_data.comidas_principales}
- Tipo de peso: Gramos en {patient_data.tipo_peso}

{meal_config_text}

RECETAS DISPONIBLES:
{recipes_json}

{self.recipe_format_rules}

INSTRUCCIONES PARA LA GENERACIÓN:
1. OBLIGATORIO: Usar ÚNICAMENTE los IDs de recetas proporcionados arriba [REC_XXXX]
2. Para cada comida, proporcionar 3 OPCIONES de recetas diferentes
3. Las 3 opciones deben tener macros similares (±10% de diferencia)
4. Adaptar las cantidades de ingredientes según los objetivos nutricionales
5. Respetar las restricciones alimentarias y nivel económico
6. Cada día debe tener exactamente las mismas comidas
7. Incluir macros específicos para cada opción
8. INCLUIR TODAS LAS COMIDAS CONFIGURADAS (principales + adicionales)
9. Si hay suplementos configurados, incluirlos con las dosis especificadas
10. Calcular macros totales al final (basados en la opción 1 de cada comida)

FORMATO DE SALIDA ESPERADO:

PLAN ALIMENTARIO - 3 DÍAS IGUALES

DESAYUNO [agregar "(2 hs post medicación)" si toma levotiroxina con fibra]
OPCIÓN 1:
- Receta: [REC_XXXX] - [Nombre de la receta]
- Ingredientes con cantidades ajustadas:
  * Ingrediente 1: XXg
  * Ingrediente 2: XXg
- Macros: P: XXg | C: XXg | G: XXg | Cal: XXX

OPCIÓN 2:
- Receta: [REC_XXXX] - [Nombre de la receta]
- Ingredientes con cantidades ajustadas:
  * [Lista de ingredientes]
- Macros: P: XXg | C: XXg | G: XXg | Cal: XXX

OPCIÓN 3:
- Receta: [REC_XXXX] - [Nombre de la receta]
- Ingredientes con cantidades ajustadas:
  * [Lista de ingredientes]
- Macros: P: XXg | C: XXg | G: XXg | Cal: XXX

ALMUERZO
[Mismo formato con 3 opciones]

MERIENDA
[Mismo formato con 3 opciones]

CENA
[Mismo formato con 3 opciones]

COMIDAS ADICIONALES (según configuración):
- MEDIA MAÑANA (si aplica)
- MEDIA TARDE (si aplica)
- POSTRE ALMUERZO (si aplica)
- POSTRE CENA (si aplica)
- DULCE SIESTA (si aplica)
- PRE-ENTRENO (si aplica)
- POST-ENTRENO (si aplica)
[Mismo formato con 3 opciones para cada una]

SUPLEMENTACIÓN (si aplica):
- Listar cada suplemento con su dosis específica
- Incluir timing recomendado

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
    
    def _check_protein_feasibility(self, patient_data: NewPatientRequest, target_protein_g: float) -> str:
        """Verifica si el objetivo de proteína es alcanzable con los alimentos"""
        if not patient_data.protein_level:
            return ""
        
        # Calcular el objetivo real basado en el nivel de proteína
        from ..utils.calculations import NutritionalCalculator
        protein_g_per_kg = NutritionalCalculator.get_protein_grams_per_kg(patient_data.protein_level)
        ideal_protein_g = patient_data.peso * protein_g_per_kg
        
        # Si hay una diferencia significativa (>10%), generar advertencia
        difference_percentage = abs((target_protein_g - ideal_protein_g) / ideal_protein_g) * 100
        
        if difference_percentage > 10:
            return f"""
⚠️ ADVERTENCIA DE PROTEÍNA:
- Objetivo ideal según nivel {patient_data.protein_level.value}: {ideal_protein_g:.0f}g ({protein_g_per_kg}g/kg)
- Proteína calculada con las calorías disponibles: {target_protein_g:.0f}g
- Diferencia: {difference_percentage:.0f}%
- NOTA: No se pudo alcanzar el objetivo de proteína. Se requiere ajuste manual de porciones o agregar fuentes proteicas adicionales.
"""
        return ""
    
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
    
    def _format_supplements(self, supplements: List[Dict], medications: List[Dict] = None) -> str:
        """Formatea los suplementos para el prompt incluyendo advertencias de interacciones"""
        if not supplements:
            return ""
        
        formatted = ["SUPLEMENTACIÓN:"]
        total_macros = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}
        
        for supp in supplements:
            dose_info = f"{supp['servings']} porción(es)"
            if supp.get('custom_dose'):
                dose_info = supp['custom_dose']
            if supp.get('frequency'):
                dose_info += f" - {supp['frequency']}"
            
            formatted.append(f"- {supp['name']}: {dose_info} ({supp.get('serving_size', '')})")
            formatted.append(f"  Aporta: {supp['calories']} kcal, P: {supp['protein']}g, C: {supp['carbs']}g, G: {supp['fats']}g")
            
            # Marcar relevancia clínica
            if supp.get('clinical_relevance'):
                formatted.append("  ⚠️ RELEVANCIA CLÍNICA - Requiere consideración especial")
            
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
        
        # Verificar interacciones si hay medicamentos
        if medications:
            interactions = check_interactions([med['name'] for med in medications], supplements)
            if interactions:
                formatted.append("\n⚠️ ADVERTENCIAS DE INTERACCIONES:")
                for warning in interactions:
                    formatted.append(f"- {warning['supplement']} con {warning['medication']}:")
                    formatted.append(f"  {warning['interaction']['recommendation']}")
        
        # Verificar dosis máximas
        dose_warnings = check_max_doses(supplements)
        if dose_warnings:
            formatted.append("\n⚠️ ADVERTENCIAS DE DOSIS:")
            for warning in dose_warnings:
                formatted.append(f"- {warning['supplement']}: Dosis actual {warning['current_dose']} excede máximo recomendado {warning['max_dose']}")
                if warning.get('side_effect'):
                    formatted.append(f"  Posible efecto: {warning['side_effect']}")
        
        # Identificar sinergias
        synergies = get_synergies(supplements)
        if synergies:
            formatted.append("\n💡 SINERGIAS BENEFICIOSAS:")
            for synergy in synergies:
                formatted.append(f"- {synergy['benefit']}")
                if synergy.get('recommendation'):
                    formatted.append(f"  Recomendación: {synergy['recommendation']}")
        
        return "\n".join(formatted)
    
    def _format_medications(self, medications: List[Dict]) -> str:
        """Formatea los medicamentos para el prompt"""
        if not medications:
            return ""
        
        formatted = ["MEDICACIÓN:"]
        impacts = []
        considerations = []
        has_t4_with_fiber = False
        
        for med in medications:
            formatted.append(f"- {med['name']}")
            if med.get('impact'):
                impacts.append(f"  • {med['name']}: {med['impact']}")
            if med.get('considerations'):
                considerations.append(f"  • {med['name']}: {med['considerations']}")
            
            # Detectar si es levotiroxina con timing de fibra
            if med['name'].lower() == 'levotiroxina' and med.get('t4_timing') == 'con_fibra_2h':
                has_t4_with_fiber = True
        
        if impacts:
            formatted.append("\nIMPACTOS NUTRICIONALES:")
            formatted.extend(impacts)
        
        if considerations:
            formatted.append("\nCONSIDERACIONES DIETÉTICAS:")
            formatted.extend(considerations)
        
        if has_t4_with_fiber:
            formatted.append("\n⚠️ IMPORTANTE - LEVOTIROXINA:")
            formatted.append("- El desayuno debe tomarse 2 HORAS después de la medicación")
            formatted.append("- Agregar esta nota en el DESAYUNO: '(2 hs post medicación)'")
        
        return "\n".join(formatted)
    
    def _format_meal_configuration(self, meal_config: Optional[Dict]) -> str:
        """Formatea la configuración de comidas para el prompt"""
        if not meal_config:
            return ""
        
        formatted = ["CONFIGURACIÓN DE COMIDAS:"]
        
        # Comidas principales
        principales = []
        if meal_config.get('brunch'):
            principales.append("Brunch (reemplaza desayuno y almuerzo)")
        else:
            if meal_config.get('desayuno'):
                principales.append("Desayuno")
            if meal_config.get('almuerzo'):
                principales.append("Almuerzo")
        
        if meal_config.get('drunch'):
            principales.append("Drunch (reemplaza merienda y cena)")
        else:
            if meal_config.get('merienda'):
                principales.append("Merienda")
            if meal_config.get('cena'):
                principales.append("Cena")
        
        if principales:
            formatted.append(f"- Comidas principales: {', '.join(principales)}")
        
        # Comidas adicionales
        adicionales = []
        if meal_config.get('media_manana'):
            adicionales.append("Media mañana")
        if meal_config.get('media_tarde'):
            adicionales.append("Media tarde")
        if meal_config.get('postre_almuerzo'):
            adicionales.append("Postre almuerzo")
        if meal_config.get('postre_cena'):
            adicionales.append("Postre cena")
        if meal_config.get('dulce_siesta'):
            adicionales.append("Dulce siesta")
        if meal_config.get('pre_entreno'):
            adicionales.append("Pre-entreno")
        if meal_config.get('post_entreno'):
            adicionales.append("Post-entreno")
        
        if adicionales:
            formatted.append(f"- Comidas adicionales: {', '.join(adicionales)}")
        
        # Alternativas
        alternativas = []
        if meal_config.get('alternativas_dulces'):
            alternativas.append("dulces")
        if meal_config.get('alternativas_saladas'):
            alternativas.append("saladas")
        
        if alternativas:
            formatted.append(f"- Incluir alternativas {' y '.join(alternativas)} para cada comida")
        
        return "\n".join(formatted)
    
    def format_recipes_by_meal_type(self, recipes_dict: Dict[str, List[Dict]]) -> str:
        """Format recipes organized by meal type for the prompt"""
        formatted_sections = []
        
        for meal_type, recipes in recipes_dict.items():
            if not recipes:
                continue
                
            formatted_sections.append(f"\n=== RECETAS PARA {meal_type.upper()} ===")
            
            for recipe in recipes:
                # Format as summary with ID prominent
                summary = (
                    f"[{recipe['id']}] {recipe['nombre']} | "
                    f"{recipe.get('calorias_aprox', 0)} kcal | "
                    f"P: {recipe.get('proteinas_aprox', 0)}g | "
                    f"C: {recipe.get('carbohidratos_aprox', 0)}g | "
                    f"G: {recipe.get('grasas_aprox', 0)}g"
                )
                formatted_sections.append(summary)
        
        return "\n".join(formatted_sections)
    
    def format_recipe_details(self, recipes_list: List[Dict]) -> str:
        """Format full recipe details in a separate section"""
        formatted_details = ["\n=== DETALLES DE RECETAS ==="]
        
        for recipe in recipes_list:
            ingredients = " | ".join([
                f"{ing['item']}: {ing['cantidad']}"
                for ing in recipe.get('ingredientes', [])
            ])
            
            detail = f"""
[{recipe['id']}] {recipe['nombre']}
Ingredientes: {ingredients}
Preparación: {recipe.get('preparacion', '')}
"""
            formatted_details.append(detail)
        
        return "\n".join(formatted_details)
    
    def _format_pathologies_and_medications(self, patient_data: NewPatientRequest) -> str:
        """Formatea las patologías y medicamentos de manera integrada"""
        formatted = []
        
        # Detectar patologías
        detected_pathologies = []
        if patient_data.patologias:
            detected_pathologies = detect_pathologies_from_text(patient_data.patologias)
        
        # Si hay patologías detectadas
        if detected_pathologies:
            formatted.append("\nPATOLOGÍAS DETECTADAS:")
            
            for pathology in detected_pathologies:
                info = get_pathology_info(pathology)
                if info:
                    formatted.append(f"- {info['name']}")
                    
                    # Agregar ajustes nutricionales
                    if 'nutritional_adjustments' in info:
                        adjustments = info['nutritional_adjustments']
                        if adjustments.get('calories_adjustment', 0) != 0:
                            formatted.append(f"  • Ajuste calórico: {adjustments['calories_adjustment']} kcal")
                        if 'carbs_percentage' in adjustments:
                            formatted.append(f"  • Distribución de macros ajustada")
                        if 'min_carbs_grams' in adjustments and adjustments['min_carbs_grams'] > 130:
                            formatted.append(f"  • Carbohidratos mínimos: {adjustments['min_carbs_grams']}g/día")
                        if 'sodium_max' in adjustments:
                            formatted.append(f"  • Sodio máximo: {adjustments['sodium_max']}mg/día")
            
            # Restricciones dietéticas combinadas
            all_restrictions = get_all_dietary_restrictions(detected_pathologies)
            if all_restrictions:
                formatted.append("\nRESTRICCIONES ALIMENTARIAS:")
                for restriction in all_restrictions:
                    formatted.append(f"- EVITAR: {restriction}")
            
            # Tags de recetas
            avoid_tags = get_recipe_tags_to_avoid(detected_pathologies)
            prefer_tags = get_recipe_tags_to_prefer(detected_pathologies)
            
            if avoid_tags:
                formatted.append("\nTIPOS DE RECETAS A EVITAR:")
                formatted.append(f"- {', '.join(avoid_tags)}")
            
            if prefer_tags:
                formatted.append("\nTIPOS DE RECETAS PREFERIDAS:")
                formatted.append(f"- {', '.join(prefer_tags)}")
            
            # Consideraciones especiales
            formatted.append("\nCONSIDERACIONES ESPECIALES:")
            for pathology in detected_pathologies:
                info = get_pathology_info(pathology)
                if info and 'special_considerations' in info:
                    for consideration in info['special_considerations']:
                        formatted.append(f"- {consideration}")
        
        # Medicamentos
        if patient_data.medications:
            formatted.append("\n")
            formatted.append(self._format_medications(patient_data.medications))
        
        # Si no hay patologías ni medicamentos
        if not detected_pathologies and not patient_data.medications:
            formatted.append("- Patologías/Medicación: Sin patologías ni medicación")
        
        return "\n".join(formatted)
    
    def validate_recipe_usage(self, meal_plan_text: str, valid_recipe_ids: List[str]) -> bool:
        """Validate that the meal plan uses only valid recipe IDs"""
        # Find all recipe IDs in the meal plan
        recipe_id_pattern = r'\[REC_\d{4}\]'
        found_ids = re.findall(recipe_id_pattern, meal_plan_text)
        
        # Clean up IDs (remove brackets)
        found_ids = [id.strip('[]') for id in found_ids]
        
        # Check if all found IDs are valid
        invalid_ids = [id for id in found_ids if id not in valid_recipe_ids]
        
        if invalid_ids:
            logger.warning(f"Invalid recipe IDs found: {invalid_ids}")
            return False
        
        # Check if at least some recipes were used
        if len(found_ids) < 3:  # At least 3 meals should have recipes
            logger.warning("Too few recipes used in meal plan")
            return False
        
        return True
    
    def extract_used_recipes(self, meal_plan_text: str) -> List[str]:
        """Extract recipe IDs used in a meal plan"""
        recipe_id_pattern = r'\[REC_\d{4}\]'
        found_ids = re.findall(recipe_id_pattern, meal_plan_text)
        # Clean up IDs (remove brackets) and remove duplicates
        return list(set([id.strip('[]') for id in found_ids]))