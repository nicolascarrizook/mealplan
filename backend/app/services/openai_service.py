import openai
from openai import AsyncOpenAI
from typing import Optional, Dict, List
import asyncio
import base64
import json
from ..config import settings

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4-turbo-preview"
        self.vision_model = "gpt-4-vision-preview"
        self.max_retries = 3
        
    async def generate_meal_plan(self, prompt: str) -> str:
        """Generate meal plan using OpenAI GPT-4"""
        
        for attempt in range(self.max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": """Sos un nutricionista experto en el método "Tres Días y Carga". 
                            Generás planes alimentarios personalizados siguiendo estrictamente las reglas del método.
                            Usás únicamente las recetas proporcionadas y adaptás las cantidades según los objetivos.
                            Todas las cantidades deben estar en gramos y el plan debe ser de 3 días iguales."""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=3000
                )
                
                return response.choices[0].message.content
                
            except openai.RateLimitError:
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    await asyncio.sleep(wait_time)
                else:
                    raise Exception("OpenAI rate limit exceeded. Please try again later.")
                    
            except openai.APIError as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1)
                else:
                    raise Exception(f"OpenAI API error: {str(e)}")
                    
            except Exception as e:
                raise Exception(f"Error generating meal plan: {str(e)}")
        
        raise Exception("Failed to generate meal plan after multiple attempts")
    
    async def analyze_meal_plan_image(self, image_bytes: bytes) -> Dict:
        """Analyze meal plan image using GPT-4 Vision"""
        
        # Encode image to base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = """Analiza esta imagen de un plan nutricional y extrae la siguiente información en formato JSON:
        {
            "nombre": "nombre del paciente",
            "fecha": "fecha del plan si está visible",
            "peso_anterior": "peso en kg (número)",
            "calorias_totales": "calorías diarias totales (número)",
            "macros": {
                "proteinas": "gramos de proteína (número)",
                "carbohidratos": "gramos de carbohidratos (número)",
                "grasas": "gramos de grasas (número)"
            },
            "comidas": {
                "desayuno": "descripción completa del desayuno con cantidades",
                "almuerzo": "descripción completa del almuerzo con cantidades",
                "merienda": "descripción completa de la merienda con cantidades",
                "cena": "descripción completa de la cena con cantidades"
            },
            "actividad_fisica": "descripción de la actividad física si está mencionada",
            "observaciones": "cualquier otra información relevante"
        }
        
        Si algún campo no está visible o no se puede determinar, usa null.
        Asegúrate de extraer las cantidades en gramos cuando estén disponibles.
        """
        
        for attempt in range(self.max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.vision_model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                        "detail": "high"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.3,
                    max_tokens=2000,
                    response_format={ "type": "json_object" }
                )
                
                # Parse JSON response
                result = response.choices[0].message.content
                return json.loads(result)
                
            except openai.RateLimitError:
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 2
                    await asyncio.sleep(wait_time)
                else:
                    raise Exception("OpenAI rate limit exceeded. Please try again later.")
                    
            except json.JSONDecodeError as e:
                raise Exception(f"Error parsing GPT-4 Vision response: {str(e)}")
                    
            except Exception as e:
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(1)
                else:
                    raise Exception(f"Error analyzing image: {str(e)}")
        
        raise Exception("Failed to analyze image after multiple attempts")