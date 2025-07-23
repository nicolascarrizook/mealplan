import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/components/ui/use-toast"
import { mealPlanService } from '@/services/api'
import { MealPlanDisplay } from '@/components/MealPlanDisplay'
import { FileUpload } from '@/components/FileUpload'
import { Loader2 } from 'lucide-react'
import type { ControlPatientData, MealPlanResponse } from '@/types'

const formSchema = z.object({
  nombre: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
  fecha_control: z.string(),
  peso_anterior: z.number().min(20).max(300),
  peso_actual: z.number().min(20).max(300),
  objetivo_actualizado: z.string().min(2),
  tipo_actividad_actual: z.string().min(2),
  frecuencia_actual: z.number().min(0).max(7),
  duracion_actual: z.number().min(0).max(300),
  agregar: z.string(),
  sacar: z.string(),
  dejar: z.string(),
  plan_anterior: z.string().min(10, 'Debe pegar el plan anterior completo'),
  tipo_peso: z.enum(['crudo', 'cocido']),
})

export function ControlForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [mealPlanResult, setMealPlanResult] = useState<MealPlanResponse | null>(null)
  const { toast } = useToast()

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      nombre: '',
      fecha_control: new Date().toISOString().split('T')[0],
      peso_anterior: 70,
      peso_actual: 69,
      objetivo_actualizado: 'Continuar bajando 0.5kg por semana',
      tipo_actividad_actual: 'Gym + cardio',
      frecuencia_actual: 4,
      duracion_actual: 60,
      agregar: '',
      sacar: '',
      dejar: '',
      plan_anterior: '',
      tipo_peso: 'crudo',
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    setMealPlanResult(null)
    
    try {
      const result = await mealPlanService.generateControlPlan(values as ControlPatientData)
      setMealPlanResult(result)
      toast({
        title: "Plan actualizado exitosamente",
        description: "El plan nutricional ha sido actualizado correctamente.",
      })
    } catch (error) {
      toast({
        title: "Error al actualizar el plan",
        description: "Hubo un problema al actualizar el plan. Por favor intenta nuevamente.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const pesoDiff = form.watch('peso_actual') - form.watch('peso_anterior')

  const handleDataExtracted = (data: Partial<ControlPatientData>) => {
    // Update form with extracted data
    if (data.nombre) form.setValue('nombre', data.nombre)
    if (data.fecha_control) form.setValue('fecha_control', data.fecha_control)
    if (data.peso_anterior) form.setValue('peso_anterior', data.peso_anterior)
    if (data.peso_actual) form.setValue('peso_actual', data.peso_actual)
    if (data.objetivo_actualizado) form.setValue('objetivo_actualizado', data.objetivo_actualizado)
    if (data.tipo_actividad_actual) form.setValue('tipo_actividad_actual', data.tipo_actividad_actual)
    if (data.frecuencia_actual) form.setValue('frecuencia_actual', data.frecuencia_actual)
    if (data.duracion_actual) form.setValue('duracion_actual', data.duracion_actual)
    if (data.agregar) form.setValue('agregar', data.agregar)
    if (data.sacar) form.setValue('sacar', data.sacar)
    if (data.dejar) form.setValue('dejar', data.dejar)
    if (data.plan_anterior) form.setValue('plan_anterior', data.plan_anterior)
    
    toast({
      title: "Datos cargados",
      description: "Se han pre-llenado los campos con los datos extraídos. Por favor, revisa y completa la información faltante.",
    })
  }

  return (
    <>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          {/* File Upload Section */}
          <FileUpload onDataExtracted={handleDataExtracted} />

          <Card>
            <CardHeader>
              <CardTitle>Datos del Control</CardTitle>
              <CardDescription>Información del paciente en el control actual</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="nombre"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nombre del paciente</FormLabel>
                    <FormControl>
                      <Input placeholder="Juan Pérez" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="fecha_control"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Fecha del control</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="peso_anterior"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Peso anterior (kg)</FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        step="0.1" 
                        {...field} 
                        onChange={e => field.onChange(parseFloat(e.target.value))} 
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="peso_actual"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Peso actual (kg)</FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        step="0.1" 
                        {...field} 
                        onChange={e => field.onChange(parseFloat(e.target.value))} 
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="md:col-span-2 p-4 bg-gray-50 rounded-lg">
                <p className="text-sm font-medium">
                  Diferencia de peso: {' '}
                  <span className={pesoDiff < 0 ? 'text-green-600' : pesoDiff > 0 ? 'text-red-600' : 'text-gray-600'}>
                    {pesoDiff > 0 ? '+' : ''}{pesoDiff.toFixed(1)} kg
                  </span>
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Actualización de Objetivo</CardTitle>
              <CardDescription>Nuevo objetivo basado en los resultados</CardDescription>
            </CardHeader>
            <CardContent>
              <FormField
                control={form.control}
                name="objetivo_actualizado"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Objetivo actualizado</FormLabel>
                    <FormControl>
                      <Input 
                        placeholder="Ej: Continuar bajando 0.5kg por semana"
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
              <CardTitle>Actividad Física Actual</CardTitle>
              <CardDescription>Cambios en la actividad física</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="tipo_actividad_actual"
                render={({ field }) => (
                  <FormItem className="md:col-span-2">
                    <FormLabel>Tipo de actividad actual</FormLabel>
                    <FormControl>
                      <Input placeholder="Ej: Gym + cardio" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="frecuencia_actual"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Frecuencia actual (veces/semana)</FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        min="0" 
                        max="7" 
                        {...field} 
                        onChange={e => field.onChange(parseInt(e.target.value))} 
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="duracion_actual"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Duración actual (minutos)</FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        min="0" 
                        max="300" 
                        {...field} 
                        onChange={e => field.onChange(parseInt(e.target.value))} 
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
              <CardTitle>Ajustes al Plan</CardTitle>
              <CardDescription>Modificaciones solicitadas para el nuevo plan</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                control={form.control}
                name="agregar"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>AGREGAR</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="¿Qué alimentos o comidas desea agregar?"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Especifique alimentos o preparaciones que desea incluir
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="sacar"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>SACAR</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="¿Qué alimentos o comidas desea eliminar?"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Especifique alimentos o preparaciones que desea quitar
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="dejar"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>DEJAR</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="¿Qué aspectos del plan desea mantener?"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Especifique elementos que funcionaron bien y desea conservar
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Plan Anterior</CardTitle>
              <CardDescription>Pegue el plan nutricional anterior completo</CardDescription>
            </CardHeader>
            <CardContent>
              <FormField
                control={form.control}
                name="plan_anterior"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Plan anterior completo</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="Pegue aquí el plan nutricional anterior completo..."
                        className="resize-none min-h-[200px]"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Copie y pegue todo el contenido del plan anterior
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="tipo_peso"
                render={({ field }) => (
                  <FormItem className="mt-4">
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
                Actualizando plan...
              </>
            ) : (
              'Actualizar Plan Nutricional'
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