import pdfplumber
import re
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class PDFExtractor:
    """Extract text and data from PDF files"""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract all text from a PDF file"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise ValueError(f"No se pudo leer el archivo PDF: {str(e)}")
    
    def extract_meal_plan_data(self, pdf_text: str) -> Dict:
        """Extract structured data from meal plan PDF text"""
        data = {
            "nombre": None,
            "peso_anterior": None,
            "plan_anterior": "",
            "fecha": None,
            "calorias_totales": None,
            "macros": {},
            "comidas": {}
        }
        
        # Extract patient name
        nombre_match = re.search(r"(?:Paciente|Nombre):\s*([^\n]+)", pdf_text, re.IGNORECASE)
        if nombre_match:
            data["nombre"] = nombre_match.group(1).strip()
        
        # Extract weight
        peso_match = re.search(r"Peso(?:\s+actual)?:\s*([\d,\.]+)\s*kg", pdf_text, re.IGNORECASE)
        if peso_match:
            data["peso_anterior"] = float(peso_match.group(1).replace(",", "."))
        
        # Extract date
        fecha_match = re.search(r"Fecha:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", pdf_text, re.IGNORECASE)
        if fecha_match:
            data["fecha"] = fecha_match.group(1)
        
        # Extract total calories
        calorias_match = re.search(r"(?:Calorías totales|Total diario):\s*([\d,\.]+)\s*(?:kcal)?", pdf_text, re.IGNORECASE)
        if calorias_match:
            data["calorias_totales"] = float(calorias_match.group(1).replace(",", "."))
        
        # Extract macros
        proteinas_match = re.search(r"Proteínas:\s*([\d,\.]+)\s*g", pdf_text, re.IGNORECASE)
        if proteinas_match:
            data["macros"]["proteinas"] = float(proteinas_match.group(1).replace(",", "."))
        
        carbos_match = re.search(r"(?:Carbohidratos|Hidratos):\s*([\d,\.]+)\s*g", pdf_text, re.IGNORECASE)
        if carbos_match:
            data["macros"]["carbohidratos"] = float(carbos_match.group(1).replace(",", "."))
        
        grasas_match = re.search(r"Grasas:\s*([\d,\.]+)\s*g", pdf_text, re.IGNORECASE)
        if grasas_match:
            data["macros"]["grasas"] = float(grasas_match.group(1).replace(",", "."))
        
        # Extract meals
        meal_patterns = [
            (r"DESAYUNO[:\s]*([^(ALMUERZO|MERIENDA|CENA|COLACI[ÓO]N)]+)", "desayuno"),
            (r"ALMUERZO[:\s]*([^(DESAYUNO|MERIENDA|CENA|COLACI[ÓO]N)]+)", "almuerzo"),
            (r"MERIENDA[:\s]*([^(DESAYUNO|ALMUERZO|CENA|COLACI[ÓO]N)]+)", "merienda"),
            (r"CENA[:\s]*([^(DESAYUNO|ALMUERZO|MERIENDA|COLACI[ÓO]N)]+)", "cena"),
        ]
        
        for pattern, meal_name in meal_patterns:
            meal_match = re.search(pattern, pdf_text, re.IGNORECASE | re.DOTALL)
            if meal_match:
                data["comidas"][meal_name] = meal_match.group(1).strip()
        
        # Store full plan text
        data["plan_anterior"] = pdf_text
        
        return data
    
    def extract_control_data(self, pdf_text: str) -> Dict:
        """Extract control-specific data from PDF"""
        data = self.extract_meal_plan_data(pdf_text)
        
        # Try to extract evolution data if present
        evolucion_match = re.search(r"Evolución[:\s]*([^\n]+)", pdf_text, re.IGNORECASE)
        if evolucion_match:
            data["evolucion"] = evolucion_match.group(1).strip()
        
        # Try to extract activity
        actividad_match = re.search(r"Actividad\s*(?:física)?[:\s]*([^\n]+)", pdf_text, re.IGNORECASE)
        if actividad_match:
            data["actividad"] = actividad_match.group(1).strip()
        
        return data