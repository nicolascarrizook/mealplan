import { useState, useEffect } from 'react'
import { X, Plus, Calculator } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

// Activity database imported from backend structure
const ACTIVITIES_DATABASE = {
  cardiovascular: {
    name: "Cardiovascular",
    activities: {
      caminar_lento: { name: "Caminata lenta (recreativa)", kcal_per_minute: 3.5, kcal_per_hour: 210 },
      caminar_rapido: { name: "Caminata rápida", kcal_per_minute: 4.5, kcal_per_hour: 270 },
      running_moderado: { name: "Running (trote medio, 8-10 km/h)", kcal_per_minute: 11, kcal_per_hour: 660 },
      running_intenso: { name: "Running (fondo o competitivo)", kcal_per_minute: 13.5, kcal_per_hour: 810 },
      bicicleta_urbana: { name: "Bicicleta urbana (traslado)", kcal_per_minute: 5.5, kcal_per_hour: 330 },
      bicicleta_entrenamiento: { name: "Bicicleta entrenamiento (ritmo moderado)", kcal_per_minute: 10.5, kcal_per_hour: 630 },
      bicicleta_fondo: { name: "Bicicleta fondo (>80 km)", kcal_per_minute: 14.5, kcal_per_hour: 870 },
      natacion_recreativa: { name: "Natación recreativa", kcal_per_minute: 8, kcal_per_hour: 480 },
      natacion_competicion: { name: "Natación de competición", kcal_per_minute: 11.5, kcal_per_hour: 690 },
      trekking: { name: "Trekking (moderado)", kcal_per_minute: 6, kcal_per_hour: 360 },
      eliptica: { name: "Elíptica", kcal_per_hour: 400 },
      remo: { name: "Máquina de remo", kcal_per_hour: 440 },
      saltar_cuerda: { name: "Saltar la cuerda", kcal_per_hour: 600 }
    }
  },
  fuerza: {
    name: "Fuerza/Gimnasio",
    activities: {
      pesas_aparatos: { name: "Pesas / Aparatos", kcal_per_minute: 5.5, kcal_per_hour: 330 },
      calistenia: { name: "Calistenia", kcal_per_minute: 6.5, kcal_per_hour: 390 },
      crossfit: { name: "CrossFit", kcal_per_minute: 11, kcal_per_hour: 660 },
      funcional_hiit: { name: "Entrenamiento Funcional / HIIT", kcal_per_minute: 9, kcal_per_hour: 540 }
    }
  },
  clases: {
    name: "Clases grupales",
    activities: {
      spinning: { name: "Spinning/Ciclismo indoor", kcal_per_hour: 500 },
      zumba: { name: "Zumba", kcal_per_hour: 400 },
      aerobicos: { name: "Aeróbicos", kcal_per_hour: 360 },
      yoga: { name: "Yoga", kcal_per_hour: 180 },
      yoga_power: { name: "Power Yoga", kcal_per_hour: 300 },
      pilates: { name: "Pilates", kcal_per_hour: 210 },
      boxeo: { name: "Boxeo (entrenamiento)", kcal_per_hour: 540 }
    }
  },
  deportes: {
    name: "Deportes",
    activities: {
      futbol: { name: "Fútbol", kcal_per_hour: 500 },
      basquet: { name: "Básquetbol", kcal_per_hour: 440 },
      tenis: { name: "Tenis", kcal_per_hour: 400 },
      paddle: { name: "Paddle", kcal_per_hour: 350 },
      golf: { name: "Golf (caminando)", kcal_per_hour: 240 },
      voleibol: { name: "Voleibol", kcal_per_hour: 270 }
    }
  },
  recreativo: {
    name: "Actividades recreativas",
    activities: {
      baile_social: { name: "Baile social", kcal_per_hour: 270 },
      senderismo: { name: "Senderismo/Trekking", kcal_per_hour: 340 },
      escalada: { name: "Escalada", kcal_per_hour: 540 }
    }
  }
}

interface Activity {
  id: string
  name: string
  duration: number
  frequency: number
  calories: number
  isManual?: boolean
}

interface ActivitySelectorProps {
  activities: Activity[]
  onChange: (activities: Activity[]) => void
  bodyWeight?: number
}

