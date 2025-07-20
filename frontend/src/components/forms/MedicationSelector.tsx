import { useState, useEffect } from 'react'
import { X, Plus, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'

// Medication database imported from backend structure
const MEDICATIONS_DATABASE = {
  antidiabeticos: {
    name: "Antidiabéticos",
    medications: {
      metformina: { name: "Metformina", impact: "Puede reducir absorción de B12, puede causar pérdida de peso", considerations: "Tomar con comidas para reducir molestias GI" },
      insulina: { name: "Insulina", impact: "Puede aumentar el apetito y peso", considerations: "Ajustar carbohidratos según dosis" }
    }
  },
  antihipertensivos: {
    name: "Antihipertensivos",
    medications: {
      enalapril: { name: "Enalapril", impact: "Puede aumentar potasio", considerations: "Limitar alimentos ricos en potasio" },
      amlodipina: { name: "Amlodipina", impact: "Puede causar edema", considerations: "Reducir sodio" }
    }
  },
  diureticos: {
    name: "Diuréticos",
    medications: {
      hidroclorotiazida: { name: "Hidroclorotiazida", impact: "Pérdida de potasio y magnesio", considerations: "Aumentar ingesta de K y Mg" },
      furosemida: { name: "Furosemida", impact: "Pérdida de electrolitos", considerations: "Monitorear electrolitos" }
    }
  },
  estatinas: {
    name: "Estatinas",
    medications: {
      atorvastatina: { name: "Atorvastatina", impact: "Puede reducir CoQ10", considerations: "Evitar pomelo" },
      simvastatina: { name: "Simvastatina", impact: "Puede reducir CoQ10", considerations: "Evitar pomelo, tomar por la noche" },
      rosuvastatina: { name: "Rosuvastatina", impact: "Puede reducir CoQ10", considerations: "Se puede tomar a cualquier hora" }
    }
  },
  tiroides: {
    name: "Tiroides",
    medications: {
      levotiroxina: { name: "Levotiroxina", impact: "Mejora metabolismo", considerations: "Tomar en ayunas, evitar soja y calcio 4h" },
      metimazol: { name: "Metimazol", impact: "Puede aumentar peso", considerations: "Monitorear peso" }
    }
  },
  antidepresivos: {
    name: "Psiquiátricos - Antidepresivos",
    medications: {
      sertralina: { name: "Sertralina", impact: "Puede alterar apetito y peso", considerations: "Monitorear cambios de peso" },
      fluoxetina: { name: "Fluoxetina", impact: "Puede reducir apetito inicialmente", considerations: "Asegurar ingesta adecuada" },
      escitalopram: { name: "Escitalopram", impact: "Puede aumentar peso", considerations: "Control de porciones" }
    }
  },
  antipsicoticos: {
    name: "Psiquiátricos - Antipsicóticos",
    medications: {
      quetiapina: { name: "Quetiapina", impact: "Aumento de peso y apetito común", considerations: "Plan hipocalórico preventivo" }
    }
  },
  ansioliticos: {
    name: "Psiquiátricos - Ansiolíticos",
    medications: {
      alprazolam: { name: "Alprazolam", impact: "Puede aumentar apetito", considerations: "Evitar alcohol" },
      clonazepam: { name: "Clonazepam", impact: "Puede causar somnolencia", considerations: "Evitar alcohol" }
    }
  },
  corticoides: {
    name: "Corticoides",
    medications: {
      prednisona: { name: "Prednisona", impact: "Aumenta apetito, retención de líquidos, pérdida de K", considerations: "Dieta baja en sodio, alta en K y Ca" },
      betametasona: { name: "Betametasona", impact: "Similar a prednisona", considerations: "Control de sodio y calorías" }
    }
  },
  aines: {
    name: "Antiinflamatorios",
    medications: {
      ibuprofeno: { name: "Ibuprofeno", impact: "Puede causar molestias GI", considerations: "Tomar con comidas" },
      diclofenac: { name: "Diclofenac", impact: "Puede causar molestias GI", considerations: "Tomar con comidas" },
      celecoxib: { name: "Celecoxib", impact: "Menor impacto GI", considerations: "Hidratación adecuada" }
    }
  },
  hormonales: {
    name: "Anticonceptivos",
    medications: {
      anticonceptivos_orales: { name: "Anticonceptivos orales", impact: "Puede aumentar peso y retención de líquidos", considerations: "Aumentar B6, B12, ácido fólico" }
    }
  },
  ibb: {
    name: "Gastrointestinales - IBP",
    medications: {
      omeprazol: { name: "Omeprazol", impact: "Reduce absorción de B12, Fe, Ca, Mg", considerations: "Suplementar si uso prolongado" },
      pantoprazol: { name: "Pantoprazol", impact: "Similar a omeprazol", considerations: "Monitorear B12" }
    }
  },
  anticoagulantes: {
    name: "Anticoagulantes",
    medications: {
      warfarina: { name: "Warfarina", impact: "Interactúa con vitamina K", considerations: "Ingesta constante de vitamina K" }
    }
  },
  otros: {
    name: "Otros",
    medications: {
      allopurinol: { name: "Allopurinol", impact: "Ninguno significativo", considerations: "Mantener hidratación" },
      colchicina: { name: "Colchicina", impact: "Puede causar diarrea", considerations: "Hidratación adecuada" }
    }
  }
}

interface Medication {
  id: string
  name: string
  impact: string
  considerations: string
}

interface MedicationSelectorProps {
  medications: Medication[]
  onChange: (medications: Medication[]) => void
}

export function MedicationSelector({ medications, onChange }: MedicationSelectorProps) {
  const [selectedMedications, setSelectedMedications] = useState<Medication[]>(medications || [])
  const [selectedCategory, setSelectedCategory] = useState<string>('antidiabeticos')
  const [selectedMedication, setSelectedMedication] = useState<string>('')

  useEffect(() => {
    onChange(selectedMedications)
  }, [selectedMedications])

  const addMedication = () => {
    if (!selectedMedication) return

    // Find the medication in the database
    let medicationData: any = null
    for (const categoryData of Object.values(MEDICATIONS_DATABASE)) {
      if (selectedMedication in categoryData.medications) {
        medicationData = categoryData.medications[selectedMedication as keyof typeof categoryData.medications]
        break
      }
    }
    
    if (!medicationData) return

    const newMedication: Medication = {
      id: `${selectedMedication}_${Date.now()}`,
      name: medicationData.name,
      impact: medicationData.impact,
      considerations: medicationData.considerations
    }

    setSelectedMedications([...selectedMedications, newMedication])
    
    // Reset form
    setSelectedMedication('')
  }

  const removeMedication = (id: string) => {
    setSelectedMedications(selectedMedications.filter(m => m.id !== id))
  }

  // Group considerations by type
  const groupedConsiderations = () => {
    const nutritionalImpacts: string[] = []
    const dietaryConsiderations: string[] = []
    
    selectedMedications.forEach(med => {
      if (med.impact) {
        nutritionalImpacts.push(`• ${med.name}: ${med.impact}`)
      }
      if (med.considerations) {
        dietaryConsiderations.push(`• ${med.name}: ${med.considerations}`)
      }
    })
    
    return { nutritionalImpacts, dietaryConsiderations }
  }

  const { nutritionalImpacts, dietaryConsiderations } = groupedConsiderations()

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <Label>Categoría</Label>
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(MEDICATIONS_DATABASE).map(([key, category]) => (
                <SelectItem key={key} value={key}>
                  {category.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label>Medicamento</Label>
          <div className="flex gap-2">
            <Select value={selectedMedication} onValueChange={setSelectedMedication}>
              <SelectTrigger>
                <SelectValue placeholder="Selecciona un medicamento" />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(MEDICATIONS_DATABASE[selectedCategory as keyof typeof MEDICATIONS_DATABASE].medications).map(([key, medication]) => (
                  <SelectItem key={key} value={key}>
                    {medication.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button onClick={addMedication} disabled={!selectedMedication}>
              <Plus className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>

      {selectedMedications.length > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div>
                <h4 className="font-medium mb-3">Medicamentos seleccionados</h4>
                <div className="space-y-2">
                  {selectedMedications.map((medication) => (
                    <div key={medication.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium text-sm">{medication.name}</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeMedication(medication.id)}
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>

              {nutritionalImpacts.length > 0 && (
                <Alert>
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    <p className="font-medium mb-2">Impactos nutricionales:</p>
                    <div className="space-y-1 text-sm">
                      {nutritionalImpacts.map((impact, idx) => (
                        <p key={idx}>{impact}</p>
                      ))}
                    </div>
                  </AlertDescription>
                </Alert>
              )}

              {dietaryConsiderations.length > 0 && (
                <Alert>
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    <p className="font-medium mb-2">Consideraciones dietéticas:</p>
                    <div className="space-y-1 text-sm">
                      {dietaryConsiderations.map((consideration, idx) => (
                        <p key={idx}>{consideration}</p>
                      ))}
                    </div>
                  </AlertDescription>
                </Alert>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}