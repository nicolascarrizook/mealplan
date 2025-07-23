import pytesseract
from PIL import Image
import re
from typing import Dict, Optional
import logging
import io
import asyncio

logger = logging.getLogger(__name__)

class ImageExtractor:
    """Extract text from images using OCR or AI Vision"""
    
    def __init__(self, openai_service=None):
        # Configure pytesseract if needed
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust path if needed
        self.openai_service = openai_service
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            # Open image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text using OCR (Spanish language)
            text = pytesseract.image_to_string(image, lang='spa')
            
            return text
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            raise ValueError(f"No se pudo procesar la imagen: {str(e)}")
    
    def extract_text_from_bytes(self, image_bytes: bytes) -> str:
        """Extract text from image bytes"""
        try:
            # Open image from bytes
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text using OCR (Spanish language)
            text = pytesseract.image_to_string(image, lang='spa')
            
            return text
        except Exception as e:
            logger.error(f"Error extracting text from image bytes: {e}")
            raise ValueError(f"No se pudo procesar la imagen: {str(e)}")
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image to improve OCR accuracy"""
        try:
            # Convert to grayscale
            image = image.convert('L')
            
            # Increase contrast
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Resize if too small
            width, height = image.size
            if width < 1000:
                ratio = 1000 / width
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            return image
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return image
    
    def extract_meal_plan_data(self, ocr_text: str) -> Dict:
        """Extract structured data from OCR text"""
        data = {
            "nombre": None,
            "peso_anterior": None,
            "plan_anterior": ocr_text,
            "fecha": None,
            "calorias_totales": None,
            "macros": {},
            "comidas": {}
        }
        
        # Clean OCR text
        ocr_text = self._clean_ocr_text(ocr_text)
        
        # Extract patient name
        nombre_patterns = [
            r"(?:Paciente|Nombre|Cliente)[\s:]+([^\n]+)",
            r"Plan\s+(?:para|de)[\s:]+([^\n]+)",
        ]
        
        for pattern in nombre_patterns:
            match = re.search(pattern, ocr_text, re.IGNORECASE)
            if match:
                data["nombre"] = match.group(1).strip()
                break
        
        # Extract weight
        peso_patterns = [
            r"Peso[\s:]+(\d+[,.]?\d*)\s*kg",
            r"(\d+[,.]?\d*)\s*kg",
        ]
        
        for pattern in peso_patterns:
            match = re.search(pattern, ocr_text, re.IGNORECASE)
            if match:
                try:
                    data["peso_anterior"] = float(match.group(1).replace(",", "."))
                    break
                except:
                    pass
        
        # Extract date
        fecha_patterns = [
            r"Fecha[\s:]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
            r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        ]
        
        for pattern in fecha_patterns:
            match = re.search(pattern, ocr_text, re.IGNORECASE)
            if match:
                data["fecha"] = match.group(1)
                break
        
        # Extract calories
        calorias_patterns = [
            r"(?:Calor[ií]as|Kcal)[\s:]+(\d+)",
            r"Total[\s:]+(\d+)\s*kcal",
        ]
        
        for pattern in calorias_patterns:
            match = re.search(pattern, ocr_text, re.IGNORECASE)
            if match:
                try:
                    data["calorias_totales"] = int(match.group(1))
                    break
                except:
                    pass
        
        # Extract macros
        macro_patterns = {
            "proteinas": [r"Prote[ií]nas?[\s:]+(\d+)\s*g", r"P[\s:]+(\d+)\s*g"],
            "carbohidratos": [r"(?:Carbohidratos?|HC|Hidratos?)[\s:]+(\d+)\s*g", r"C[\s:]+(\d+)\s*g"],
            "grasas": [r"Grasas?[\s:]+(\d+)\s*g", r"G[\s:]+(\d+)\s*g"]
        }
        
        for macro, patterns in macro_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, ocr_text, re.IGNORECASE)
                if match:
                    try:
                        data["macros"][macro] = int(match.group(1))
                        break
                    except:
                        pass
        
        # Extract meals (simplified for OCR)
        meal_keywords = {
            "desayuno": ["DESAYUNO", "Desayuno", "BREAKFAST"],
            "almuerzo": ["ALMUERZO", "Almuerzo", "LUNCH", "COMIDA"],
            "merienda": ["MERIENDA", "Merienda", "SNACK"],
            "cena": ["CENA", "Cena", "DINNER"]
        }
        
        lines = ocr_text.split('\n')
        current_meal = None
        
        for line in lines:
            line = line.strip()
            
            # Check if line is a meal header
            is_meal_header = False
            for meal, keywords in meal_keywords.items():
                if any(keyword in line for keyword in keywords):
                    current_meal = meal
                    data["comidas"][meal] = ""
                    is_meal_header = True
                    break
            
            # Add content to current meal if it's not a meal header
            if not is_meal_header and current_meal and line:
                data["comidas"][current_meal] += line + " "
        
        # Clean up meal descriptions
        for meal in data["comidas"]:
            data["comidas"][meal] = data["comidas"][meal].strip()
        
        return data
    
    def _clean_ocr_text(self, text: str) -> str:
        """Clean OCR text to improve parsing"""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR errors
        replacements = {
            '0': 'O',  # Sometimes O is read as 0
            '1': 'I',  # Sometimes I is read as 1
            '|': 'I',  # Vertical bar often confused with I
            '—': '-',  # Em dash to regular dash
        }
        
        # Apply replacements where it makes sense
        # This is a simplified approach - in production you'd want more sophisticated error correction
        
        return text
    
    async def extract_with_vision(self, image_bytes: bytes) -> Dict:
        """Extract meal plan data using GPT-4 Vision"""
        if not self.openai_service:
            raise ValueError("OpenAI service not configured for Vision extraction")
        
        try:
            # Use GPT-4 Vision to analyze the image
            vision_data = await self.openai_service.analyze_meal_plan_image(image_bytes)
            
            # Convert Vision response to our standard format
            return self._convert_vision_to_standard_format(vision_data)
            
        except Exception as e:
            logger.error(f"Error using GPT-4 Vision: {e}")
            raise ValueError(f"No se pudo analizar la imagen con Vision AI: {str(e)}")
    
    def extract_with_vision_sync(self, image_bytes: bytes) -> Dict:
        """Synchronous wrapper for Vision extraction"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.extract_with_vision(image_bytes))
        finally:
            loop.close()
    
    def _convert_vision_to_standard_format(self, vision_data: Dict) -> Dict:
        """Convert GPT-4 Vision response to standard format"""
        data = {
            "nombre": vision_data.get("nombre"),
            "peso_anterior": None,
            "plan_anterior": "",
            "fecha": vision_data.get("fecha"),
            "calorias_totales": vision_data.get("calorias_totales"),
            "macros": vision_data.get("macros", {}),
            "comidas": vision_data.get("comidas", {}),
            "actividad": vision_data.get("actividad_fisica"),
            "observaciones": vision_data.get("observaciones")
        }
        
        # Try to extract weight from observations or other fields
        if vision_data.get("peso_anterior"):
            try:
                data["peso_anterior"] = float(str(vision_data["peso_anterior"]).replace(",", "."))
            except:
                pass
        
        # Build plan_anterior from all available data
        plan_parts = []
        
        if data["nombre"]:
            plan_parts.append(f"Paciente: {data['nombre']}")
        
        if data["fecha"]:
            plan_parts.append(f"Fecha: {data['fecha']}")
        
        if data["calorias_totales"]:
            plan_parts.append(f"Calorías totales: {data['calorias_totales']} kcal")
        
        if data["macros"]:
            macros = data["macros"]
            if macros.get("proteinas"):
                plan_parts.append(f"Proteínas: {macros['proteinas']}g")
            if macros.get("carbohidratos"):
                plan_parts.append(f"Carbohidratos: {macros['carbohidratos']}g")
            if macros.get("grasas"):
                plan_parts.append(f"Grasas: {macros['grasas']}g")
        
        # Add meals
        for meal_type, meal_desc in data["comidas"].items():
            if meal_desc:
                plan_parts.append(f"\n{meal_type.upper()}:\n{meal_desc}")
        
        if data["actividad"]:
            plan_parts.append(f"\nActividad física: {data['actividad']}")
        
        if data["observaciones"]:
            plan_parts.append(f"\nObservaciones: {data['observaciones']}")
        
        data["plan_anterior"] = "\n".join(plan_parts)
        
        return data