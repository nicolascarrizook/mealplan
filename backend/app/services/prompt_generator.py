from typing import Dict, List, Optional

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
9. Respetar horarios del paciente
10. Adaptarse al nivel económico
"""

    def generate_motor1_prompt(self, patient_data, recipes_json):
        """Motor 1: Paciente Nuevo"""
        
        prompt = f"""
{self.base_rules}

MOTOR 1 - PACIENTE NUEVO
Generá un plan alimentario de 3 días iguales siguiendo el método.

DATOS DEL PACIENTE:
- Nombre: {patient_data.nombre}
- Edad: {patient_data.edad} años
- Sexo: {patient_data.sexo}
- Estatura: {patient_data.estatura} cm
- Peso: {patient_data.peso} kg
- IMC: {patient_data.imc}
- Objetivo: {patient_data.objetivo} {patient_data.objetivo_semanal or ''}

ACTIVIDAD FÍSICA:
- Tipo: {patient_data.tipo_actividad}
- Frecuencia: {patient_data.frecuencia_semanal}x por semana
- Duración: {patient_data.duracion_sesion} minutos

ESPECIFICACIONES MÉDICAS:
- Suplementación: {patient_data.suplementacion or 'Ninguna'}
- Patologías/Medicación: {patient_data.patologias or 'Sin patologías'}
- NO consume: {patient_data.no_consume or 'Sin restricciones'}
- Le gusta: {patient_data.le_gusta}
- Nivel económico: {patient_data.nivel_economico}

HORARIOS:
{self._format_horarios(patient_data.horarios)}

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

DESAYUNO (horario)
- [Nombre de la receta de la base de datos]
- Ingredientes con cantidades ajustadas:
  * Ingrediente 1: XXg
  * Ingrediente 2: XXg
- Preparación: [de la receta]

ALMUERZO (horario)
[Mismo formato]

MERIENDA (horario)
[Mismo formato]

CENA (horario)
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

    def _format_horarios(self, horarios: Dict[str, str]) -> str:
        """Formatea los horarios del paciente"""
        if not horarios:
            return "- No especificados"
        
        formatted = []
        for comida, hora in horarios.items():
            formatted.append(f"- {comida.capitalize()}: {hora}")
        
        return "\n".join(formatted)