"""
Sistema de validación para planes alimentarios según las reglas del sistema Tres Días y Carga
"""

from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class MealPlanValidator:
    """Validador de planes alimentarios según reglas estrictas del sistema"""
    
    def __init__(self, tolerance: float = 0.05):
        """
        Inicializa el validador con tolerancia para equivalencias
        
        Args:
            tolerance: Porcentaje de tolerancia (default 5% = 0.05)
        """
        self.tolerance = tolerance
    
    def validate_option_equivalence(
        self, 
        options: List[Dict[str, float]], 
        meal_name: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida que las 3 opciones de una comida sean equivalentes (±5%)
        
        Args:
            options: Lista de diccionarios con macros de cada opción
                    [{'calories': X, 'protein': X, 'carbs': X, 'fat': X}, ...]
            meal_name: Nombre de la comida para mensajes de error
            
        Returns:
            (is_valid, error_message)
        """
        if len(options) != 3:
            return False, f"{meal_name}: Debe tener exactamente 3 opciones"
        
        # Tomar la primera opción como referencia
        reference = options[0]
        
        for i, option in enumerate(options[1:], 2):
            # Validar cada macro
            for macro in ['calories', 'protein', 'carbs', 'fat']:
                ref_value = reference.get(macro, 0)
                opt_value = option.get(macro, 0)
                
                if ref_value == 0:
                    if opt_value != 0:
                        return False, f"{meal_name} - Opción {i}: {macro} no puede ser 0 en referencia y {opt_value} en opción"
                    continue
                
                # Calcular diferencia porcentual
                diff_percentage = abs((opt_value - ref_value) / ref_value)
                
                if diff_percentage > self.tolerance:
                    return False, (
                        f"{meal_name} - Opción {i}: {macro} fuera de rango. "
                        f"Referencia: {ref_value}, Opción: {opt_value} "
                        f"(diferencia: {diff_percentage*100:.1f}%, máximo permitido: {self.tolerance*100}%)"
                    )
        
        return True, None
    
    def validate_equitable_distribution(
        self, 
        meals: Dict[str, Dict[str, float]]
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida que todas las comidas principales tengan distribución equitativa
        
        Args:
            meals: Diccionario con macros de cada comida principal
                  {'desayuno': {...}, 'almuerzo': {...}, ...}
                  
        Returns:
            (is_valid, error_message)
        """
        main_meals = ['desayuno', 'almuerzo', 'merienda', 'cena']
        
        # Filtrar solo comidas principales que existan
        existing_meals = {k: v for k, v in meals.items() if k in main_meals}
        
        if len(existing_meals) < 2:
            return True, None  # No hay suficientes comidas para comparar
        
        # Tomar la primera comida como referencia
        reference_name = list(existing_meals.keys())[0]
        reference = existing_meals[reference_name]
        
        for meal_name, meal_macros in existing_meals.items():
            if meal_name == reference_name:
                continue
                
            # Validar cada macro
            for macro in ['calories', 'protein', 'carbs', 'fat']:
                ref_value = reference.get(macro, 0)
                meal_value = meal_macros.get(macro, 0)
                
                if ref_value == 0:
                    if meal_value != 0:
                        return False, f"Distribución no equitativa: {reference_name} tiene {macro}=0 pero {meal_name} tiene {meal_value}"
                    continue
                
                # Calcular diferencia porcentual
                diff_percentage = abs((meal_value - ref_value) / ref_value)
                
                if diff_percentage > self.tolerance:
                    return False, (
                        f"Distribución no equitativa entre {reference_name} y {meal_name}. "
                        f"{macro}: {ref_value} vs {meal_value} "
                        f"(diferencia: {diff_percentage*100:.1f}%, máximo permitido: {self.tolerance*100}%)"
                    )
        
        return True, None
    
    def validate_collation_structure(
        self,
        collations: List[Dict[str, float]],
        main_meal_avg: Dict[str, float]
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida que las colaciones sean más livianas que las comidas principales
        
        Args:
            collations: Lista con macros de cada colación
            main_meal_avg: Promedio de macros de comidas principales
            
        Returns:
            (is_valid, error_message)
        """
        if not collations:
            return True, None
        
        main_meal_calories = main_meal_avg.get('calories', 0)
        
        for i, collation in enumerate(collations, 1):
            collation_calories = collation.get('calories', 0)
            
            # Las colaciones deben tener menos calorías que las comidas principales
            if collation_calories >= main_meal_calories * 0.8:  # Máximo 80% de una comida principal
                return False, (
                    f"Colación {i} tiene {collation_calories} cal, "
                    f"lo cual es muy cercano o superior a las comidas principales ({main_meal_calories} cal). "
                    f"Las colaciones deben ser más livianas."
                )
        
        return True, None
    
    def validate_complete_meal_plan(
        self,
        meal_plan: Dict[str, List[Dict[str, float]]],
        distribution_type: str = "standard"
    ) -> Tuple[bool, List[str]]:
        """
        Valida un plan completo según todas las reglas
        
        Args:
            meal_plan: Diccionario con todas las comidas y sus opciones
                      {'desayuno': [opt1, opt2, opt3], 'almuerzo': [...], ...}
            distribution_type: "equitable" o "standard"
            
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # 1. Validar equivalencia entre opciones de cada comida
        for meal_name, options in meal_plan.items():
            if meal_name.startswith('colacion'):
                continue  # Las colaciones se validan por separado
                
            is_valid, error = self.validate_option_equivalence(options, meal_name)
            if not is_valid:
                errors.append(error)
        
        # 2. Si es distribución equitativa, validar igualdad entre comidas principales
        if distribution_type == "equitable":
            # Tomar la primera opción de cada comida para comparar
            main_meals = {}
            for meal_name in ['desayuno', 'almuerzo', 'merienda', 'cena']:
                if meal_name in meal_plan and meal_plan[meal_name]:
                    main_meals[meal_name] = meal_plan[meal_name][0]
            
            is_valid, error = self.validate_equitable_distribution(main_meals)
            if not is_valid:
                errors.append(error)
        
        # 3. Validar estructura de colaciones
        collations = []
        main_meal_totals = []
        
        for meal_name, options in meal_plan.items():
            if meal_name.startswith('colacion') and options:
                collations.extend(options)
            elif meal_name in ['desayuno', 'almuerzo', 'merienda', 'cena'] and options:
                main_meal_totals.append(options[0])
        
        if collations and main_meal_totals:
            # Calcular promedio de comidas principales
            main_meal_avg = {
                'calories': sum(m.get('calories', 0) for m in main_meal_totals) / len(main_meal_totals),
                'protein': sum(m.get('protein', 0) for m in main_meal_totals) / len(main_meal_totals),
                'carbs': sum(m.get('carbs', 0) for m in main_meal_totals) / len(main_meal_totals),
                'fat': sum(m.get('fat', 0) for m in main_meal_totals) / len(main_meal_totals)
            }
            
            is_valid, error = self.validate_collation_structure(collations, main_meal_avg)
            if not is_valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    def generate_validation_report(
        self,
        meal_plan: Dict[str, List[Dict[str, float]]],
        distribution_type: str = "standard"
    ) -> str:
        """
        Genera un reporte detallado de validación
        
        Args:
            meal_plan: Plan completo a validar
            distribution_type: Tipo de distribución
            
        Returns:
            Reporte en formato string
        """
        is_valid, errors = self.validate_complete_meal_plan(meal_plan, distribution_type)
        
        report = "📋 REPORTE DE VALIDACIÓN DEL PLAN ALIMENTARIO\n"
        report += "=" * 50 + "\n\n"
        
        if is_valid:
            report += "✅ PLAN VÁLIDO: Cumple con todas las reglas del sistema\n\n"
            
            # Mostrar resumen de equivalencias
            report += "📊 Resumen de equivalencias:\n"
            for meal_name, options in meal_plan.items():
                if options:
                    ref_cal = options[0].get('calories', 0)
                    report += f"- {meal_name.capitalize()}: ~{ref_cal:.0f} cal por opción\n"
        else:
            report += "❌ PLAN INVÁLIDO: Se encontraron los siguientes errores:\n\n"
            for i, error in enumerate(errors, 1):
                report += f"{i}. {error}\n"
            
            report += "\n⚠️ El plan debe ser corregido antes de entregarse al paciente.\n"
        
        return report