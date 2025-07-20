import { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CustomMealDistribution, MealMacroDistribution } from '@/types'

interface CustomDistributionProps {
  dailyCalories: number
  dailyProtein: number
  dailyCarbs: number
  dailyFats: number
  mealsCount: number
  value?: CustomMealDistribution
  onChange: (value: CustomMealDistribution) => void
}

export function CustomDistribution({
  dailyCalories,
  dailyProtein,
  dailyCarbs,
  dailyFats,
  mealsCount,
  value,
  onChange
}: CustomDistributionProps) {
  const meals = mealsCount === 3 
    ? ['desayuno', 'almuerzo', 'cena'] 
    : ['desayuno', 'almuerzo', 'merienda', 'cena']

  const initialMeal: MealMacroDistribution = {
    calories: Math.round(dailyCalories / mealsCount),
    calories_percentage: Math.round(100 / mealsCount),
    protein_g: Math.round(dailyProtein / mealsCount),
    protein_percentage: Math.round(100 / mealsCount),
    carbs_g: Math.round(dailyCarbs / mealsCount),
    carbs_percentage: Math.round(100 / mealsCount),
    fats_g: Math.round(dailyFats / mealsCount),
    fats_percentage: Math.round(100 / mealsCount),
  }

  const [distribution, setDistribution] = useState<CustomMealDistribution>(() => {
    if (value) return value
    
    const initial: CustomMealDistribution = {}
    meals.forEach(meal => {
      initial[meal as keyof CustomMealDistribution] = { ...initialMeal }
    })
    return initial
  })

  // Calculate totals
  const totals = meals.reduce((acc, meal) => {
    const mealData = distribution[meal as keyof CustomMealDistribution]
    if (mealData) {
      acc.calories += mealData.calories
      acc.calories_percentage += mealData.calories_percentage
      acc.protein_g += mealData.protein_g
      acc.protein_percentage += mealData.protein_percentage
      acc.carbs_g += mealData.carbs_g
      acc.carbs_percentage += mealData.carbs_percentage
      acc.fats_g += mealData.fats_g
      acc.fats_percentage += mealData.fats_percentage
    }
    return acc
  }, {
    calories: 0,
    calories_percentage: 0,
    protein_g: 0,
    protein_percentage: 0,
    carbs_g: 0,
    carbs_percentage: 0,
    fats_g: 0,
    fats_percentage: 0,
  })

  const updateMealValue = (
    meal: string, 
    field: keyof MealMacroDistribution, 
    value: number
  ) => {
    const newDistribution = { ...distribution }
    if (!newDistribution[meal as keyof CustomMealDistribution]) {
      newDistribution[meal as keyof CustomMealDistribution] = { ...initialMeal }
    }
    
    const mealData = newDistribution[meal as keyof CustomMealDistribution]!
    mealData[field] = value

    // Update related fields
    if (field === 'calories') {
      mealData.calories_percentage = Math.round((value / dailyCalories) * 100)
    } else if (field === 'calories_percentage') {
      mealData.calories = Math.round((value / 100) * dailyCalories)
    } else if (field === 'protein_g') {
      mealData.protein_percentage = Math.round((value / dailyProtein) * 100)
    } else if (field === 'protein_percentage') {
      mealData.protein_g = Math.round((value / 100) * dailyProtein)
    } else if (field === 'carbs_g') {
      mealData.carbs_percentage = Math.round((value / dailyCarbs) * 100)
    } else if (field === 'carbs_percentage') {
      mealData.carbs_g = Math.round((value / 100) * dailyCarbs)
    } else if (field === 'fats_g') {
      mealData.fats_percentage = Math.round((value / dailyFats) * 100)
    } else if (field === 'fats_percentage') {
      mealData.fats_g = Math.round((value / 100) * dailyFats)
    }

    setDistribution(newDistribution)
    onChange(newDistribution)
  }

  // Check if totals are valid
  const isValid = (value: number, target: number, tolerance: number = 5) => {
    return Math.abs(value - target) <= tolerance
  }

  return (
    <Card className="mt-4">
      <CardHeader>
        <CardTitle>Distribución Personalizada</CardTitle>
        <CardDescription>
          Define la distribución de calorías y macronutrientes para cada comida.
          Los totales deben sumar 100% (±5% de tolerancia).
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Header */}
          <div className="grid grid-cols-9 gap-2 text-sm font-medium">
            <div>Comida</div>
            <div className="text-center">Calorías</div>
            <div className="text-center">% Cal</div>
            <div className="text-center">Prot (g)</div>
            <div className="text-center">% Prot</div>
            <div className="text-center">Carb (g)</div>
            <div className="text-center">% Carb</div>
            <div className="text-center">Grasa (g)</div>
            <div className="text-center">% Grasa</div>
          </div>

          {/* Meals */}
          {meals.map(meal => {
            const mealData = distribution[meal as keyof CustomMealDistribution]
            if (!mealData) return null

            return (
              <div key={meal} className="grid grid-cols-9 gap-2 items-center">
                <Label className="capitalize">{meal}</Label>
                
                <Input
                  type="number"
                  value={mealData.calories}
                  onChange={(e) => updateMealValue(meal, 'calories', parseInt(e.target.value) || 0)}
                  className="text-center"
                />
                <Input
                  type="number"
                  value={mealData.calories_percentage}
                  onChange={(e) => updateMealValue(meal, 'calories_percentage', parseInt(e.target.value) || 0)}
                  className="text-center"
                />
                
                <Input
                  type="number"
                  value={mealData.protein_g}
                  onChange={(e) => updateMealValue(meal, 'protein_g', parseInt(e.target.value) || 0)}
                  className="text-center"
                />
                <Input
                  type="number"
                  value={mealData.protein_percentage}
                  onChange={(e) => updateMealValue(meal, 'protein_percentage', parseInt(e.target.value) || 0)}
                  className="text-center"
                />
                
                <Input
                  type="number"
                  value={mealData.carbs_g}
                  onChange={(e) => updateMealValue(meal, 'carbs_g', parseInt(e.target.value) || 0)}
                  className="text-center"
                />
                <Input
                  type="number"
                  value={mealData.carbs_percentage}
                  onChange={(e) => updateMealValue(meal, 'carbs_percentage', parseInt(e.target.value) || 0)}
                  className="text-center"
                />
                
                <Input
                  type="number"
                  value={mealData.fats_g}
                  onChange={(e) => updateMealValue(meal, 'fats_g', parseInt(e.target.value) || 0)}
                  className="text-center"
                />
                <Input
                  type="number"
                  value={mealData.fats_percentage}
                  onChange={(e) => updateMealValue(meal, 'fats_percentage', parseInt(e.target.value) || 0)}
                  className="text-center"
                />
              </div>
            )
          })}

          {/* Totals */}
          <div className="grid grid-cols-9 gap-2 pt-4 border-t font-medium">
            <div>Total</div>
            <div className={`text-center ${!isValid(totals.calories, dailyCalories, dailyCalories * 0.05) ? 'text-red-500' : 'text-green-500'}`}>
              {totals.calories}
            </div>
            <div className={`text-center ${!isValid(totals.calories_percentage, 100) ? 'text-red-500' : 'text-green-500'}`}>
              {totals.calories_percentage}%
            </div>
            <div className={`text-center ${!isValid(totals.protein_g, dailyProtein, dailyProtein * 0.05) ? 'text-red-500' : 'text-green-500'}`}>
              {totals.protein_g}
            </div>
            <div className={`text-center ${!isValid(totals.protein_percentage, 100) ? 'text-red-500' : 'text-green-500'}`}>
              {totals.protein_percentage}%
            </div>
            <div className={`text-center ${!isValid(totals.carbs_g, dailyCarbs, dailyCarbs * 0.05) ? 'text-red-500' : 'text-green-500'}`}>
              {totals.carbs_g}
            </div>
            <div className={`text-center ${!isValid(totals.carbs_percentage, 100) ? 'text-red-500' : 'text-green-500'}`}>
              {totals.carbs_percentage}%
            </div>
            <div className={`text-center ${!isValid(totals.fats_g, dailyFats, dailyFats * 0.05) ? 'text-red-500' : 'text-green-500'}`}>
              {totals.fats_g}
            </div>
            <div className={`text-center ${!isValid(totals.fats_percentage, 100) ? 'text-red-500' : 'text-green-500'}`}>
              {totals.fats_percentage}%
            </div>
          </div>

          {/* Target values */}
          <div className="grid grid-cols-9 gap-2 text-sm text-muted-foreground">
            <div>Objetivo</div>
            <div className="text-center">{dailyCalories}</div>
            <div className="text-center">100%</div>
            <div className="text-center">{dailyProtein}</div>
            <div className="text-center">100%</div>
            <div className="text-center">{dailyCarbs}</div>
            <div className="text-center">100%</div>
            <div className="text-center">{dailyFats}</div>
            <div className="text-center">100%</div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}