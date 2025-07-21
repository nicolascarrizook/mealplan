import { useState, useEffect } from 'react'
import { X, Plus, Calculator } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'

// Supplement database imported from backend structure
const SUPPLEMENTS_DATABASE = {
  proteinas: {
    name: "Proteínas",
    supplements: {
      whey_protein: { name: "Proteína Whey (Star Nutrition, ENA, UltraTech, Xtrenght)", serving: "30g (1 scoop)", calories: 120, protein: 24, carbs: 2, fats: 2 },
      casein_protein: { name: "Proteína Caseína", serving: "30g (1 scoop)", calories: 110, protein: 24, carbs: 3, fats: 0.5 },
      plant_protein: { name: "Proteína Vegetal", serving: "30g (1 scoop)", calories: 110, protein: 20, carbs: 4, fats: 2 },
      egg_protein: { name: "Proteína de Huevo", serving: "30g (1 scoop)", calories: 115, protein: 23, carbs: 2, fats: 1 }
    }
  },
  aminoacidos: {
    name: "Aminoácidos",
    supplements: {
      bcaa: { name: "BCAA (Aminoácidos de cadena ramificada)", serving: "5-10g", calories: 40, protein: 10, carbs: 0, fats: 0 },
      glutamine: { name: "Glutamina", serving: "5-10g", calories: 30, protein: 7.5, carbs: 0, fats: 0 },
      eaa: { name: "EAA (Aminoácidos esenciales)", serving: "15g", calories: 60, protein: 15, carbs: 0, fats: 0 }
    }
  },
  creatina: {
    name: "Creatina",
    supplements: {
      creatine_mono: { name: "Creatina Monohidratada", serving: "3-5g", calories: 0, protein: 0, carbs: 0, fats: 0 },
      creatine_hcl: { name: "Creatina HCL", serving: "3g", calories: 0, protein: 0, carbs: 0, fats: 0 }
    }
  },
  pre_entreno: {
    name: "Pre-entreno",
    supplements: {
      pre_workout: { name: "Pre-entreno estándar", serving: "10g", calories: 20, protein: 0, carbs: 5, fats: 0 },
      pre_workout_stim_free: { name: "Pre-entreno sin estimulantes", serving: "10g", calories: 15, protein: 0, carbs: 3, fats: 0 }
    }
  },
  carbohidratos: {
    name: "Carbohidratos",
    supplements: {
      maltodextrin: { name: "Maltodextrina", serving: "50g", calories: 200, protein: 0, carbs: 50, fats: 0 },
      dextrose: { name: "Dextrosa", serving: "50g", calories: 200, protein: 0, carbs: 50, fats: 0 },
      waxy_maize: { name: "Almidón de maíz ceroso", serving: "50g", calories: 200, protein: 0, carbs: 50, fats: 0 }
    }
  },
  ganadores: {
    name: "Ganadores de peso",
    supplements: {
      mass_gainer: { name: "Ganador de peso (Mutant Mass, Star Nutrition Gainer)", serving: "100g", calories: 400, protein: 20, carbs: 65, fats: 7 },
      lean_gainer: { name: "Ganador magro", serving: "100g", calories: 350, protein: 35, carbs: 45, fats: 3 }
    }
  },
  quemadores: {
    name: "Quemadores",
    supplements: {
      l_carnitine: { name: "L-Carnitina", serving: "3g", calories: 0, protein: 0, carbs: 0, fats: 0 },
      cla: { name: "CLA", serving: "3g", calories: 27, protein: 0, carbs: 0, fats: 3 },
      thermogenic: { name: "Termogénico", serving: "1 cápsula", calories: 0, protein: 0, carbs: 0, fats: 0 }
    }
  },
  vitaminas: {
    name: "Vitaminas y minerales",
    supplements: {
      multivitamin: { name: "Multivitamínico", serving: "1 tableta", calories: 0, protein: 0, carbs: 0, fats: 0 },
      vitamin_d: { name: "Vitamina D3", serving: "1 cápsula", calories: 0, protein: 0, carbs: 0, fats: 0 },
      omega_3: { name: "Omega 3", serving: "2 cápsulas", calories: 20, protein: 0, carbs: 0, fats: 2 },
      magnesium: { name: "Magnesio", serving: "400mg", calories: 0, protein: 0, carbs: 0, fats: 0 },
      zinc: { name: "Zinc", serving: "15mg", calories: 0, protein: 0, carbs: 0, fats: 0 }
    }
  },
  otros: {
    name: "Otros",
    supplements: {
      collagen: { name: "Colágeno hidrolizado", serving: "10g", calories: 40, protein: 10, carbs: 0, fats: 0 },
      cafeina: { name: "Cafeína (pastillas o polvo)", serving: "200mg", calories: 0, protein: 0, carbs: 0, fats: 0 },
      beta_alanina: { name: "Beta-alanina", serving: "3.2-6g", calories: 0, protein: 0, carbs: 0, fats: 0 },
      citrulina_malato: { name: "Citrulina Malato (2:1)", serving: "6-8g", calories: 0, protein: 0, carbs: 0, fats: 0 },
      sales_hidratacion: { name: "Sales de hidratación (Hydrate UP, Total Magnesiano, Suero Mix)", serving: "1 sobre", calories: 0, protein: 0, carbs: 0, fats: 0 },
      spirulina: { name: "Espirulina", serving: "5g", calories: 20, protein: 3, carbs: 1, fats: 0.5 },
      mct_oil: { name: "Aceite MCT", serving: "15ml", calories: 130, protein: 0, carbs: 0, fats: 14 }
    }
  },
  fibra: {
    name: "Fibra",
    supplements: {
      fiber_supplement: { 
        name: "Fibra Dietaria (Psyllium, Inulina, Salvado de avena)", 
        serving: "5-10g por toma", 
        calories: 20, 
        protein: 0, 
        carbs: 8, 
        fats: 0
      }
    }
  },
  minerales_adicionales: {
    name: "Minerales Adicionales",
    supplements: {
      magnesium_supplement: { 
        name: "Magnesio (Citrato, Bisglicinato, Malato)", 
        serving: "300-400mg", 
        calories: 0, 
        protein: 0, 
        carbs: 0, 
        fats: 0
      }
    }
  },
  vitaminas_adicionales: {
    name: "Vitaminas Adicionales",
    supplements: {
      vitamin_c_supplement: { 
        name: "Vitamina C", 
        serving: "500-1000mg", 
        calories: 0, 
        protein: 0, 
        carbs: 0, 
        fats: 0
      },
      vitamin_d3_k2: { 
        name: "Vitamina D3 + K2", 
        serving: "D3: 2000-4000 UI + K2: 90-180 mcg", 
        calories: 0, 
        protein: 0, 
        carbs: 0, 
        fats: 0
      }
    }
  },
  especializados: {
    name: "Suplementos Especializados",
    supplements: {
      collagen_hydrolyzed: { 
        name: "Colágeno Hidrolizado", 
        serving: "10g", 
        calories: 35, 
        protein: 9, 
        carbs: 0, 
        fats: 0
      },
      omega3_epa_dha: { 
        name: "Omega 3 (EPA/DHA)", 
        serving: "1000-3000mg aceite de pescado", 
        calories: 10, 
        protein: 0, 
        carbs: 0, 
        fats: 1
      }
    }
  }
}

