import { useState, useEffect } from 'react'
import { X, Plus } from 'lucide-react'
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
  }
}

interface Supplement {
  id: string
  name: string
  servings: number
  calories: number
  protein: number
  carbs: number
  fats: number
  serving_size: string
}

interface SupplementSelectorProps {
  supplements: Supplement[]
  onChange: (supplements: Supplement[]) => void
}

export function SupplementSelector({ supplements, onChange }: SupplementSelectorProps) {
  const [selectedSupplements, setSelectedSupplements] = useState<Supplement[]>(supplements || [])
  const [selectedCategory, setSelectedCategory] = useState<string>('proteinas')
  const [selectedSupplement, setSelectedSupplement] = useState<string>('')
  const [servings, setServings] = useState<number>(1)

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
          <Select value={selectedSupplement} onValueChange={setSelectedSupplement}>
            <SelectTrigger>
              <SelectValue placeholder="Selecciona un suplemento" />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(SUPPLEMENTS_DATABASE[selectedCategory as keyof typeof SUPPLEMENTS_DATABASE].supplements).map(([key, supplement]) => (
                <SelectItem key={key} value={key}>
                  {supplement.name}
                </SelectItem>
              ))}
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
        return supplement ? (
          <div className="text-sm text-muted-foreground">
            Porción: {supplement.serving}
          </div>
        ) : null
      })()}

      {selectedSupplements.length > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-3">
              <h4 className="font-medium mb-3">Suplementos seleccionados</h4>
              
              {selectedSupplements.map((supplement) => (
                <div key={supplement.id} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-sm">{supplement.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {supplement.servings} {supplement.servings === 1 ? 'porción' : 'porciones'} • {supplement.serving_size}
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