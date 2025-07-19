import openai
from openai import AsyncOpenAI
from typing import Optional
import asyncio
from ..config import settings

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4-turbo-preview"
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