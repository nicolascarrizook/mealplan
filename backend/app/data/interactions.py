# Sistema de interacciones medicamento-suplemento
# Basado en las indicaciones del nutricionista para manejo seguro

from typing import Dict, List, Optional

# Diccionario de interacciones: medicamento -> suplemento -> información
DRUG_SUPPLEMENT_INTERACTIONS = {
    "levotiroxina": {
        "fiber_supplement": {
            "separation_hours": 4,
            "reason": "La fibra puede interferir con la absorción de levotiroxina",
            "severity": "high",
            "recommendation": "Tomar la fibra al menos 4 horas después de la levotiroxina"
        },
        "omega3_epa_dha": {
            "separation_hours": 1,
            "reason": "Puede afectar ligeramente la absorción",
            "severity": "moderate",
            "recommendation": "Separar al menos 1 hora de la toma de levotiroxina"
        },
        "magnesium_supplement": {
            "separation_hours": 4,
            "reason": "El magnesio puede reducir la absorción de hormona tiroidea",
            "severity": "high",
            "recommendation": "Separar al menos 4 horas de la levotiroxina"
        },
        "calcium": {
            "separation_hours": 4,
            "reason": "El calcio interfiere significativamente con la absorción",
            "severity": "high",
            "recommendation": "Separar al menos 4 horas"
        },
        "iron": {
            "separation_hours": 4,
            "reason": "El hierro reduce la absorción de levotiroxina",
            "severity": "high",
            "recommendation": "Separar al menos 4 horas"
        }
    },
    "glp1_agonists": {  # Ozempic, Wegovy, Mounjaro, etc.
        "fiber_supplement": {
            "max_single_dose": "10g",
            "reason": "Dosis altas pueden causar náuseas o distensión con GLP-1",
            "severity": "moderate",
            "recommendation": "No exceder 10g de fibra en una sola ingesta"
        }
    },
    "metformina": {
        "vitamin_b12": {
            "monitoring": True,
            "reason": "La metformina puede reducir la absorción de B12 a largo plazo",
            "severity": "moderate",
            "recommendation": "Considerar suplementación de B12 y monitorear niveles"
        }
    },
    "estatinas": {  # Atorvastatina, Simvastatina, etc.
        "coq10": {
            "supplementation_recommended": True,
            "reason": "Las estatinas pueden reducir los niveles de CoQ10",
            "severity": "low",
            "recommendation": "Considerar suplementar con 100-200mg de CoQ10"
        }
    },
    "anticoagulantes": {  # Warfarina
        "vitamin_k": {
            "monitoring": True,
            "reason": "La vitamina K puede interferir con la anticoagulación",
            "severity": "high",
            "recommendation": "Mantener ingesta constante de vitamina K y monitorear INR"
        },
        "omega3_epa_dha": {
            "caution": True,
            "reason": "Dosis altas pueden aumentar el riesgo de sangrado",
            "severity": "moderate",
            "recommendation": "No exceder 2g/día sin supervisión médica"
        }
    }
}

# Suplementos con dosis máximas tolerables
SUPPLEMENT_MAX_DOSES = {
    "vitamin_c_supplement": {
        "max_dose": 2000,
        "unit": "mg",
        "side_effect": "Puede causar diarrea en dosis superiores"
    },
    "fiber_supplement": {
        "max_single_dose": 10,
        "max_daily": 40,
        "unit": "g",
        "side_effect": "Distensión abdominal, gases"
    },
    "magnesium_supplement": {
        "max_dose": 400,
        "unit": "mg",
        "side_effect": "Efecto laxante en dosis altas"
    },
    "omega3_epa_dha": {
        "max_dose": 4000,
        "unit": "mg",
        "side_effect": "Riesgo de sangrado en dosis muy altas",
        "requires_supervision": True
    },
    "vitamin_d3_k2": {
        "max_d3": 4000,
        "unit_d3": "UI",
        "max_k2": 200,
        "unit_k2": "mcg",
        "side_effect": "Hipercalcemia en dosis muy altas de D3"
    }
}

