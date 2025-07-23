import pytesseract
from PIL import Image
import re
from typing import Dict, Optional
import logging
import io

logger = logging.getLogger(__name__)

class ImageExtractor:
    """Extract text from images using OCR"""
    
    def __init__(self):
        # Configure pytesseract if needed
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust path if needed
        pass
    
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
            for meal, keywords in meal_keywords.items():
                if any(keyword in line for keyword in keywords):
                    current_meal = meal
                    data["comidas"][meal] = ""
                    break
            
            # Add content to current meal
            elif current_meal and line and not any(k in line for keywords in meal_keywords.values() for k in keywords):
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