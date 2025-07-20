"""
Cálculos nutricionales y de macronutrientes
"""

from typing import Dict, Tuple
from ..schemas.meal_plan import NewPatientRequest, Objetivo, ProteinLevel

class NutritionalCalculator:
    """Calculadora de requerimientos nutricionales"""
    
    @staticmethod
    def calculate_bmr(patient: NewPatientRequest) -> float:
        """
        Calcula el BMR (Basal Metabolic Rate) usando la ecuación de Mifflin-St Jeor
        """
        if patient.sexo.value == "masculino":
            bmr = 10 * patient.peso + 6.25 * patient.estatura - 5 * patient.edad + 5
        else:
            bmr = 10 * patient.peso + 6.25 * patient.estatura - 5 * patient.edad - 161
        
        return bmr
    
    @staticmethod
    def get_activity_factor(tipo_actividad: str, frecuencia: int, duracion: int) -> float:
        """
        Calcula el factor de actividad basado en tipo, frecuencia y duración
        """
        if tipo_actividad.lower() in ["sedentario", "ninguna"]:
            return 1.2
        
        # Calcular horas semanales de actividad
        horas_semanales = (frecuencia * duracion) / 60
        
        if horas_semanales < 3:
            return 1.375  # Actividad ligera
        elif horas_semanales < 5:
            return 1.55   # Actividad moderada
        elif horas_semanales < 7:
            return 1.725  # Actividad alta
        else:
            return 1.9    # Actividad muy alta
    
    @staticmethod
    def calculate_daily_calories(patient: NewPatientRequest) -> float:
        """
        Calcula las calorías diarias necesarias según el objetivo
        """
        bmr = NutritionalCalculator.calculate_bmr(patient)
        activity_factor = NutritionalCalculator.get_activity_factor(
            patient.tipo_actividad,
            patient.frecuencia_semanal,
            patient.duracion_sesion
        )
        
        tdee = bmr * activity_factor
        
        # Ajustar según objetivo
        objetivo_adjustments = {
            Objetivo.mantener: 0,
            Objetivo.bajar_025: -250,
            Objetivo.bajar_05: -500,
            Objetivo.bajar_075: -750,
            Objetivo.bajar_1: -1000,
            Objetivo.subir_025: 250,
            Objetivo.subir_05: 500,
            Objetivo.subir_075: 750,
            Objetivo.subir_1: 1000,
        }
        
        adjustment = objetivo_adjustments.get(patient.objetivo, 0)
        
        # Ajustes adicionales por patologías
        if patient.patologias:
            pathologies_lower = patient.patologias.lower()
            if "diabetes" in pathologies_lower or "resistencia a la insulina" in pathologies_lower:
                # Reducir ligeramente las calorías para mejorar sensibilidad a insulina
                adjustment -= 100
            elif "hipotiroidismo" in pathologies_lower:
                # Reducir calorías por metabolismo más lento
                adjustment -= 150
        
        return round(tdee + adjustment)
    
    @staticmethod
    def get_protein_grams_per_kg(protein_level: ProteinLevel) -> float:
        """
        Retorna los gramos de proteína por kg de peso corporal según el nivel
        """
        protein_ranges = {
            ProteinLevel.muy_baja: 0.65,      # Promedio de 0.5-0.8
            ProteinLevel.conservada: 1.0,      # Promedio de 0.8-1.2
            ProteinLevel.moderada: 1.4,        # Promedio de 1.2-1.6
            ProteinLevel.alta: 1.9,            # Promedio de 1.6-2.2
            ProteinLevel.muy_alta: 2.5,        # Promedio de 2.2-2.8
            ProteinLevel.extrema: 3.2,         # Promedio de 3.0-3.5
        }
        return protein_ranges.get(protein_level, 1.0)
    
    @staticmethod
    def calculate_macro_distribution(patient: NewPatientRequest) -> Dict[str, float]:
        """
        Calcula la distribución de macronutrientes personalizada
        """
        daily_calories = NutritionalCalculator.calculate_daily_calories(patient)
        
        # Si hay personalización de macros, usarla
        if patient.protein_level or patient.carbs_percentage is not None or patient.fat_percentage:
            return NutritionalCalculator._calculate_custom_macros(patient, daily_calories)
        
        # Distribución por defecto según objetivo
        if "bajar" in patient.objetivo.value:
            # Para pérdida de peso: más proteína, menos carbohidratos
            distribution = {
                "proteinas": 0.30,
                "carbohidratos": 0.40,
                "grasas": 0.30
            }
        elif "subir" in patient.objetivo.value:
            # Para ganancia de peso: más carbohidratos
            distribution = {
                "proteinas": 0.20,
                "carbohidratos": 0.50,
                "grasas": 0.30
            }
        else:
            # Mantenimiento: distribución balanceada
            distribution = {
                "proteinas": 0.25,
                "carbohidratos": 0.45,
                "grasas": 0.30
            }
        
        # Ajustes por patologías
        if patient.patologias:
            pathologies_lower = patient.patologias.lower()
            if any(cond in pathologies_lower for cond in ["diabetes", "resistencia a la insulina", "hígado graso"]):
                # Reducir carbohidratos, aumentar proteína
                distribution["carbohidratos"] = 0.35
                distribution["proteinas"] = 0.35
                distribution["grasas"] = 0.30
        
        return distribution
    
    @staticmethod
    def _calculate_custom_macros(patient: NewPatientRequest, daily_calories: float) -> Dict[str, float]:
        """
        Calcula macros personalizados según las preferencias del usuario
        """
        # Paso 1: Calcular proteína
        if patient.protein_level:
            protein_g_per_kg = NutritionalCalculator.get_protein_grams_per_kg(patient.protein_level)
            total_protein_g = patient.peso * protein_g_per_kg
            protein_calories = total_protein_g * 4
            protein_percentage = min(protein_calories / daily_calories, 0.40)  # Máximo 40%
        else:
            protein_percentage = 0.25  # Default
        
        # Paso 2: Usar carbohidratos directos si se especifican
        if patient.carbs_percentage is not None:
            carbs_percentage = patient.carbs_percentage / 100
        else:
            # Carbohidratos por defecto según objetivo
            if "bajar" in patient.objetivo.value:
                carbs_percentage = 0.40
            elif "subir" in patient.objetivo.value:
                carbs_percentage = 0.50
            else:
                carbs_percentage = 0.45
        
        # Paso 3: Calcular grasas
        if patient.fat_percentage is not None:
            fat_percentage = patient.fat_percentage / 100
        else:
            # Calcular grasas como el restante
            fat_percentage = 1.0 - protein_percentage - carbs_percentage
        
        # Validar que sumen 100% (con tolerancia)
        total = protein_percentage + carbs_percentage + fat_percentage
        if abs(total - 1.0) > 0.02:  # 2% de tolerancia
            # Ajustar grasas para que sume 100%
            fat_percentage = 1.0 - protein_percentage - carbs_percentage
        
        # Asegurar que las grasas estén en rango válido (15-45%)
        fat_percentage = max(0.15, min(0.45, fat_percentage))
        
        return {
            "proteinas": round(protein_percentage, 2),
            "carbohidratos": round(carbs_percentage, 2),
            "grasas": round(fat_percentage, 2)
        }
    
    @staticmethod
    def calculate_meal_distribution(
        daily_calories: float, 
        meals_per_day: int, 
        distribution_type: str,
        include_snacks: bool = False,
        custom_distribution: Optional[Dict[str, Dict[str, float]]] = None
    ) -> Dict[str, float]:
        """
        Calcula la distribución de calorías entre las comidas
        """
        if distribution_type == "custom" and custom_distribution:
            # Usar distribución personalizada
            distribution = {}
            for meal, data in custom_distribution.items():
                if isinstance(data, dict) and 'calories' in data:
                    distribution[meal] = data['calories']
            return distribution
        elif distribution_type == "equitable":
            # Distribución equitativa
            calories_per_meal = daily_calories / meals_per_day
            if meals_per_day == 3:
                distribution = {
                    "desayuno": calories_per_meal,
                    "almuerzo": calories_per_meal,
                    "cena": calories_per_meal
                }
            else:  # 4 comidas
                distribution = {
                    "desayuno": calories_per_meal,
                    "almuerzo": calories_per_meal,
                    "merienda": calories_per_meal,
                    "cena": calories_per_meal
                }
        else:
            # Distribución tradicional
            if meals_per_day == 3:
                distribution = {
                    "desayuno": daily_calories * 0.30,
                    "almuerzo": daily_calories * 0.40,
                    "cena": daily_calories * 0.30
                }
            else:  # 4 comidas
                distribution = {
                    "desayuno": daily_calories * 0.25,
                    "almuerzo": daily_calories * 0.35,
                    "merienda": daily_calories * 0.15,
                    "cena": daily_calories * 0.25
                }
        
        # Si hay colaciones, restar 10-15% del total y redistribuir
        if include_snacks:
            snack_calories = daily_calories * 0.10
            # Reducir proporcionalmente cada comida
            for meal in distribution:
                distribution[meal] *= 0.90
            distribution["colacion"] = snack_calories
        
        # Redondear valores
        return {meal: round(calories) for meal, calories in distribution.items()}