# Cambios para Desplegar - 20 de Enero 2025

## Archivos Modificados

### Backend
1. **`/backend/app/services/prompt_generator.py`**
   - Modificado para solicitar 3 opciones de recetas por comida
   - Actualizado formato de salida con macros individuales
   - Instrucciones para mantener macros similares entre opciones (±10%)

### Frontend

2. **`/frontend/src/components/forms/SupplementSelector.tsx`**
   - Añadido cálculo automático de dosis basado en peso corporal
   - Creatina: 0.1g × kg
   - Proteína: 1 scoop (20-25g)
   - Magnesio: 350-400mg
   - Omega-3: 1000-2000mg EPA/DHA
   - Visual con ícono de calculadora

3. **`/frontend/src/components/forms/NewPatientForm.tsx`**
   - Actualizado para usar MealPlanDisplayV2
   - Pasa peso corporal a SupplementSelector

4. **`/frontend/src/components/MealPlanDisplayV2.tsx`** (NUEVO)
   - Componente para mostrar 3 opciones por comida
   - Tabs interactivos para seleccionar opciones
   - Cálculo dinámico de macros totales
   - Mejor visualización con íconos

5. **`/frontend/src/components/ui/checkbox.tsx`** (NUEVO)
   - Componente checkbox para MealConfiguration

6. **`/frontend/src/components/forms/MealConfiguration.tsx`**
   - Corregidos tipos TypeScript

7. **`/frontend/src/components/forms/MedicationSelector.tsx`**
   - Eliminado import no usado

8. **`/frontend/src/utils/interactions.ts`**
   - Corregido problema de spread operator

## Comandos de Despliegue

```bash
# En el droplet
cd /path/to/app

# Detener contenedores
docker compose down

# Actualizar código
git pull origin main  # o copiar archivos manualmente

# Reconstruir y levantar
docker compose up -d --build

# Ver logs
docker compose logs -f
```

## Funcionalidades Nuevas para Probar

1. **Suplementos con Cálculo Automático**
   - Al seleccionar creatina, proteína, magnesio u omega-3
   - Debe mostrar dosis calculada automáticamente
   - Ícono de calculadora indica cálculo automático

2. **3 Opciones de Recetas por Comida**
   - Cada comida muestra 3 tabs con opciones
   - Cada opción tiene sus propios macros
   - Los macros totales se actualizan al cambiar opciones
   - Vista completa del plan al final

3. **Todas las características anteriores funcionando**
   - Complejidad de recetas
   - Opción "ambas" para peso
   - Configuración flexible de comidas
   - Timing de T4