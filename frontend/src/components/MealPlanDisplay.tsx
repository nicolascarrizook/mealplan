import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { mealPlanService } from "@/services/api"
import { Download, Loader2 } from "lucide-react"

interface MealPlanDisplayProps {
  mealPlan: string
  pdfPath: string
}

export function MealPlanDisplay({ mealPlan, pdfPath }: MealPlanDisplayProps) {
  const [isDownloading, setIsDownloading] = useState(false)

  const handleDownload = () => {
    setIsDownloading(true)
    mealPlanService.downloadPdf(pdfPath)
    setTimeout(() => setIsDownloading(false), 2000)
  }

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