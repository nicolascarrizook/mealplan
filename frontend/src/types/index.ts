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
  cocido = "cocido"
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
  equitable = "equitable"
}

export interface NewPatientData {
  nombre: string
  edad: number
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
  horarios: {
    desayuno: string
    almuerzo: string
    merienda: string
    cena: string
  }
  nivel_economico: NivelEconomico
  notas_personales?: string
  comidas_principales: number
  colaciones: TipoColacion
  tipo_peso: TipoPeso
  // Nuevos campos de personalización de macros
  carbs_percentage?: number
  protein_level?: ProteinLevel
  fat_percentage?: number
  distribution_type: DistributionType
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