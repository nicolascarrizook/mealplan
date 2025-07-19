export interface NewPatientData {
  nombre: string
  edad: number
  sexo: string
  estatura: number
  peso: number
  objetivo: string
  objetivo_semanal?: string
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
  nivel_economico: string
  notas_personales?: string
  comidas_principales: number
  colaciones: string
  tipo_peso: string
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
  tipo_peso: string
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
  tipo_peso: string
}

export interface MealPlanResponse {
  meal_plan: string
  pdf_path: string
}