# Sinergias entre suplementos
SUPPLEMENT_SYNERGIES = {
    "collagen_hydrolyzed": {
        "vitamin_c_supplement": {
            "benefit": "La vitamina C mejora la síntesis de colágeno",
            "recommended_dose": "50-100mg de vitamina C con cada dosis de colágeno"
        }
    },
    "iron": {
        "vitamin_c_supplement": {
            "benefit": "La vitamina C mejora la absorción del hierro no hemo",
            "recommended_dose": "50-100mg de vitamina C con las comidas ricas en hierro"
        }
    },
    "vitamin_d3_k2": {
        "combined": True,
        "benefit": "K2 ayuda a dirigir el calcio a los huesos, evitando depósitos arteriales",
        "ratio": "Por cada 1000 UI de D3, 45 mcg de K2"
    }
}

def check_interactions(medications: List[str], supplements: List[Dict]) -> List[Dict]:
    """
    Verifica interacciones entre medicamentos y suplementos
    
    Args:
        medications: Lista de medicamentos del paciente
        supplements: Lista de suplementos con sus dosis
    
    Returns:
        Lista de advertencias de interacción
    """
    warnings = []
    
    for med in medications:
        med_lower = med.lower()
        
        # Buscar medicamento en el diccionario de interacciones
        for drug_key, interactions in DRUG_SUPPLEMENT_INTERACTIONS.items():
            if drug_key in med_lower or med_lower in drug_key:
                # Verificar cada suplemento
                for supp in supplements:
                    supp_id = supp.get('id', '').replace('_', ' ')
                    
                    for supp_key, interaction in interactions.items():
                        if supp_key in supp_id or supp_key in supp.get('name', '').lower():
                            warnings.append({
                                'medication': med,
                                'supplement': supp['name'],
                                'interaction': interaction,
                                'type': 'drug_supplement'
                            })
    
    return warnings

def check_max_doses(supplements: List[Dict]) -> List[Dict]:
    """
    Verifica si las dosis de suplementos exceden los máximos recomendados
    
    Args:
        supplements: Lista de suplementos con sus dosis
    
    Returns:
        Lista de advertencias de dosis
    """
    warnings = []
    
    for supp in supplements:
        supp_id = supp.get('id', '')
        custom_dose = supp.get('custom_dose')
        
        if supp_id in SUPPLEMENT_MAX_DOSES and custom_dose:
            max_info = SUPPLEMENT_MAX_DOSES[supp_id]
            
            # Convertir dosis a número
            try:
                dose_value = float(custom_dose.replace('mg', '').replace('g', '').replace('UI', '').strip())
                
                # Verificar si excede el máximo
                if 'max_dose' in max_info and dose_value > max_info['max_dose']:
                    warnings.append({
                        'supplement': supp['name'],
                        'current_dose': f"{dose_value}{max_info['unit']}",
                        'max_dose': f"{max_info['max_dose']}{max_info['unit']}",
                        'side_effect': max_info.get('side_effect', ''),
                        'type': 'max_dose_exceeded'
                    })
                    
            except ValueError:
                pass  # Ignorar si no se puede parsear la dosis
    
    return warnings

def get_synergies(supplements: List[Dict]) -> List[Dict]:
    """
    Identifica sinergias beneficiosas entre suplementos
    
    Args:
        supplements: Lista de suplementos
    
    Returns:
        Lista de recomendaciones de sinergia
    """
    synergies = []
    supp_ids = [s.get('id', '') for s in supplements]
    
    for supp_id in supp_ids:
        if supp_id in SUPPLEMENT_SYNERGIES:
            synergy_info = SUPPLEMENT_SYNERGIES[supp_id]
            
            for synergy_supp, info in synergy_info.items():
                if isinstance(info, dict) and any(synergy_supp in sid for sid in supp_ids):
                    synergies.append({
                        'supplement1': supp_id,
                        'supplement2': synergy_supp,
                        'benefit': info.get('benefit', ''),
                        'recommendation': info.get('recommended_dose', '')
                    })
    
    return synergies