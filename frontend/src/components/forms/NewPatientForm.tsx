import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/components/ui/use-toast"
import { mealPlanService } from '@/services/api'
import { MealPlanDisplay } from '@/components/MealPlanDisplay'
import { Loader2 } from 'lucide-react'
import type { 
  NewPatientData, 
  MealPlanResponse,
  Sexo,
  Objetivo,
  NivelEconomico,
  TipoPeso,
  TipoColacion,
  ProteinLevel,
  DistributionType
} from '@/types'

const formSchema = z.object({
  nombre: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
  edad: z.number().min(1).max(120),
  sexo: z.nativeEnum(Sexo),
  estatura: z.number().min(50).max(250),
  peso: z.number().min(20).max(300),
  objetivo: z.nativeEnum(Objetivo),
  tipo_actividad: z.string().min(2),
  frecuencia_semanal: z.number().min(0).max(7),
  duracion_sesion: z.enum([30, 45, 60, 75, 90, 120]),
  suplementacion: z.string().optional(),
  patologias: z.string().optional(),
  no_consume: z.string().optional(),
  le_gusta: z.string().optional(),
  horarios: z.object({
    desayuno: z.string(),
    almuerzo: z.string(),
    merienda: z.string(),
    cena: z.string(),
  }),
  nivel_economico: z.nativeEnum(NivelEconomico),
  notas_personales: z.string().optional(),
  comidas_principales: z.number().min(3).max(4),
  colaciones: z.nativeEnum(TipoColacion),
  tipo_peso: z.nativeEnum(TipoPeso),
  // Nuevos campos
  carbs_percentage: z.number().min(5).max(65).multipleOf(5).optional(),
  protein_level: z.nativeEnum(ProteinLevel).optional(),
  fat_percentage: z.number().min(15).max(45).optional(),
  distribution_type: z.nativeEnum(DistributionType),
})

