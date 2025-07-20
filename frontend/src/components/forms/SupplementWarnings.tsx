import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { AlertTriangle, Info, CheckCircle } from 'lucide-react'
import { Badge } from '@/components/ui/badge'

interface Interaction {
  medication: string
  supplement: string
  interaction: {
    separation_hours?: number
    reason: string
    severity: string
    recommendation: string
  }
}

interface DoseWarning {
  supplement: string
  current_dose: string
  max_dose: string
  side_effect?: string
}

interface Synergy {
  supplement1: string
  supplement2: string
  benefit: string
  recommendation?: string
}

interface SupplementWarningsProps {
  interactions?: Interaction[]
  doseWarnings?: DoseWarning[]
  synergies?: Synergy[]
}

export function SupplementWarnings({ interactions = [], doseWarnings = [], synergies = [] }: SupplementWarningsProps) {
  if (interactions.length === 0 && doseWarnings.length === 0 && synergies.length === 0) {
    return null
  }

  return (
    <div className="space-y-4">
      {/* Interacciones medicamento-suplemento */}
      {interactions.length > 0 && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>⚠️ Advertencias de Interacciones</AlertTitle>
          <AlertDescription>
            <div className="space-y-3 mt-2">
              {interactions.map((warning, index) => (
                <div key={index} className="border-l-4 border-orange-500 pl-3 py-2">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="font-medium text-sm">
                        {warning.supplement} con {warning.medication}
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        {warning.interaction.reason}
                      </p>
                      <p className="text-xs font-medium text-orange-600 mt-1">
                        📌 {warning.interaction.recommendation}
                      </p>
                    </div>
                    <Badge variant={warning.interaction.severity === 'high' ? 'destructive' : 'secondary'} className="ml-2">
                      {warning.interaction.severity === 'high' ? 'Alta' : 'Moderada'}
                    </Badge>
                  </div>
                  {warning.interaction.separation_hours && (
                    <div className="mt-2 bg-orange-50 rounded p-2">
                      <p className="text-xs font-medium">
                        ⏰ Separar al menos {warning.interaction.separation_hours} horas
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Advertencias de dosis */}
      {doseWarnings.length > 0 && (
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>⚠️ Advertencias de Dosis</AlertTitle>
          <AlertDescription>
            <div className="space-y-2 mt-2">
              {doseWarnings.map((warning, index) => (
                <div key={index} className="border-l-4 border-yellow-500 pl-3 py-2">
                  <p className="font-medium text-sm">{warning.supplement}</p>
                  <p className="text-xs text-gray-600">
                    Dosis actual: {warning.current_dose} | Máximo recomendado: {warning.max_dose}
                  </p>
                  {warning.side_effect && (
                    <p className="text-xs text-yellow-600 mt-1">
                      ⚠️ Posible efecto: {warning.side_effect}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Sinergias beneficiosas */}
      {synergies.length > 0 && (
        <Alert className="border-green-200">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertTitle className="text-green-800">💡 Sinergias Beneficiosas</AlertTitle>
          <AlertDescription>
            <div className="space-y-2 mt-2">
              {synergies.map((synergy, index) => (
                <div key={index} className="border-l-4 border-green-500 pl-3 py-2">
                  <p className="text-sm text-gray-700">{synergy.benefit}</p>
                  {synergy.recommendation && (
                    <p className="text-xs text-green-600 mt-1">
                      💡 {synergy.recommendation}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Información general */}
      <Alert>
        <Info className="h-4 w-4" />
        <AlertTitle>Información Importante</AlertTitle>
        <AlertDescription>
          <ul className="list-disc list-inside text-xs space-y-1 mt-2">
            <li>Siempre consulte con su médico antes de cambiar su suplementación</li>
            <li>Las separaciones horarias son para optimizar la absorción</li>
            <li>Los suplementos con relevancia clínica requieren supervisión profesional</li>
          </ul>
        </AlertDescription>
      </Alert>
    </div>
  )
}