interface Supplement {
  id: string
  name: string
  servings: number
  custom_dose?: string
  frequency?: string
  clinical_relevance?: boolean
  calories: number
  protein: number
  carbs: number
  fats: number
  serving_size: string
}

interface SupplementSelectorProps {
  supplements: Supplement[]
  onChange: (supplements: Supplement[]) => void
  bodyWeight?: number  // Para cálculos automáticos
}

export function SupplementSelector({ supplements, onChange, bodyWeight = 70 }: SupplementSelectorProps) {
  const [selectedSupplements, setSelectedSupplements] = useState<Supplement[]>(supplements || [])
  const [selectedCategory, setSelectedCategory] = useState<string>('proteinas')
  const [selectedSupplement, setSelectedSupplement] = useState<string>('')
  const [servings, setServings] = useState<number>(1)
  const [customDose, setCustomDose] = useState<string>('')
  const [frequency, setFrequency] = useState<string>('')
  const [clinicalRelevance, setClinicalRelevance] = useState<boolean>(false)

  // Función para calcular dosis automáticas
  const calculateAutomaticDose = (supplementKey: string): { dose: string, servings: number } | null => {
    switch (supplementKey) {
      case 'creatine_mono':
      case 'creatine_hcl':
        // Creatina: 0.1g por kg de peso corporal
        const creatineDose = Math.round(bodyWeight * 0.1 * 10) / 10 // Redondear a 1 decimal
        return { dose: `${creatineDose}g (0.1g × ${bodyWeight}kg)`, servings: Math.round((creatineDose / 5) * 100) / 100 } // Asumiendo 5g por porción estándar
      
      case 'whey_protein':
      case 'casein_protein':
      case 'plant_protein':
      case 'egg_protein':
        // Proteína: 1 scoop = 20-25g de proteína
        // Calculamos basándonos en las necesidades típicas post-entreno
        return { dose: '1 scoop (20-25g proteína)', servings: 1 }
      
      case 'magnesium':
      case 'magnesium_supplement':
        // Magnesio: 350-400mg
        return { dose: '350-400mg', servings: 1 }
      
      case 'omega_3':
      case 'omega3_epa_dha':
        // Omega 3: dosis estándar recomendada
        return { dose: '1000-2000mg EPA/DHA', servings: 2 }
      
      default:
        return null
    }
  }

  useEffect(() => {
    onChange(selectedSupplements)
  }, [selectedSupplements])

  const addSupplement = () => {
    if (!selectedSupplement) return

    // Find the supplement in the database
    let supplementData: any = null
    for (const categoryData of Object.values(SUPPLEMENTS_DATABASE)) {
      if (selectedSupplement in categoryData.supplements) {
        supplementData = categoryData.supplements[selectedSupplement as keyof typeof categoryData.supplements]
        break
      }
    }
    
    if (!supplementData) return

    const newSupplement: Supplement = {
      id: `${selectedSupplement}_${Date.now()}`,
      name: supplementData.name,
      servings,
      custom_dose: customDose || undefined,
      frequency: frequency || undefined,
      clinical_relevance: clinicalRelevance,
      calories: supplementData.calories * servings,
      protein: supplementData.protein * servings,
      carbs: supplementData.carbs * servings,
      fats: supplementData.fats * servings,
      serving_size: supplementData.serving
    }

    setSelectedSupplements([...selectedSupplements, newSupplement])
    
    // Reset form
    setSelectedSupplement('')
    setServings(1)
    setCustomDose('')
    setFrequency('')
    setClinicalRelevance(false)
  }

  const removeSupplement = (id: string) => {
    setSelectedSupplements(selectedSupplements.filter(s => s.id !== id))
  }

  const totals = selectedSupplements.reduce((acc, supp) => ({
    calories: acc.calories + supp.calories,
    protein: acc.protein + supp.protein,
    carbs: acc.carbs + supp.carbs,
    fats: acc.fats + supp.fats
  }), { calories: 0, protein: 0, carbs: 0, fats: 0 })

  return (
    <div className="space-y-4">
      {bodyWeight && (
        <div className="text-sm text-muted-foreground bg-blue-50 p-3 rounded-lg">
          <Calculator className="w-4 h-4 inline mr-2 text-blue-600" />
          Los suplementos marcados con el ícono de calculadora tienen dosis automáticas basadas en tu peso ({bodyWeight}kg)
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <Label>Categoría</Label>
          <Select value={selectedCategory} onValueChange={setSelectedCategory}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(SUPPLEMENTS_DATABASE).map(([key, category]) => (
                <SelectItem key={key} value={key}>
                  {category.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label>Suplemento</Label>
          <Select 
            value={selectedSupplement} 
            onValueChange={(value) => {
              setSelectedSupplement(value)
              // Aplicar dosis automática si está disponible
              const autoDose = calculateAutomaticDose(value)
              if (autoDose) {
                setCustomDose(autoDose.dose)
                setServings(autoDose.servings)
              }
            }}
          >
            <SelectTrigger>
              <SelectValue placeholder="Selecciona un suplemento" />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(SUPPLEMENTS_DATABASE[selectedCategory as keyof typeof SUPPLEMENTS_DATABASE].supplements).map(([key, supplement]) => {
                const hasAutoDose = calculateAutomaticDose(key) !== null
                return (
                  <SelectItem key={key} value={key}>
                    <div className="flex items-center gap-2">
                      {supplement.name}
                      {hasAutoDose && (
                        <Calculator className="w-3 h-3 text-blue-500" />
                      )}
                    </div>
                  </SelectItem>
                )
              })}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Label>Porciones diarias</Label>
          <div className="flex gap-2">
            <Input
              type="number"
              value={servings}
              onChange={(e) => setServings(Number(e.target.value))}
              min={0.5}
              max={10}
              step={0.5}
            />
            <Button onClick={addSupplement} disabled={!selectedSupplement}>
              <Plus className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>

      {selectedSupplement && (() => {
        // Find and display serving size
        const category = SUPPLEMENTS_DATABASE[selectedCategory as keyof typeof SUPPLEMENTS_DATABASE]
        const supplement = (category.supplements as any)[selectedSupplement]
        const autoDose = calculateAutomaticDose(selectedSupplement)
        
        return supplement ? (
          <div className="space-y-2">
            <div className="text-sm text-muted-foreground">
              Porción: {supplement.serving}
            </div>
            {autoDose && (
              <div className="text-sm text-blue-600 font-medium">
                ✨ Dosis calculada automáticamente basada en {bodyWeight}kg de peso corporal
              </div>
            )}
          </div>
        ) : null
      })()}

      {/* Nuevos campos para dosis personalizada */}
      {selectedSupplement && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <div>
            <Label className="text-sm">Dosis personalizada (opcional)</Label>
            <Input
              placeholder="Ej: 400mg, 10g, 2000UI"
              value={customDose}
              onChange={(e) => setCustomDose(e.target.value)}
              className="mt-1"
            />
          </div>
          <div>
            <Label className="text-sm">Frecuencia (opcional)</Label>
            <Input
              placeholder="Ej: Con desayuno y cena"
              value={frequency}
              onChange={(e) => setFrequency(e.target.value)}
              className="mt-1"
            />
          </div>
          <div className="flex items-end">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="clinical-relevance"
                checked={clinicalRelevance}
                onChange={(e) => setClinicalRelevance(e.target.checked)}
                className="h-4 w-4 rounded border-gray-300"
              />
              <Label htmlFor="clinical-relevance" className="cursor-pointer text-sm">
                Relevancia clínica
              </Label>
            </div>
          </div>
        </div>
      )}

      {selectedSupplements.length > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-3">
              <h4 className="font-medium mb-3">Suplementos seleccionados</h4>
              
              {selectedSupplements.map((supplement) => (
                <div key={supplement.id} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-sm">
                        {supplement.name}
                        {supplement.clinical_relevance && (
                          <span className="ml-2 text-xs text-orange-600 font-medium">⚠️ Relevancia clínica</span>
                        )}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {supplement.custom_dose || `${supplement.servings} ${supplement.servings === 1 ? 'porción' : 'porciones'}`} • {supplement.serving_size}
                        {supplement.frequency && ` • ${supplement.frequency}`}
                        {supplement.custom_dose && (supplement.custom_dose.includes('kg)') || supplement.custom_dose.includes('scoop')) && (
                          <span className="text-blue-600"> • Calculado automáticamente</span>
                        )}
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeSupplement(supplement.id)}
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                  <div className="flex gap-2 text-xs">
                    <Badge variant="secondary">{supplement.calories} kcal</Badge>
                    <Badge variant="outline">P: {supplement.protein}g</Badge>
                    <Badge variant="outline">C: {supplement.carbs}g</Badge>
                    <Badge variant="outline">G: {supplement.fats}g</Badge>
                  </div>
                </div>
              ))}
              
              <Separator />
              
              <div className="space-y-2">
                <p className="font-medium text-sm">Totales de suplementación</p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                  <div className="text-center p-2 bg-gray-50 rounded">
                    <p className="text-xs text-muted-foreground">Calorías</p>
                    <p className="font-semibold">{totals.calories}</p>
                  </div>
                  <div className="text-center p-2 bg-gray-50 rounded">
                    <p className="text-xs text-muted-foreground">Proteínas</p>
                    <p className="font-semibold">{totals.protein}g</p>
                  </div>
                  <div className="text-center p-2 bg-gray-50 rounded">
                    <p className="text-xs text-muted-foreground">Carbohidratos</p>
                    <p className="font-semibold">{totals.carbs}g</p>
                  </div>
                  <div className="text-center p-2 bg-gray-50 rounded">
                    <p className="text-xs text-muted-foreground">Grasas</p>
                    <p className="font-semibold">{totals.fats}g</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}