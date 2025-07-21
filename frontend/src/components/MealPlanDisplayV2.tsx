import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { mealPlanService } from "@/services/api"
import { Download, Loader2, ChefHat, Clock, Apple } from "lucide-react"

interface MealOption {
  recipeId: string
  recipeName: string
  ingredients: string[]
  macros: {
    protein: number
    carbs: number
    fats: number
    calories: number
  }
}

interface Meal {
  name: string
  options: MealOption[]
}

interface MealPlanDisplayProps {
  mealPlan: string
  pdfPath: string
}

export function MealPlanDisplayV2({ mealPlan, pdfPath }: MealPlanDisplayProps) {
  const [isDownloading, setIsDownloading] = useState(false)
  const [selectedOptions, setSelectedOptions] = useState<Record<string, number>>({})

  const handleDownload = () => {
    setIsDownloading(true)
    mealPlanService.downloadPdf(pdfPath)
    setTimeout(() => setIsDownloading(false), 2000)
  }

  // Parse the meal plan text to extract meals and options
  const parseMealPlan = (planText: string): Meal[] => {
    const meals: Meal[] = []
    const mealSections = planText.split(/(?=DESAYUNO|ALMUERZO|MERIENDA|CENA|COLACIÓN)/g)
    
    mealSections.forEach(section => {
      if (!section.trim()) return
      
      const lines = section.split('\n')
      const mealName = lines[0].trim()
      
      if (!mealName || mealName === 'PLAN ALIMENTARIO - 3 DÍAS IGUALES') return
      
      const meal: Meal = {
        name: mealName,
        options: []
      }
      
      let currentOption: MealOption | null = null
      let collectingIngredients = false
      
      lines.forEach((line) => {
        // Check for option header
        if (line.includes('OPCIÓN')) {
          if (currentOption) {
            meal.options.push(currentOption)
          }
          currentOption = {
            recipeId: '',
            recipeName: '',
            ingredients: [],
            macros: { protein: 0, carbs: 0, fats: 0, calories: 0 }
          }
          collectingIngredients = false
        }
        
        // Extract recipe ID and name
        if (currentOption && line.includes('Receta:') && line.includes('[REC_')) {
          const recipeMatch = line.match(/\[REC_(\d+)\]\s*-\s*(.+)/)
          if (recipeMatch) {
            currentOption.recipeId = `REC_${recipeMatch[1]}`
            currentOption.recipeName = recipeMatch[2].trim()
          }
        }
        
        // Start collecting ingredients
        if (currentOption && line.includes('Ingredientes con cantidades ajustadas:')) {
          collectingIngredients = true
        } else if (collectingIngredients && line.trim().startsWith('*')) {
          currentOption?.ingredients.push(line.trim().substring(1).trim())
        } else if (collectingIngredients && !line.trim().startsWith('*') && line.includes('Macros:')) {
          collectingIngredients = false
        }
        
        // Extract macros
        if (currentOption && line.includes('Macros:')) {
          const macroMatch = line.match(/P:\s*(\d+)g\s*\|\s*C:\s*(\d+)g\s*\|\s*G:\s*(\d+)g\s*\|\s*Cal:\s*(\d+)/)
          if (macroMatch) {
            currentOption.macros = {
              protein: parseInt(macroMatch[1]),
              carbs: parseInt(macroMatch[2]),
              fats: parseInt(macroMatch[3]),
              calories: parseInt(macroMatch[4])
            }
          }
        }
      })
      
      // Add the last option
      if (currentOption) {
        meal.options.push(currentOption)
      }
      
      if (meal.options.length > 0) {
        meals.push(meal)
      }
    })
    
    return meals
  }

  const meals = parseMealPlan(mealPlan)

  // Get selected option for a meal (default to 0)
  const getSelectedOption = (mealName: string) => {
    return selectedOptions[mealName] || 0
  }

  // Calculate total macros based on selected options
  const calculateTotalMacros = () => {
    return meals.reduce((totals, meal) => {
      const selectedIdx = getSelectedOption(meal.name)
      const option = meal.options[selectedIdx]
      if (option) {
        return {
          protein: totals.protein + option.macros.protein,
          carbs: totals.carbs + option.macros.carbs,
          fats: totals.fats + option.macros.fats,
          calories: totals.calories + option.macros.calories
        }
      }
      return totals
    }, { protein: 0, carbs: 0, fats: 0, calories: 0 })
  }

  const totalMacros = calculateTotalMacros()

  if (meals.length === 0) {
    // Fallback to simple display if parsing fails
    return (
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Plan Nutricional Generado</CardTitle>
          <CardDescription>
            Plan de 3 días iguales según el método "Tres Días y Carga"
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <Button 
              onClick={handleDownload} 
              disabled={isDownloading}
              className="w-full sm:w-auto"
            >
              {isDownloading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Descargando...
                </>
              ) : (
                <>
                  <Download className="mr-2 h-4 w-4" />
                  Descargar PDF
                </>
              )}
            </Button>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-6 overflow-auto max-h-[600px]">
            <pre className="whitespace-pre-wrap font-mono text-sm">
              {mealPlan}
            </pre>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle>Plan Nutricional Generado</CardTitle>
        <CardDescription>
          Plan de 3 días iguales con opciones para cada comida
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex flex-col sm:flex-row gap-4">
          <Button 
            onClick={handleDownload} 
            disabled={isDownloading}
            className="w-full sm:w-auto"
          >
            {isDownloading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Descargando...
              </>
            ) : (
              <>
                <Download className="mr-2 h-4 w-4" />
                Descargar PDF
              </>
            )}
          </Button>
          
          <div className="flex-1 flex items-center justify-end gap-2">
            <Badge variant="secondary" className="text-base">
              Total: {totalMacros.calories} kcal
            </Badge>
            <Badge variant="outline">P: {totalMacros.protein}g</Badge>
            <Badge variant="outline">C: {totalMacros.carbs}g</Badge>
            <Badge variant="outline">G: {totalMacros.fats}g</Badge>
          </div>
        </div>

        <div className="space-y-4">
          {meals.map((meal) => (
            <Card key={meal.name}>
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  {meal.name.includes('DESAYUNO') && <Clock className="w-5 h-5 text-orange-500" />}
                  {meal.name.includes('ALMUERZO') && <ChefHat className="w-5 h-5 text-blue-500" />}
                  {meal.name.includes('MERIENDA') && <Apple className="w-5 h-5 text-green-500" />}
                  {meal.name.includes('CENA') && <ChefHat className="w-5 h-5 text-purple-500" />}
                  <CardTitle className="text-lg">{meal.name}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <Tabs 
                  defaultValue="0" 
                  value={getSelectedOption(meal.name).toString()}
                  onValueChange={(value) => setSelectedOptions(prev => ({ ...prev, [meal.name]: parseInt(value) }))}
                >
                  <TabsList className="grid grid-cols-3 w-full">
                    <TabsTrigger value="0">Opción 1</TabsTrigger>
                    <TabsTrigger value="1">Opción 2</TabsTrigger>
                    <TabsTrigger value="2">Opción 3</TabsTrigger>
                  </TabsList>
                  
                  {meal.options.map((option, idx) => (
                    <TabsContent key={idx} value={idx.toString()} className="space-y-3">
                      <div>
                        <h4 className="font-semibold text-sm mb-1">{option.recipeName}</h4>
                        <p className="text-xs text-muted-foreground">{option.recipeId}</p>
                      </div>
                      
                      {option.ingredients.length > 0 && (
                        <div>
                          <p className="text-sm font-medium mb-1">Ingredientes:</p>
                          <ul className="text-sm text-gray-600 space-y-1">
                            {option.ingredients.map((ing, i) => (
                              <li key={i} className="flex items-start">
                                <span className="mr-2">•</span>
                                <span>{ing}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      <div className="flex gap-2 pt-2">
                        <Badge variant="secondary">{option.macros.calories} kcal</Badge>
                        <Badge variant="outline">P: {option.macros.protein}g</Badge>
                        <Badge variant="outline">C: {option.macros.carbs}g</Badge>
                        <Badge variant="outline">G: {option.macros.fats}g</Badge>
                      </div>
                    </TabsContent>
                  ))}
                </Tabs>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold mb-2">Vista completa del plan</h3>
          <div className="overflow-auto max-h-[400px]">
            <pre className="whitespace-pre-wrap font-mono text-xs">
              {mealPlan}
            </pre>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}