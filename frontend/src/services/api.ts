import axios from 'axios'
import { NewPatientData, ControlPatientData, MealReplacementData, MealPlanResponse } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const mealPlanService = {
  generateNewPatientPlan: async (data: NewPatientData): Promise<MealPlanResponse> => {
    const response = await api.post('/meal-plans/new-patient', data)
    return response.data
  },

  generateControlPlan: async (data: ControlPatientData): Promise<MealPlanResponse> => {
    const response = await api.post('/meal-plans/control', data)
    return response.data
  },

  replaceMeal: async (data: MealReplacementData): Promise<MealPlanResponse> => {
    const response = await api.post('/meal-plans/replace-meal', data)
    return response.data
  },

  downloadPdf: (filename: string) => {
    window.open(`/api/meal-plans/download/${filename}`, '_blank')
  },
}

export default api