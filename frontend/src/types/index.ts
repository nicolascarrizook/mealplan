// Enums
export enum Sexo {
  masculino = "masculino",
  femenino = "femenino"
}

export enum Objetivo {
  mantener = "mantener",
  bajar_025 = "bajar_025",
  bajar_05 = "bajar_05",
  bajar_075 = "bajar_075",
  bajar_1 = "bajar_1",
  subir_025 = "subir_025",
  subir_05 = "subir_05",
  subir_075 = "subir_075",
  subir_1 = "subir_1"
}

export enum NivelEconomico {
  sin_restricciones = "Sin restricciones",
  medio = "Medio",
  limitado = "Limitado",
  bajo_recursos = "Bajo recursos"
}

export enum TipoPeso {
  crudo = "crudo",
  cocido = "cocido",
  ambas = "ambas"
}

export enum TipoColacion {
  no = "No",
  por_saciedad = "Por saciedad",
  pre_entreno = "Pre-entreno",
  post_entreno = "Post-entreno"
}

export enum ProteinLevel {
  muy_baja = "muy_baja",
  conservada = "conservada",
  moderada = "moderada",
  alta = "alta",
  muy_alta = "muy_alta",
  extrema = "extrema"
}

export enum DistributionType {
  traditional = "traditional",
  equitable = "equitable",
  custom = "custom"
}

export enum RecipeComplexity {
  simple = "simple",
  elaborada = "elaborada",
  mixta = "mixta"
}

export interface MealMacroDistribution {
  calories: number
  calories_percentage: number
  protein_g: number
  protein_percentage: number
  carbs_g: number
  carbs_percentage: number
  fats_g: number
  fats_percentage: number
}

export interface CustomMealDistribution {
  desayuno?: MealMacroDistribution
  almuerzo?: MealMacroDistribution
  merienda?: MealMacroDistribution
  cena?: MealMacroDistribution
}

export interface MealConfiguration {
  // Comidas principales
  desayuno: boolean
  almuerzo: boolean
  merienda: boolean
  cena: boolean
  brunch: boolean
  drunch: boolean  // Combinación de merienda y cena
  
  // Comidas adicionales
  media_manana: boolean
  media_tarde: boolean
  postre_almuerzo: boolean
  postre_cena: boolean
  dulce_siesta: boolean
  pre_entreno: boolean
  post_entreno: boolean
  
  // Alternativas
  alternativas_dulces: boolean
  alternativas_saladas: boolean
}

export interface NewPatientData {
  nombre: string
  edad: number
  fecha_nacimiento?: string  // ISO date string
  sexo: Sexo
  estatura: number
  peso: number
  objetivo: Objetivo
  tipo_actividad: string
  frecuencia_semanal: number
  duracion_sesion: number
  suplementacion?: string
  patologias?: string
  no_consume?: string
  le_gusta?: string
  antecedentes_personales?: string
  antecedentes_familiares?: string
  medicacion_detallada?: string
  nivel_economico: NivelEconomico
  notas_personales?: string
  comidas_principales: number
  tipo_peso: TipoPeso
  recipe_complexity: RecipeComplexity
  // Características específicas del menú
  caracteristicas_menu?: string
  almuerzo_transportable?: boolean
  timing_desayuno?: string
  // Nuevos campos de personalización de macros
  carbs_percentage?: number
  protein_level?: ProteinLevel
  fat_percentage?: number
  distribution_type: DistributionType
  custom_meal_distribution?: CustomMealDistribution
  meal_configuration?: MealConfiguration
  // Actividades, suplementos y medicamentos
  activities?: Array<{
    id: string
    name: string
    duration: number
    frequency: number
    calories: number
    isManual?: boolean
  }>
  supplements?: Array<{
    id: string
    name: string
    servings: number
    calories: number
    protein: number
    carbs: number
    fats: number
    serving_size: string
  }>
  medications?: Array<{
    id: string
    name: string
    impact: string
    considerations: string
  }>
}

export interface ControlPatientData {
  nombre: string
  fecha_control: string
  peso_anterior: number
  peso_actual: number
  objetivo_actualizado: string
  tipo_actividad_actual: string
  frecuencia_actual: number
  duracion_actual: number
  agregar: string
  sacar: string
  dejar: string
  plan_anterior: string
  tipo_peso: TipoPeso
}

export interface MealReplacementData {
  paciente: string
  comida_reemplazar: string
  nueva_comida: string
  condiciones?: string
  comida_actual: string
  proteinas: number
  carbohidratos: number
  grasas: number
  calorias: number
  tipo_peso: TipoPeso
}

export interface MealPlanResponse {
  meal_plan: string
  pdf_path: string
}