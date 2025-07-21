import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Info } from "lucide-react"

export enum T4Timing {
  con_fibra_2h = "con_fibra_2h",
  sin_fibra_30min = "sin_fibra_30min"
}

interface T4TimingSelectorProps {
  value?: T4Timing
  onChange: (timing: T4Timing) => void
}

export function T4TimingSelector({ value, onChange }: T4TimingSelectorProps) {
  return (
    <div className="space-y-4">
      <Alert>
        <Info className="h-4 w-4" />
        <AlertDescription>
          La levotiroxina (T4) requiere consideraciones especiales para su absorción
        </AlertDescription>
      </Alert>
      
      <RadioGroup value={value} onValueChange={(val) => onChange(val as T4Timing)}>
        <div className="space-y-3">
          <div className="flex items-start space-x-3">
            <RadioGroupItem value={T4Timing.sin_fibra_30min} id="sin_fibra" />
            <div className="grid gap-1.5 leading-none">
              <Label htmlFor="sin_fibra" className="font-medium cursor-pointer">
                Desayuno sin fibra (30 min - 1 hora después)
              </Label>
              <p className="text-sm text-muted-foreground">
                Permite desayunar más temprano pero sin alimentos con fibra
              </p>
            </div>
          </div>
          
          <div className="flex items-start space-x-3">
            <RadioGroupItem value={T4Timing.con_fibra_2h} id="con_fibra" />
            <div className="grid gap-1.5 leading-none">
              <Label htmlFor="con_fibra" className="font-medium cursor-pointer">
                Desayuno con fibra (2 horas después)
              </Label>
              <p className="text-sm text-muted-foreground">
                Permite consumir cualquier alimento pero requiere mayor tiempo de espera
              </p>
            </div>
          </div>
        </div>
      </RadioGroup>
      
      {value === T4Timing.sin_fibra_30min && (
        <Alert className="bg-yellow-50 border-yellow-200">
          <AlertDescription className="text-sm">
            <strong>Evitar en el desayuno:</strong> avena, cereales integrales, pan integral, 
            frutas con cáscara, salvado, semillas
          </AlertDescription>
        </Alert>
      )}
      
      {value === T4Timing.con_fibra_2h && (
        <Alert className="bg-blue-50 border-blue-200">
          <AlertDescription className="text-sm">
            <strong>Recomendación:</strong> Tomar la levotiroxina al despertar y desayunar 
            2 horas después sin restricciones
          </AlertDescription>
        </Alert>
      )}
    </div>
  )
}