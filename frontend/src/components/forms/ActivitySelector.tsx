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
      caminar_lento: { name: "Caminar (ritmo lento)", kcal_per_hour: 150, met: 2.5 },
      caminar_moderado: { name: "Caminar (ritmo moderado)", kcal_per_hour: 270, met: 3.5 },
      caminar_rapido: { name: "Caminar (ritmo rápido)", kcal_per_hour: 360, met: 4.5 },
      correr_lento: { name: "Correr (8 km/h)", kcal_per_hour: 480, met: 8.0 },
      correr_moderado: { name: "Correr (10 km/h)", kcal_per_hour: 600, met: 10.0 },
      correr_rapido: { name: "Correr (12 km/h)", kcal_per_hour: 720, met: 12.0 },
      bicicleta_paseo: { name: "Bicicleta (paseo)", kcal_per_hour: 240, met: 4.0 },
      bicicleta_moderado: { name: "Bicicleta (ritmo moderado)", kcal_per_hour: 420, met: 7.0 },
      bicicleta_intenso: { name: "Bicicleta (ritmo intenso)", kcal_per_hour: 600, met: 10.0 },
      natacion_suave: { name: "Natación (ritmo suave)", kcal_per_hour: 360, met: 6.0 },
      natacion_moderado: { name: "Natación (ritmo moderado)", kcal_per_hour: 420, met: 7.0 },
      natacion_intenso: { name: "Natación (ritmo intenso)", kcal_per_hour: 600, met: 10.0 },
      eliptica: { name: "Elíptica", kcal_per_hour: 400, met: 6.0 },
      remo: { name: "Máquina de remo", kcal_per_hour: 440, met: 7.0 },
      saltar_cuerda: { name: "Saltar la cuerda", kcal_per_hour: 600, met: 10.0 }
    }
  },
  fuerza: {
    name: "Fuerza/Gimnasio",
    activities: {
      pesas_ligero: { name: "Pesas (intensidad ligera)", kcal_per_hour: 180, met: 3.0 },
      pesas_moderado: { name: "Pesas (intensidad moderada)", kcal_per_hour: 270, met: 4.5 },
      pesas_intenso: { name: "Pesas (intensidad alta)", kcal_per_hour: 360, met: 6.0 },
      crossfit: { name: "CrossFit", kcal_per_hour: 600, met: 10.0 },
      calistenia: { name: "Calistenia", kcal_per_hour: 400, met: 6.5 }
    }
  },
  clases: {
    name: "Clases grupales",
    activities: {
      spinning: { name: "Spinning/Ciclismo indoor", kcal_per_hour: 500, met: 8.5 },
      zumba: { name: "Zumba", kcal_per_hour: 400, met: 6.5 },
      aerobicos: { name: "Aeróbicos", kcal_per_hour: 360, met: 6.0 },
      yoga: { name: "Yoga", kcal_per_hour: 180, met: 3.0 },
      yoga_power: { name: "Power Yoga", kcal_per_hour: 300, met: 5.0 },
      pilates: { name: "Pilates", kcal_per_hour: 210, met: 3.5 },
      boxeo: { name: "Boxeo (entrenamiento)", kcal_per_hour: 540, met: 9.0 }
    }
  },
  deportes: {
    name: "Deportes",
    activities: {
      futbol: { name: "Fútbol", kcal_per_hour: 500, met: 8.0 },
      basquet: { name: "Básquetbol", kcal_per_hour: 440, met: 7.5 },
      tenis: { name: "Tenis", kcal_per_hour: 400, met: 7.0 },
      paddle: { name: "Paddle", kcal_per_hour: 350, met: 6.0 },
      golf: { name: "Golf (caminando)", kcal_per_hour: 240, met: 4.0 },
      voleibol: { name: "Voleibol", kcal_per_hour: 270, met: 4.5 }
    }
  },
  recreativo: {
    name: "Actividades recreativas",
    activities: {
      baile_social: { name: "Baile social", kcal_per_hour: 270, met: 4.5 },
      senderismo: { name: "Senderismo/Trekking", kcal_per_hour: 340, met: 5.5 },
      escalada: { name: "Escalada", kcal_per_hour: 540, met: 9.0 }
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
    for (const [categoryKey, categoryData] of Object.entries(ACTIVITIES_DATABASE)) {
      if (activityKey in categoryData.activities) {
        const activity = categoryData.activities[activityKey as keyof typeof categoryData.activities]
        const kcalPerHour = activity.kcal_per_hour * (bodyWeight / 70) // Adjust for body weight
        const kcalPerSession = (kcalPerHour / 60) * duration
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
        activityData = categoryData.activities[selectedActivity as keyof typeof categoryData.activities]
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
                    {!activity.isManual && (
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