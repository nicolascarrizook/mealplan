from typing import Dict, Optional, Union
import os
from datetime import datetime
import logging

from .pdf_extractor import PDFExtractor
from .excel_extractor import ExcelExtractor
from .image_extractor import ImageExtractor

logger = logging.getLogger(__name__)

class FileParser:
    """Main parser to handle different file types and extract control data"""
    
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.excel_extractor = ExcelExtractor()
        self.image_extractor = ImageExtractor()
    
    def parse_file(self, file_path: str, file_type: str) -> Dict:
        """Parse file based on its type and return structured data"""
        
        file_type = file_type.lower()
        
        try:
            if file_type == 'pdf' or file_path.lower().endswith('.pdf'):
                return self._parse_pdf(file_path)
            
            elif file_type in ['excel', 'xlsx', 'xls'] or file_path.lower().endswith(('.xlsx', '.xls')):
                return self._parse_excel(file_path)
            
            elif file_type == 'csv' or file_path.lower().endswith('.csv'):
                return self._parse_csv(file_path)
            
            elif file_type in ['image', 'jpg', 'jpeg', 'png'] or file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                return self._parse_image(file_path)
            
            else:
                raise ValueError(f"Tipo de archivo no soportado: {file_type}")
                
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {e}")
            raise
    
    def parse_file_bytes(self, file_bytes: bytes, file_type: str, filename: str) -> Dict:
        """Parse file from bytes"""
        
        # Save temporarily to process
        temp_path = f"/tmp/{filename}"
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(file_bytes)
            
            return self.parse_file(temp_path, file_type)
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _parse_pdf(self, file_path: str) -> Dict:
        """Parse PDF file and structure the data for control form"""
        
        # Extract text from PDF
        pdf_text = self.pdf_extractor.extract_text_from_pdf(file_path)
        
        # Extract structured data
        pdf_data = self.pdf_extractor.extract_control_data(pdf_text)
        
        # Convert to control form format
        control_data = self._convert_to_control_format(pdf_data)
        
        return control_data
    
    def _parse_excel(self, file_path: str) -> Dict:
        """Parse Excel file and return first patient data"""
        
        # Extract all rows
        excel_data = self.excel_extractor.extract_from_excel(file_path)
        
        if not excel_data:
            raise ValueError("No se encontraron datos válidos en el archivo Excel")
        
        # Return first patient (can be extended to handle multiple)
        patient_data = excel_data[0]
        
        # Convert to control form format
        control_data = self._convert_excel_to_control_format(patient_data)
        
        return control_data
    
    def _parse_csv(self, file_path: str) -> Dict:
        """Parse CSV file and return first patient data"""
        
        # Extract all rows
        csv_data = self.excel_extractor.extract_from_csv(file_path)
        
        if not csv_data:
            raise ValueError("No se encontraron datos válidos en el archivo CSV")
        
        # Return first patient
        patient_data = csv_data[0]
        
        # Convert to control form format
        control_data = self._convert_excel_to_control_format(patient_data)
        
        return control_data
    
    def _parse_image(self, file_path: str) -> Dict:
        """Parse image file using OCR"""
        
        # Extract text using OCR
        ocr_text = self.image_extractor.extract_text_from_image(file_path)
        
        # Extract structured data
        image_data = self.image_extractor.extract_meal_plan_data(ocr_text)
        
        # Convert to control form format
        control_data = self._convert_to_control_format(image_data)
        
        return control_data
    
    def _convert_to_control_format(self, data: Dict) -> Dict:
        """Convert extracted data to control form format"""
        
        # Get today's date if not provided
        fecha_control = data.get('fecha', datetime.now().strftime('%Y-%m-%d'))
        
        control_data = {
            'nombre': data.get('nombre', ''),
            'fecha_control': fecha_control,
            'peso_anterior': data.get('peso_anterior', 0),
            'peso_actual': 0,  # User needs to fill this
            'objetivo_actualizado': '',  # User needs to fill this
            'tipo_actividad_actual': data.get('actividad', ''),
            'frecuencia_actual': 0,  # User needs to fill this
            'duracion_actual': 0,  # User needs to fill this
            'agregar': '',  # User needs to fill this
            'sacar': '',  # User needs to fill this
            'dejar': '',  # User needs to fill this
            'plan_anterior': data.get('plan_anterior', ''),
            'tipo_peso': 'crudo',
            
            # Additional extracted data
            'extracted_data': {
                'calorias_totales': data.get('calorias_totales'),
                'macros': data.get('macros', {}),
                'comidas': data.get('comidas', {}),
                'evolucion': data.get('evolucion', '')
            }
        }
        
        return control_data
    
    def _convert_excel_to_control_format(self, data: Dict) -> Dict:
        """Convert Excel/CSV data to control form format"""
        
        control_data = {
            'nombre': data.get('nombre', ''),
            'fecha_control': data.get('fecha_control', datetime.now().strftime('%Y-%m-%d')),
            'peso_anterior': data.get('peso_anterior', 0),
            'peso_actual': data.get('peso_actual', 0),
            'objetivo_actualizado': data.get('objetivo', ''),
            'tipo_actividad_actual': data.get('actividad', ''),
            'frecuencia_actual': data.get('frecuencia', 0),
            'duracion_actual': data.get('duracion', 0),
            'agregar': data.get('agregar', ''),
            'sacar': data.get('sacar', ''),
            'dejar': data.get('dejar', ''),
            'plan_anterior': data.get('plan_anterior', ''),
            'tipo_peso': 'crudo',
            
            # Additional data
            'notas': data.get('notas', '')
        }
        
        return control_data
    
    def generate_excel_template(self, output_path: str):
        """Generate Excel template for users"""
        self.excel_extractor.save_template(output_path)