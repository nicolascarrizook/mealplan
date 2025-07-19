import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Toaster } from "@/components/ui/toaster"
import { NewPatientForm } from "@/components/forms/NewPatientForm"
import { ControlForm } from "@/components/forms/ControlForm"
import { MealReplacementForm } from "@/components/forms/MealReplacementForm"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Meal Planner Pro</h1>
          <p className="text-sm text-gray-600">Sistema de Planes Nutricionales - Tres Días y Carga</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Generador de Planes Nutricionales</CardTitle>
            <CardDescription>
              Selecciona el tipo de plan que deseas generar
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="new-patient" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="new-patient">Paciente Nuevo</TabsTrigger>
                <TabsTrigger value="control">Control de Paciente</TabsTrigger>
                <TabsTrigger value="replacement">Reemplazo de Comida</TabsTrigger>
              </TabsList>
              
              <TabsContent value="new-patient" className="mt-6">
                <NewPatientForm />
              </TabsContent>
              
              <TabsContent value="control" className="mt-6">
                <ControlForm />
              </TabsContent>
              
              <TabsContent value="replacement" className="mt-6">
                <MealReplacementForm />
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </main>

      <Toaster />
    </div>
  )
}

export default App