"""
Módulo de embarazo - Adaptación del plan alimentario según embarazo
Compatible con el método Tres Días y Carga | Dieta Inteligente® & Nutrición Evolutiva
"""

from typing import Dict, List, Optional, Tuple, Any
from app.data.pathologies import (
    PathologyType, 
    get_pathology_info, 
    detect_pathologies_from_text,
    is_pregnancy_pathology,
    get_pregnancy_info
)


class PregnancyManager:
    """Maneja los ajustes nutricionales y recomendaciones para embarazo"""
    
    def __init__(self):
        self.activation_phrases = [
            "está embarazada",
            "cursa el", "trimestre",
            "embarazo semana",
            "gestación",
            "paciente embarazada",
            "actualizar plan durante el embarazo",
            "plan adaptado al embarazo"
        ]
    
    def detect_pregnancy(self, patient_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Detecta si hay embarazo basándose en los datos del paciente
        Retorna información del embarazo o None
        """
        # Verificar en patologías
        pathologies_text = patient_data.get("patologias", "")
        detected_pathologies = detect_pathologies_from_text(pathologies_text)
        
        # Verificar si hay patologías de embarazo
        pregnancy_info = get_pregnancy_info(detected_pathologies)
        if pregnancy_info:
            return pregnancy_info
        
        # Verificar en el PROM (campo adicional si existe)
        prom = patient_data.get("prom", "")
        if prom and any(phrase in prom.lower() for phrase in self.activation_phrases):
            # Intentar detectar desde el PROM
            detected_from_prom = detect_pathologies_from_text(prom)
            pregnancy_info = get_pregnancy_info(detected_from_prom)
            if pregnancy_info:
                return pregnancy_info
        
        return None
    
    def get_trimester_adjustments(self, trimester: str) -> Dict[str, Any]:
        """Obtiene los ajustes específicos por trimestre"""
        trimester_map = {
            "embarazo_primer_trimestre": PathologyType.EMBARAZO_PRIMER_TRIMESTRE,
            "embarazo_segundo_trimestre": PathologyType.EMBARAZO_SEGUNDO_TRIMESTRE,
            "embarazo_tercer_trimestre": PathologyType.EMBARAZO_TERCER_TRIMESTRE
        }
        
        pathology_type = trimester_map.get(trimester)
        if pathology_type:
            return get_pathology_info(pathology_type)
        
        # Por defecto, segundo trimestre
        return get_pathology_info(PathologyType.EMBARAZO_SEGUNDO_TRIMESTRE)
    
    def calculate_pregnancy_requirements(
        self, 
        base_calories: float,
        weight: float,
        pregestational_weight: Optional[float],
        trimester: str,
        additional_conditions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Calcula los requerimientos nutricionales específicos para embarazo
        """
        # Obtener ajustes del trimestre
        trimester_info = self.get_trimester_adjustments(trimester)
        adjustments = trimester_info.get("nutritional_adjustments", {})
        
        # Calcular calorías ajustadas
        adjusted_calories = base_calories + adjustments.get("calories_adjustment", 0)
        
        # Calcular proteínas
        weight_for_protein = pregestational_weight if trimester == "embarazo_primer_trimestre" and pregestational_weight else weight
        protein_per_kg = adjustments.get("protein_g_per_kg", 1.2)
        total_protein_g = weight_for_protein * protein_per_kg
        
        # Distribución de macros
        carbs_percentage = adjustments.get("carbs_percentage", 50)
        protein_percentage = adjustments.get("protein_percentage", 20)
        fat_percentage = adjustments.get("fat_percentage", 30)
        
        # Verificar carbohidratos mínimos (evitar cetosis)
        min_carbs_g = adjustments.get("min_carbs_grams", 175)
        carbs_from_percentage = (adjusted_calories * carbs_percentage / 100) / 4
        if carbs_from_percentage < min_carbs_g:
            # Ajustar para cumplir mínimo
            carbs_calories = min_carbs_g * 4
            carbs_percentage = (carbs_calories / adjusted_calories) * 100
            # Reajustar otros macros proporcionalmente
            remaining_percentage = 100 - carbs_percentage
            protein_percentage = (protein_percentage / (protein_percentage + fat_percentage)) * remaining_percentage
            fat_percentage = remaining_percentage - protein_percentage
        
        # Manejar condiciones adicionales
        if additional_conditions:
            if "diabetes_gestacional" in additional_conditions:
                # Ajustes para diabetes gestacional
                dg_info = get_pathology_info(PathologyType.DIABETES_GESTACIONAL)
                dg_adjustments = dg_info.get("nutritional_adjustments", {})
                # Usar distribución más restrictiva de carbohidratos
                carbs_percentage = min(carbs_percentage, dg_adjustments.get("carbs_percentage", 40))
                protein_percentage = dg_adjustments.get("protein_percentage", 30)
                fat_percentage = 100 - carbs_percentage - protein_percentage
        
        # Calcular gramos de macros
        carbs_g = (adjusted_calories * carbs_percentage / 100) / 4
        protein_g = max(total_protein_g, (adjusted_calories * protein_percentage / 100) / 4)
        fat_g = (adjusted_calories * fat_percentage / 100) / 9
        
        # Micronutrientes importantes
        micronutrients = {
            "folic_acid_mcg": adjustments.get("folic_acid_mcg", 600),
            "iron_mg": adjustments.get("iron_mg", 27),
            "calcium_mg": adjustments.get("calcium_mg", 1000),
            "vitamin_d_iu": adjustments.get("vitamin_d_iu", 600)
        }
        
        return {
            "adjusted_calories": round(adjusted_calories),
            "macros": {
                "carbs_g": round(carbs_g),
                "carbs_percentage": round(carbs_percentage),
                "protein_g": round(protein_g),
                "protein_percentage": round(protein_percentage),
                "fat_g": round(fat_g),
                "fat_percentage": round(fat_percentage)
            },
            "micronutrients": micronutrients,
            "min_carbs_g": min_carbs_g,
            "meal_distribution": trimester_info.get("meal_distribution", {}),
            "special_considerations": trimester_info.get("special_considerations", [])
        }
    
    def get_pregnancy_prompt_section(self, pregnancy_info: Dict[str, Any], requirements: Dict[str, Any]) -> str:
        """
        Genera la sección del prompt específica para embarazo
        """
        trimester_name = pregnancy_info.get("name", "Embarazo")
        additional_conditions = pregnancy_info.get("additional_conditions", [])
        
        prompt = f"\n## 🧬 EMBARAZO - CONSIDERACIONES ESPECIALES\n\n"
        prompt += f"**Estado actual**: {trimester_name}\n"
        
        if additional_conditions:
            prompt += f"**Condiciones adicionales**: {', '.join(additional_conditions)}\n"
        
        prompt += f"\n### Requerimientos Nutricionales Ajustados:\n"
        prompt += f"- **Calorías totales**: {requirements['adjusted_calories']} kcal/día\n"
        prompt += f"- **Distribución de macros**:\n"
        prompt += f"  - Carbohidratos: {requirements['macros']['carbs_g']}g ({requirements['macros']['carbs_percentage']}%)\n"
        prompt += f"  - Proteínas: {requirements['macros']['protein_g']}g ({requirements['macros']['protein_percentage']}%)\n"
        prompt += f"  - Grasas: {requirements['macros']['fat_g']}g ({requirements['macros']['fat_percentage']}%)\n"
        prompt += f"\n**⚠️ IMPORTANTE**: Mínimo {requirements['min_carbs_g']}g de carbohidratos por día para evitar cetosis\n"
        
        # Micronutrientes
        prompt += f"\n### Micronutrientes Esenciales:\n"
        for nutrient, value in requirements['micronutrients'].items():
            nutrient_name = nutrient.replace("_", " ").title()
            prompt += f"- {nutrient_name}: {value}\n"
        
        # Distribución de comidas
        prompt += f"\n### Distribución de Comidas Recomendada:\n"
        for meal, percentage in requirements['meal_distribution'].items():
            meal_name = meal.replace("_", " ").title()
            prompt += f"- {meal_name}: {percentage}%\n"
        
        # Consideraciones especiales
        prompt += f"\n### Consideraciones Especiales:\n"
        for consideration in requirements['special_considerations']:
            prompt += f"- {consideration}\n"
        
        # Restricciones alimentarias
        dietary_restrictions = pregnancy_info.get("dietary_restrictions", [])
        if dietary_restrictions:
            prompt += f"\n### Alimentos a EVITAR:\n"
            for restriction in dietary_restrictions:
                prompt += f"- {restriction}\n"
        
        # Manejo de síntomas específicos
        if "nausea_management" in pregnancy_info:
            prompt += f"\n### Manejo de Náuseas y Malestar:\n"
            nausea_info = pregnancy_info["nausea_management"]
            prompt += f"- **Alimentos matutinos**: {', '.join(nausea_info['morning_foods'])}\n"
            prompt += f"- **Evitar texturas**: {', '.join(nausea_info['avoid_textures'])}\n"
            prompt += f"- **Temperaturas preferidas**: {', '.join(nausea_info['preferred_temps'])}\n"
            prompt += f"- **Hidratación**: {nausea_info['hydration']}\n"
        
        if "reflux_management" in pregnancy_info:
            prompt += f"\n### Manejo del Reflujo:\n"
            reflux_info = pregnancy_info["reflux_management"]
            prompt += f"- **Evitar**: {', '.join(reflux_info['avoid_foods'])}\n"
            prompt += f"- **Horarios**: {reflux_info['meal_timing']}\n"
            prompt += f"- **Porciones**: {reflux_info['portions']}\n"
        
        # Instrucciones para el plan
        prompt += "\n### INSTRUCCIONES PARA EL PLAN:\n"
        prompt += "1. **Seguridad alimentaria**: Asegurar que todas las carnes estén bien cocidas, evitar lácteos no pasteurizados\n"
        prompt += "2. **Hidratación**: Incluir recomendaciones de agua (8-10 vasos/día)\n"
        prompt += "3. **Suplementación**: Recordar la importancia de suplementos prenatales\n"
        prompt += "4. **Frecuencia**: Respetar la distribución de comidas para evitar ayunos prolongados\n"
        prompt += "5. **Calidad**: Priorizar alimentos nutritivos y de fácil digestión\n"
        prompt += "6. **NO CETOSIS**: Ningún día debe tener menos de 175g de carbohidratos\n"
        
        if "diabetes_gestacional" in additional_conditions:
            prompt += "\n### Control de Diabetes Gestacional:\n"
            prompt += "- Incluir proteína o grasa saludable en CADA comida\n"
            prompt += "- Limitar carbohidratos por comida: máximo 45g en principales, 20g en colaciones\n"
            prompt += "- Evitar jugos de fruta y azúcares simples\n"
            prompt += "- Preferir carbohidratos complejos con bajo índice glucémico\n"
        
        return prompt
    
    def validate_meal_plan_for_pregnancy(self, meal_plan: Dict[str, Any], requirements: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida que un plan de comidas cumpla con los requerimientos del embarazo
        Retorna (es_válido, lista_de_problemas)
        """
        issues = []
        
        # Verificar carbohidratos mínimos por día
        min_carbs = requirements.get("min_carbs_g", 175)
        
        for day in ["day1", "day2", "day3"]:
            if day in meal_plan:
                day_carbs = 0
                for meal in meal_plan[day].get("meals", {}).values():
                    if isinstance(meal, dict) and "macros" in meal:
                        day_carbs += meal["macros"].get("carbs", 0)
                
                if day_carbs < min_carbs:
                    issues.append(f"{day}: Carbohidratos insuficientes ({day_carbs}g < {min_carbs}g mínimo)")
        
        # Verificar que no haya ayunos prolongados
        expected_meals = len(requirements.get("meal_distribution", {}))
        for day in ["day1", "day2", "day3"]:
            if day in meal_plan:
                actual_meals = len(meal_plan[day].get("meals", {}))
                if actual_meals < expected_meals:
                    issues.append(f"{day}: Número insuficiente de comidas ({actual_meals} < {expected_meals} recomendadas)")
        
        return len(issues) == 0, issues
    
    def get_recipe_filters_for_pregnancy(self, pregnancy_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Obtiene filtros específicos para recetas según el embarazo
        """
        avoid_tags = pregnancy_info.get("recipe_tags_avoid", [])
        prefer_tags = pregnancy_info.get("recipe_tags_prefer", [])
        
        # Agregar tags adicionales según condiciones
        additional_conditions = pregnancy_info.get("additional_conditions", [])
        
        if "diabetes_gestacional" in additional_conditions:
            avoid_tags.extend(["alto_ig", "azucarado"])
            prefer_tags.extend(["bajo_ig", "proteico"])
        
        if "hipertension_gestacional" in additional_conditions or "preeclampsia" in additional_conditions:
            avoid_tags.extend(["alto_sodio", "procesado"])
            prefer_tags.extend(["bajo_sodio", "potasio"])
        
        # Eliminar duplicados
        avoid_tags = list(set(avoid_tags))
        prefer_tags = list(set(prefer_tags))
        
        return {
            "avoid": avoid_tags,
            "prefer": prefer_tags
        }