export function ActivitySelector({ activities, onChange, bodyWeight = 70 }: ActivitySelectorProps) {
  const [selectedActivities, setSelectedActivities] = useState<Activity[]>(activities || [])
  const [selectedCategory, setSelectedCategory] = useState<string>('cardiovascular')
  const [selectedActivity, setSelectedActivity] = useState<string>('')
  const [duration, setDuration] = useState<number>(30)
  const [frequency, setFrequency] = useState<number>(3)
  const [manualCalories, setManualCalories] = useState<number>(0)

  useEffect(() => {
    onChange(selectedActivities)
  }, [selectedActivities])

  const calculateCalories = (activityKey: string, duration: number, frequency: number) => {
    // Find the category that contains this activity
    for (const [_, categoryData] of Object.entries(ACTIVITIES_DATABASE)) {
      if (activityKey in categoryData.activities) {
        const activity = (categoryData.activities as any)[activityKey]
        
        // Use the new formula: (Kcal/min x peso paciente / 70) x duración en minutos
        let kcalPerSession: number
        if ('kcal_per_minute' in activity) {
          kcalPerSession = (activity.kcal_per_minute * bodyWeight / 70) * duration
        } else {
          // Fallback for activities without kcal_per_minute
          const kcalPerHour = activity.kcal_per_hour * (bodyWeight / 70)
          kcalPerSession = (kcalPerHour / 60) * duration
        }
        
        const kcalPerWeek = kcalPerSession * frequency
        const kcalPerDay = kcalPerWeek / 7
        
        return Math.round(kcalPerDay)
      }
    }
    
    return 0
  }

  const addActivity = () => {
    if (!selectedActivity) return

    // Find the activity in the database
    let activityData: any = null
    for (const categoryData of Object.values(ACTIVITIES_DATABASE)) {
      if (selectedActivity in categoryData.activities) {
        activityData = (categoryData.activities as any)[selectedActivity]
        break
      }
    }
    
    if (!activityData) return

    const calories = calculateCalories(selectedActivity, duration, frequency)

    const newActivity: Activity = {
      id: `${selectedActivity}_${Date.now()}`,
      name: activityData.name,
      duration,
      frequency,
      calories
    }

    setSelectedActivities([...selectedActivities, newActivity])
    
    // Reset form
    setSelectedActivity('')
    setDuration(30)
    setFrequency(3)
  }

  const addManualActivity = () => {
    if (manualCalories <= 0) return

    const newActivity: Activity = {
      id: `manual_${Date.now()}`,
      name: "Actividad personalizada (reloj inteligente)",
      duration: 0,
      frequency: 0,
      calories: manualCalories,
      isManual: true
    }

    setSelectedActivities([...selectedActivities, newActivity])
    setManualCalories(0)
  }

  const removeActivity = (id: string) => {
    setSelectedActivities(selectedActivities.filter(a => a.id !== id))
  }

  const totalCalories = selectedActivities.reduce((sum, activity) => sum + activity.calories, 0)

  return (
    <div className="space-y-4">
      <Tabs defaultValue="automatic" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="automatic">Actividades Predefinidas</TabsTrigger>
          <TabsTrigger value="manual">Ingreso Manual</TabsTrigger>
        </TabsList>
        
        <TabsContent value="automatic" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label>Categoría</Label>
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(ACTIVITIES_DATABASE).map(([key, category]) => (
                    <SelectItem key={key} value={key}>
                      {category.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label>Actividad</Label>
              <Select value={selectedActivity} onValueChange={setSelectedActivity}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona una actividad" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(ACTIVITIES_DATABASE[selectedCategory as keyof typeof ACTIVITIES_DATABASE].activities).map(([key, activity]) => (
                    <SelectItem key={key} value={key}>
                      {activity.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label>Duración (minutos)</Label>
              <Input
                type="number"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                min={5}
                max={240}
                step={5}
              />
            </div>

            <div>
              <Label>Frecuencia semanal</Label>
              <Input
                type="number"
                value={frequency}
                onChange={(e) => setFrequency(Number(e.target.value))}
                min={1}
                max={7}
              />
            </div>
          </div>

          {selectedActivity && (
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-2">
                <Calculator className="w-4 h-4 text-blue-600" />
                <span className="text-sm">
                  Gasto estimado: <strong>{calculateCalories(selectedActivity, duration, frequency)} kcal/día</strong>
                </span>
              </div>
              <Button onClick={addActivity} size="sm">
                <Plus className="w-4 h-4 mr-1" />
                Agregar
              </Button>
            </div>
          )}
        </TabsContent>

        <TabsContent value="manual" className="space-y-4">
          <div className="space-y-2">
            <Label>Calorías diarias (según reloj inteligente)</Label>
            <div className="flex gap-2">
              <Input
                type="number"
                value={manualCalories}
                onChange={(e) => setManualCalories(Number(e.target.value))}
                placeholder="Ej: 450"
                min={0}
              />
              <Button onClick={addManualActivity} disabled={manualCalories <= 0}>
                <Plus className="w-4 h-4 mr-1" />
                Agregar
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">
              Ingresa el gasto calórico diario promedio reportado por tu dispositivo
            </p>
          </div>
        </TabsContent>
      </Tabs>

      {selectedActivities.length > 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-3">
              <div className="flex justify-between items-center mb-2">
                <h4 className="font-medium">Actividades seleccionadas</h4>
                <Badge variant="secondary">
                  Total: {totalCalories} kcal/día
                </Badge>
              </div>
              
              {selectedActivities.map((activity) => (
                <div key={activity.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-sm">{activity.name}</p>
                    {!activity.isManual && activity.duration && activity.frequency && (
                      <p className="text-xs text-muted-foreground">
                        {activity.duration} min • {activity.frequency}x/semana
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">{activity.calories} kcal/día</Badge>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeActivity(activity.id)}
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}