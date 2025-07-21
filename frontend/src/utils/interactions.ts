// Sistema de verificación de interacciones medicamento-suplemento

interface Supplement {
  id: string
  name: string
  custom_dose?: string
  [key: string]: any
}

interface Medication {
  id: string
  name: string
  [key: string]: any
}

// Mapa simplificado de interacciones (para verificación rápida en frontend)
const INTERACTIONS_MAP: Record<string, Record<string, any>> = {
  levotiroxina: {
    fiber_supplement: {
      separation_hours: 4,
      reason: "La fibra puede interferir con la absorción de levotiroxina",
      severity: "high",
      recommendation: "Tomar la fibra al menos 4 horas después de la levotiroxina"
    },
    omega3_epa_dha: {
      separation_hours: 1,
      reason: "Puede afectar ligeramente la absorción",
      severity: "moderate",
      recommendation: "Separar al menos 1 hora de la toma de levotiroxina"
    },
    magnesium_supplement: {
      separation_hours: 4,
      reason: "El magnesio puede reducir la absorción de hormona tiroidea",
      severity: "high",
      recommendation: "Separar al menos 4 horas de la levotiroxina"
    }
  },
  metformina: {
    vitamin_b12: {
      monitoring: true,
      reason: "La metformina puede reducir la absorción de B12 a largo plazo",
      severity: "moderate",
      recommendation: "Considerar suplementación de B12 y monitorear niveles"
    }
  }
}

const MAX_DOSES: Record<string, any> = {
  vitamin_c_supplement: {
    max_dose: 2000,
    unit: "mg",
    side_effect: "Puede causar diarrea en dosis superiores"
  },
  fiber_supplement: {
    max_single_dose: 10,
    max_daily: 40,
    unit: "g",
    side_effect: "Distensión abdominal, gases"
  },
  magnesium_supplement: {
    max_dose: 400,
    unit: "mg",
    side_effect: "Efecto laxante en dosis altas"
  }
}

const SYNERGIES: Record<string, any> = {
  collagen_hydrolyzed: {
    vitamin_c_supplement: {
      benefit: "La vitamina C mejora la síntesis de colágeno",
      recommendation: "50-100mg de vitamina C con cada dosis de colágeno"
    }
  }
}

export function checkInteractions(medications: Medication[], supplements: Supplement[]) {
  const interactions = []
  
  for (const med of medications) {
    const medName = med.name.toLowerCase()
    
    // Buscar en las claves del mapa de interacciones
    for (const [drugKey, drugInteractions] of Object.entries(INTERACTIONS_MAP)) {
      if (medName.includes(drugKey)) {
        // Verificar cada suplemento
        for (const supp of supplements) {
          const suppId = supp.id.toLowerCase()
          
          for (const [suppKey, interaction] of Object.entries(drugInteractions)) {
            if (suppId.includes(suppKey)) {
              interactions.push({
                medication: med.name,
                supplement: supp.name,
                interaction
              })
            }
          }
        }
      }
    }
  }
  
  return interactions
}

export function checkDoseWarnings(supplements: Supplement[]) {
  const warnings = []
  
  for (const supp of supplements) {
    const suppId = supp.id.toLowerCase()
    const customDose = supp.custom_dose
    
    if (suppId in MAX_DOSES && customDose) {
      const maxInfo = MAX_DOSES[suppId]
      
      // Extraer valor numérico de la dosis
      const doseMatch = customDose.match(/(\d+(?:\.\d+)?)/);
      if (doseMatch) {
        const doseValue = parseFloat(doseMatch[1])
        
        if (doseValue > maxInfo.max_dose) {
          warnings.push({
            supplement: supp.name,
            current_dose: customDose,
            max_dose: `${maxInfo.max_dose}${maxInfo.unit}`,
            side_effect: maxInfo.side_effect
          })
        }
      }
    }
  }
  
  return warnings
}

export function checkSynergies(supplements: Supplement[]) {
  const synergies = []
  const suppIds = supplements.map(s => s.id.toLowerCase())
  
  for (const [suppKey, synergyData] of Object.entries(SYNERGIES)) {
    if (suppIds.some(id => id.includes(suppKey))) {
      for (const [synergySupp, info] of Object.entries(synergyData)) {
        if (suppIds.some(id => id.includes(synergySupp))) {
          synergies.push({
            supplement1: suppKey,
            supplement2: synergySupp,
            benefit: (info as any).benefit,
            recommendation: (info as any).recommendation
          })
        }
      }
    }
  }
  
  return synergies
}