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
import type { NewPatientData, MealPlanResponse } from '@/types'

const formSchema = z.object({
  nombre: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
  edad: z.number().min(1).max(120),
  sexo: z.enum(['masculino', 'femenino']),
  estatura: z.number().min(50).max(250),
  peso: z.number().min(20).max(300),
  objetivo: z.enum(['bajar', 'subir', 'mantener']),
  objetivo_semanal: z.string().optional(),
  tipo_actividad: z.string().min(2),
  frecuencia_semanal: z.number().min(0).max(7),
  duracion_sesion: z.number().min(0).max(300),
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
  nivel_economico: z.enum(['Sin restricciones', 'Medio', 'Limitado', 'Bajo recursos']),
  notas_personales: z.string().optional(),
  comidas_principales: z.number().min(3).max(4),
  colaciones: z.enum(['No', 'Por saciedad', 'Pre-entreno', 'Post-entreno']),
  tipo_peso: z.enum(['crudo', 'cocido']),
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
      sexo: 'masculino',
      estatura: 170,
      peso: 70,
      objetivo: 'mantener',
      tipo_actividad: 'Sedentario',
      frecuencia_semanal: 3,
      duracion_sesion: 60,
      horarios: {
        desayuno: '08:00',
        almuerzo: '13:00',
        merienda: '17:00',
        cena: '21:00',
      },
      nivel_economico: 'Medio',
      comidas_principales: 4,
      colaciones: 'No',
      tipo_peso: 'crudo',
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
                        <SelectItem value="masculino">Masculino</SelectItem>
                        <SelectItem value="femenino">Femenino</SelectItem>
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
                            <RadioGroupItem value="bajar" />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Bajar de peso
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value="subir" />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Subir de peso
                          </FormLabel>
                        </FormItem>
                        <FormItem className="flex items-center space-x-3 space-y-0">
                          <FormControl>
                            <RadioGroupItem value="mantener" />
                          </FormControl>
                          <FormLabel className="font-normal">
                            Mantener peso
                          </FormLabel>
                        </FormItem>
                      </RadioGroup>
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {(form.watch('objetivo') === 'bajar' || form.watch('objetivo') === 'subir') && (
                <FormField
                  control={form.control}
                  name="objetivo_semanal"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Objetivo semanal</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Seleccionar objetivo semanal" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="0.5kg">0.5 kg por semana</SelectItem>
                          <SelectItem value="1kg">1 kg por semana</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}
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
                    <FormLabel>Duración por sesión (minutos)</FormLabel>
                    <FormControl>
                      <Input type="number" min="0" max="300" {...field} onChange={e => field.onChange(parseInt(e.target.value))} />
                    </FormControl>
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
                        <SelectItem value="Sin restricciones">Sin restricciones</SelectItem>
                        <SelectItem value="Medio">Medio</SelectItem>
                        <SelectItem value="Limitado">Limitado</SelectItem>
                        <SelectItem value="Bajo recursos">Bajo recursos</SelectItem>
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
                        <SelectItem value="No">No</SelectItem>
                        <SelectItem value="Por saciedad">Por saciedad</SelectItem>
                        <SelectItem value="Pre-entreno">Pre-entreno</SelectItem>
                        <SelectItem value="Post-entreno">Post-entreno</SelectItem>
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
                        <SelectItem value="crudo">Peso crudo</SelectItem>
                        <SelectItem value="cocido">Peso cocido</SelectItem>
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