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
import { Loader2 } from 'lucide-react'
import type { MealReplacementData, MealPlanResponse } from '@/types'

const formSchema = z.object({
  paciente: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
  comida_reemplazar: z.enum(['desayuno', 'almuerzo', 'merienda', 'cena']),
  nueva_comida: z.string().min(5, 'Describa la nueva comida deseada'),
  condiciones: z.string().optional(),
  comida_actual: z.string().min(10, 'Debe describir la comida actual completa'),
  proteinas: z.number().min(0).max(200),
  carbohidratos: z.number().min(0).max(300),
  grasas: z.number().min(0).max(150),
  calorias: z.number().min(0).max(2000),
  tipo_peso: z.enum(['crudo', 'cocido']),
})

export function MealReplacementForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [mealPlanResult, setMealPlanResult] = useState<MealPlanResponse | null>(null)
  const { toast } = useToast()

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      paciente: '',
      comida_reemplazar: 'desayuno',
      nueva_comida: '',
      condiciones: '',
      comida_actual: '',
      proteinas: 0,
      carbohidratos: 0,
      grasas: 0,
      calorias: 0,
      tipo_peso: 'crudo',
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true)
    setMealPlanResult(null)
    
    try {
      const result = await mealPlanService.replaceMeal(values as MealReplacementData)
      setMealPlanResult(result)
      toast({
        title: "Reemplazo generado exitosamente",
        description: "La nueva opción de comida ha sido creada manteniendo los macros.",
      })
    } catch (error) {
      toast({
        title: "Error al generar el reemplazo",
        description: "Hubo un problema al generar el reemplazo. Por favor intenta nuevamente.",
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
              <CardTitle>Información del Paciente</CardTitle>
              <CardDescription>Datos del paciente y comida a reemplazar</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="paciente"
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
                name="comida_reemplazar"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Comida a reemplazar</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar comida" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="desayuno">Desayuno</SelectItem>
                        <SelectItem value="almuerzo">Almuerzo</SelectItem>
                        <SelectItem value="merienda">Merienda</SelectItem>
                        <SelectItem value="cena">Cena</SelectItem>
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
              <CardTitle>Comida Actual</CardTitle>
              <CardDescription>Describa la comida actual que desea reemplazar</CardDescription>
            </CardHeader>
            <CardContent>
              <FormField
                control={form.control}
                name="comida_actual"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Descripción completa de la comida actual</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder={`Ejemplo:
- Avena: 40g
- Banana: 100g
- Mantequilla de maní: 10g
- Leche descremada: 200ml
Preparación: Cocinar la avena con leche, agregar banana cortada y mantequilla de maní`}
                        className="resize-none min-h-[150px]"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Incluya todos los ingredientes con sus cantidades y forma de preparación
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Macros de la Comida Actual</CardTitle>
              <CardDescription>Información nutricional que debe mantenerse</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <FormField
                control={form.control}
                name="proteinas"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Proteínas (g)</FormLabel>
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
                name="carbohidratos"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Carbohidratos (g)</FormLabel>
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
                name="grasas"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Grasas (g)</FormLabel>
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
                name="calorias"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Calorías</FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        {...field} 
                        onChange={e => field.onChange(parseInt(e.target.value))} 
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="col-span-2 md:col-span-4 p-4 bg-gray-50 rounded-lg mt-2">
                <p className="text-sm text-gray-600">
                  <strong>Tolerancia permitida:</strong> ±5g en proteínas y carbohidratos, ±3g en grasas, ±50 kcal
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Nueva Comida Deseada</CardTitle>
              <CardDescription>Especifique qué tipo de comida desea como reemplazo</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FormField
                control={form.control}
                name="nueva_comida"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Descripción de la nueva comida</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="Ej: Tostadas con huevo y palta, o un bowl de yogur con frutas y granola"
                        className="resize-none"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Describa el tipo de comida que prefiere como reemplazo
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="condiciones"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Condiciones especiales (opcional)</FormLabel>
                    <FormControl>
                      <Textarea 
                        placeholder="Ej: Sin lácteos, sin gluten, preparación rápida, etc."
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
            </CardContent>
          </Card>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generando reemplazo...
              </>
            ) : (
              'Generar Reemplazo de Comida'
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