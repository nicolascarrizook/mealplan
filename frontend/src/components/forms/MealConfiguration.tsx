import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { Info } from 'lucide-react'
import { Alert, AlertDescription } from '@/components/ui/alert'
import type { MealConfiguration as MealConfigType } from '@/types'

interface MealConfigurationProps {
  value: MealConfigType
  onChange: (config: MealConfigType) => void
}

export function MealConfiguration({ value, onChange }: MealConfigurationProps) {
  const [config, setConfig] = useState<MealConfigType>(value || {
    desayuno: true,
    almuerzo: true,
    merienda: true,
    cena: true,
    brunch: false,
    media_manana: false,
    media_tarde: false,
    postre_almuerzo: false,
    postre_cena: false,
    dulce_siesta: false,
    pre_entreno: false,
    post_entreno: false,
    alternativas_dulces: false,
    alternativas_saladas: false,
  })

  useEffect(() => {
    onChange(config)
  }, [config])

  const handleMainMealChange = (meal: keyof MealConfigType, checked: boolean) => {
    const newConfig = { ...config, [meal]: checked }
    
    // Si se selecciona brunch, desactivar desayuno y almuerzo
    if (meal === 'brunch' && checked) {
      newConfig.desayuno = false
      newConfig.almuerzo = false
    }
    
    // Si se selecciona desayuno o almuerzo, desactivar brunch
    if ((meal === 'desayuno' || meal === 'almuerzo') && checked) {
      newConfig.brunch = false
    }
    
    setConfig(newConfig)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Configuración de Comidas</CardTitle>
        <CardDescription>
          Personaliza las comidas del día según las necesidades del paciente
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Comidas principales */}
        <div>
          <h4 className="text-sm font-medium mb-3">Comidas Principales</h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="desayuno"
                checked={config.desayuno}
                onCheckedChange={(checked: boolean) => handleMainMealChange('desayuno', checked)}
                disabled={config.brunch}
              />
              <Label htmlFor="desayuno" className="cursor-pointer">
                Desayuno
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="almuerzo"
                checked={config.almuerzo}
                onCheckedChange={(checked: boolean) => handleMainMealChange('almuerzo', checked)}
                disabled={config.brunch}
              />
              <Label htmlFor="almuerzo" className="cursor-pointer">
                Almuerzo
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="merienda"
                checked={config.merienda}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, merienda: checked })}
              />
              <Label htmlFor="merienda" className="cursor-pointer">
                Merienda
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="cena"
                checked={config.cena}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, cena: checked })}
              />
              <Label htmlFor="cena" className="cursor-pointer">
                Cena
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="brunch"
                checked={config.brunch}
                onCheckedChange={(checked: boolean) => handleMainMealChange('brunch', checked)}
              />
              <Label htmlFor="brunch" className="cursor-pointer">
                Brunch
              </Label>
            </div>
          </div>
          
          {config.brunch && (
            <Alert className="mt-3">
              <Info className="h-4 w-4" />
              <AlertDescription>
                El brunch reemplaza al desayuno y almuerzo combinándolos en una sola comida
              </AlertDescription>
            </Alert>
          )}
        </div>

        <Separator />

        {/* Comidas adicionales */}
        <div>
          <h4 className="text-sm font-medium mb-3">Comidas Adicionales</h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="media_manana"
                checked={config.media_manana}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, media_manana: checked })}
              />
              <Label htmlFor="media_manana" className="cursor-pointer">
                Media mañana
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="media_tarde"
                checked={config.media_tarde}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, media_tarde: checked })}
              />
              <Label htmlFor="media_tarde" className="cursor-pointer">
                Media tarde
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="postre_almuerzo"
                checked={config.postre_almuerzo}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, postre_almuerzo: checked })}
                disabled={!config.almuerzo && !config.brunch}
              />
              <Label htmlFor="postre_almuerzo" className="cursor-pointer">
                Postre almuerzo
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="postre_cena"
                checked={config.postre_cena}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, postre_cena: checked })}
                disabled={!config.cena}
              />
              <Label htmlFor="postre_cena" className="cursor-pointer">
                Postre cena
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="dulce_siesta"
                checked={config.dulce_siesta}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, dulce_siesta: checked })}
              />
              <Label htmlFor="dulce_siesta" className="cursor-pointer">
                Dulce a la siesta
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="pre_entreno"
                checked={config.pre_entreno}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, pre_entreno: checked })}
              />
              <Label htmlFor="pre_entreno" className="cursor-pointer">
                Pre-entreno
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="post_entreno"
                checked={config.post_entreno}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, post_entreno: checked })}
              />
              <Label htmlFor="post_entreno" className="cursor-pointer">
                Post-entreno
              </Label>
            </div>
          </div>
        </div>

        <Separator />

        {/* Alternativas */}
        <div>
          <h4 className="text-sm font-medium mb-3">Alternativas por Comida</h4>
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="alternativas_dulces"
                checked={config.alternativas_dulces}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, alternativas_dulces: checked })}
              />
              <Label htmlFor="alternativas_dulces" className="cursor-pointer">
                Alternativas dulces
              </Label>
            </div>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="alternativas_saladas"
                checked={config.alternativas_saladas}
                onCheckedChange={(checked: boolean) => setConfig({ ...config, alternativas_saladas: checked })}
              />
              <Label htmlFor="alternativas_saladas" className="cursor-pointer">
                Alternativas saladas
              </Label>
            </div>
          </div>
          
          <p className="text-xs text-muted-foreground mt-2">
            Se generarán opciones dulces y/o saladas para cada comida según lo seleccionado
          </p>
        </div>

        {/* Resumen */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="text-sm font-medium mb-2">Resumen de comidas seleccionadas:</h4>
          <div className="text-xs space-y-1">
            <p>
              <span className="font-medium">Principales:</span>{' '}
              {[
                config.brunch ? 'Brunch' : null,
                config.desayuno && !config.brunch ? 'Desayuno' : null,
                config.almuerzo && !config.brunch ? 'Almuerzo' : null,
                config.merienda ? 'Merienda' : null,
                config.cena ? 'Cena' : null,
              ].filter(Boolean).join(', ') || 'Ninguna'}
            </p>
            <p>
              <span className="font-medium">Adicionales:</span>{' '}
              {[
                config.media_manana ? 'Media mañana' : null,
                config.media_tarde ? 'Media tarde' : null,
                config.postre_almuerzo ? 'Postre almuerzo' : null,
                config.postre_cena ? 'Postre cena' : null,
                config.dulce_siesta ? 'Dulce siesta' : null,
                config.pre_entreno ? 'Pre-entreno' : null,
                config.post_entreno ? 'Post-entreno' : null,
              ].filter(Boolean).join(', ') || 'Ninguna'}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}