export function NewPatientForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [mealPlanResult, setMealPlanResult] = useState<MealPlanResponse | null>(null)
  const { toast } = useToast()

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      nombre: '',
      edad: 30,
      sexo: Sexo.masculino,
      estatura: 170,
      peso: 70,
      objetivo: Objetivo.mantener,
      tipo_actividad: 'Sedentario',
      frecuencia_semanal: 3,
      duracion_sesion: 60,
      horarios: {
        desayuno: '08:00',
        almuerzo: '13:00',
        merienda: '17:00',
        cena: '21:00',
      },
      nivel_economico: NivelEconomico.medio,
      notas_personales: '',
      comidas_principales: 4,
      colaciones: TipoColacion.no,
      tipo_peso: TipoPeso.crudo,
      distribution_type: DistributionType.traditional,
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    setMealPlanResult(null)
    
    try {
      const result = await mealPlanService.generateNewPatientPlan(values as NewPatientData)
      setMealPlanResult(result)
      toast({
        title: "Plan generado exitosamente",
        description: "El plan nutricional ha sido creado correctamente.",
      })
    } catch (error) {
      toast({
        title: "Error al generar el plan",
        description: "Hubo un problema al generar el plan. Por favor intenta nuevamente.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Datos Personales</CardTitle>
              <CardDescription>Información básica del paciente</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="nombre"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nombre completo</FormLabel>
                    <FormControl>
                      <Input placeholder="Juan Pérez" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="edad"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Edad</FormLabel>
                    <FormControl>
                      <Input type="number" {...field} onChange={e => field.onChange(parseInt(e.target.value))} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="sexo"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Sexo</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar sexo" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value={Sexo.masculino}>Masculino</SelectItem>
                        <SelectItem value={Sexo.femenino}>Femenino</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="estatura"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Estatura (cm)</FormLabel>
                    <FormControl>
                      <Input type="number" {...field} onChange={e => field.onChange(parseFloat(e.target.value))} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="peso"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Peso (kg)</FormLabel>
                    <FormControl>
                      <Input type="number" step="0.1" {...field} onChange={e => field.onChange(parseFloat(e.target.value))} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Objetivo</CardTitle>
              <CardDescription>¿Cuál es el objetivo del paciente?</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                control={form.control}
                name="objetivo"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Objetivo principal</FormLabel>
                    <FormControl>
                      <RadioGroup
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                        className="flex flex-col space-y-1"
                      >
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.mantener} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Mantener peso
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.bajar_025} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Bajar 0.25 kg/semana
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.bajar_05} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Bajar 0.5 kg/semana
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.bajar_075} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Bajar 0.75 kg/semana
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.bajar_1} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Bajar 1 kg/semana
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.subir_025} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Subir 0.25 kg/semana
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.subir_05} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Subir 0.5 kg/semana
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.subir_075} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Subir 0.75 kg/semana
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value={Objetivo.subir_1} />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Subir 1 kg/semana
                          </FormLabel>
                        </FormItem>
                      </RadioGroup>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Actividad Física</CardTitle>
              <CardDescription>Información sobre la actividad física del paciente</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="tipo_actividad"
                render={({ field }) => (
                  <FormItem className="md:col-span-2">
                    <FormLabel>Tipo de actividad</FormLabel>
                    <FormControl>
                      <Input placeholder="Ej: Caminar, correr, gym, natación" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="frecuencia_semanal"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Frecuencia semanal</FormLabel>
                    <FormControl>
                      <Input type="number" min="0" max="7" {...field} onChange={e => field.onChange(parseInt(e.target.value))} />
                    </FormControl>
                    <FormDescription>Veces por semana</FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="duracion_sesion"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Duración por sesión</FormLabel>
                    <Select onValueChange={(value) => field.onChange(parseInt(value))} defaultValue={field.value?.toString()}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar duración" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="30">30 minutos</SelectItem>
                        <SelectItem value="45">45 minutos</SelectItem>
                        <SelectItem value="60">60 minutos</SelectItem>
                        <SelectItem value="75">75 minutos</SelectItem>
                        <SelectItem value="90">90 minutos</SelectItem>
                        <SelectItem value="120">120 minutos</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Especificaciones Médicas</CardTitle>
              <CardDescription>Información médica y restricciones alimentarias</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                control={form.control}
                name="suplementacion"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Suplementación</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="Indicar si toma algún suplemento (opcional)"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="patologias"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Patologías / Medicación</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="Indicar patologías o medicación actual (opcional)"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="no_consume"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Alimentos que NO consume</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="Ej: lácteos, gluten, mariscos (opcional)"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="le_gusta"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Alimentos que le gustan</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="Indicar preferencias alimentarias (opcional)"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Horarios de Comidas</CardTitle>
              <CardDescription>Horarios habituales para cada comida</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="horarios.desayuno"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Desayuno</FormLabel>
                    <FormControl>
                      <Input type="time" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="horarios.almuerzo"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Almuerzo</FormLabel>
                    <FormControl>
                      <Input type="time" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="horarios.merienda"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Merienda</FormLabel>
                    <FormControl>
                      <Input type="time" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="horarios.cena"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Cena</FormLabel>
                    <FormControl>
                      <Input type="time" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Configuración del Plan</CardTitle>
              <CardDescription>Parámetros adicionales para el plan nutricional</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                control={form.control}
                name="nivel_economico"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nivel económico</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar nivel económico" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value={NivelEconomico.sin_restricciones}>{NivelEconomico.sin_restricciones}</SelectItem>
                        <SelectItem value={NivelEconomico.medio}>{NivelEconomico.medio}</SelectItem>
                        <SelectItem value={NivelEconomico.limitado}>{NivelEconomico.limitado}</SelectItem>
                        <SelectItem value={NivelEconomico.bajo_recursos}>{NivelEconomico.bajo_recursos}</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="comidas_principales"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Número de comidas principales</FormLabel>
                    <Select onValueChange={(value) => field.onChange(parseInt(value))} defaultValue={field.value.toString()}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar cantidad" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="3">3 comidas</SelectItem>
                        <SelectItem value="4">4 comidas</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="colaciones"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Colaciones</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar tipo de colación" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value={TipoColacion.no}>{TipoColacion.no}</SelectItem>
                        <SelectItem value={TipoColacion.por_saciedad}>{TipoColacion.por_saciedad}</SelectItem>
                        <SelectItem value={TipoColacion.pre_entreno}>{TipoColacion.pre_entreno}</SelectItem>
                        <SelectItem value={TipoColacion.post_entreno}>{TipoColacion.post_entreno}</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="tipo_peso"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Tipo de peso</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar tipo de peso" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value={TipoPeso.crudo}>Peso crudo</SelectItem>
                        <SelectItem value={TipoPeso.cocido}>Peso cocido</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormDescription>
                      Las cantidades se mostrarán en gramos de alimento {field.value}
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="notas_personales"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Notas adicionales</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="Cualquier información adicional relevante (opcional)"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Personalización de Macronutrientes</CardTitle>
              <CardDescription>Configuración avanzada de macros (opcional)</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                control={form.control}
                name="protein_level"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nivel de proteína</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar nivel de proteína" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value={ProteinLevel.muy_baja}>Muy baja (0.5-0.8 g/kg) - Patologías renales</SelectItem>
                        <SelectItem value={ProteinLevel.conservada}>Conservada (0.8-1.2 g/kg) - Normal</SelectItem>
                        <SelectItem value={ProteinLevel.moderada}>Moderada (1.2-1.6 g/kg) - Personas activas</SelectItem>
                        <SelectItem value={ProteinLevel.alta}>Alta (1.6-2.2 g/kg) - Uso deportivo</SelectItem>
                        <SelectItem value={ProteinLevel.muy_alta}>Muy alta (2.2-2.8 g/kg) - Alto rendimiento</SelectItem>
                        <SelectItem value={ProteinLevel.extrema}>Extrema (3.0-3.5 g/kg) - Requerimientos especiales</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="carbs_percentage"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Porcentaje de carbohidratos</FormLabel>
                    <Select onValueChange={(value) => field.onChange(parseInt(value))} defaultValue={field.value?.toString()}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar porcentaje de carbohidratos" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="20">20%</SelectItem>
                        <SelectItem value="25">25%</SelectItem>
                        <SelectItem value="30">30%</SelectItem>
                        <SelectItem value="35">35%</SelectItem>
                        <SelectItem value="40">40%</SelectItem>
                        <SelectItem value="45">45%</SelectItem>
                        <SelectItem value="50">50%</SelectItem>
                        <SelectItem value="55">55%</SelectItem>
                        <SelectItem value="60">60%</SelectItem>
                        <SelectItem value="65">65%</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormDescription>
                      Porcentaje del total calórico diario
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="fat_percentage"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Porcentaje de grasas</FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        min="15" 
                        max="45" 
                        placeholder="15-45%"
                        {...field} 
                        onChange={e => field.onChange(parseInt(e.target.value) || undefined)} 
                      />
                    </FormControl>
                    <FormDescription>
                      Porcentaje del total calórico diario (15-45%)
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="distribution_type"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Tipo de distribución calórica</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar tipo de distribución" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value={DistributionType.traditional}>Tradicional (más calorías en almuerzo)</SelectItem>
                        <SelectItem value={DistributionType.equitable}>Equitativa (mismas calorías en cada comida)</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
          </Card>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generando plan...
              </>
            ) : (
              'Generar Plan Nutricional'
            )}
          </Button>
        </form>
      </Form>

      {mealPlanResult && (
        <MealPlanDisplay 
          mealPlan={mealPlanResult.meal_plan} 
          pdfPath={mealPlanResult.pdf_path} 
        />
      )}
    </>
  )
}