import axios from 'axios'
import { NewPatientData, ControlPatientData, MealReplacementData, MealPlanResponse } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface UploadResponse {
  success: boolean
  data: ControlPatientData
  message: string
  method_used?: string
}

export interface ExtractTextResponse {
  success: boolean
  text: string
  length: number
}

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

  uploadControlFile: async (file: File, method: 'ocr' | 'vision' | 'auto' = 'auto'): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post(`/meal-plans/control/upload?method=${method}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  extractTextFromFile: async (file: File): Promise<ExtractTextResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/meal-plans/control/extract-text', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  downloadControlTemplate: () => {
    window.open(`/api/meal-plans/control/template`, '_blank')
  },
}

export default api