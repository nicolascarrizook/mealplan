import pandas as pd
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ExcelExtractor:
    """Extract data from Excel and CSV files"""
    
    def extract_from_excel(self, file_path: str) -> List[Dict]:
        """Extract data from Excel file"""
        try:
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=0)
            return self._process_dataframe(df)
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            raise ValueError(f"No se pudo leer el archivo Excel: {str(e)}")
    
    def extract_from_csv(self, file_path: str) -> List[Dict]:
        """Extract data from CSV file"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("No se pudo decodificar el archivo CSV")
            
            return self._process_dataframe(df)
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise ValueError(f"No se pudo leer el archivo CSV: {str(e)}")
    
    def _process_dataframe(self, df: pd.DataFrame) -> List[Dict]:
        """Process dataframe and extract control data"""
        results = []
        
        # Normalize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Expected columns mapping
        column_mapping = {
            'nombre': ['nombre', 'paciente', 'name', 'patient'],
            'fecha_control': ['fecha_control', 'fecha', 'date', 'fecha control'],
            'peso_anterior': ['peso_anterior', 'peso anterior', 'previous weight', 'peso_previo'],
            'peso_actual': ['peso_actual', 'peso actual', 'current weight', 'peso'],
            'objetivo': ['objetivo', 'goal', 'objetivo_actualizado'],
            'actividad': ['actividad', 'activity', 'tipo_actividad', 'ejercicio'],
            'frecuencia': ['frecuencia', 'frequency', 'frecuencia_semanal', 'veces_semana'],
            'duracion': ['duracion', 'duration', 'duracion_sesion', 'minutos'],
            'plan_anterior': ['plan_anterior', 'plan anterior', 'previous plan', 'plan'],
            'notas': ['notas', 'notes', 'observaciones', 'comments'],
            'agregar': ['agregar', 'add', 'incluir'],
            'sacar': ['sacar', 'remove', 'quitar', 'eliminar'],
            'dejar': ['dejar', 'keep', 'mantener']
        }
        
        # Process each row
        for idx, row in df.iterrows():
            data = {}
            
            # Extract data using column mapping
            for field, possible_columns in column_mapping.items():
                for col in possible_columns:
                    if col in df.columns and pd.notna(row[col]):
                        data[field] = row[col]
                        break
            
            # Convert data types
            if 'peso_anterior' in data:
                try:
                    data['peso_anterior'] = float(str(data['peso_anterior']).replace(',', '.'))
                except:
                    pass
            
            if 'peso_actual' in data:
                try:
                    data['peso_actual'] = float(str(data['peso_actual']).replace(',', '.'))
                except:
                    pass
            
            if 'frecuencia' in data:
                try:
                    data['frecuencia'] = int(data['frecuencia'])
                except:
                    pass
            
            if 'duracion' in data:
                try:
                    data['duracion'] = int(data['duracion'])
                except:
                    pass
            
            # Handle date formatting
            if 'fecha_control' in data:
                try:
                    if isinstance(data['fecha_control'], pd.Timestamp):
                        data['fecha_control'] = data['fecha_control'].strftime('%Y-%m-%d')
                    elif isinstance(data['fecha_control'], str):
                        # Try to parse and reformat
                        date_obj = pd.to_datetime(data['fecha_control'])
                        data['fecha_control'] = date_obj.strftime('%Y-%m-%d')
                except:
                    # Keep original if parsing fails
                    pass
            
            # Only add if we have minimum required data
            if data.get('nombre') and (data.get('peso_actual') or data.get('plan_anterior')):
                results.append(data)
        
        return results
    
    def create_template(self) -> pd.DataFrame:
        """Create a template DataFrame for users to fill"""
        template_data = {
            'Nombre': ['Juan Pérez (ejemplo)'],
            'Fecha Control': [datetime.now().strftime('%Y-%m-%d')],
            'Peso Anterior': [70.5],
            'Peso Actual': [69.8],
            'Objetivo': ['Continuar bajando 0.5kg por semana'],
            'Actividad': ['Gym + cardio'],
            'Frecuencia': [4],
            'Duracion': [60],
            'Plan Anterior': ['Pegar aquí el plan anterior completo...'],
            'Agregar': ['Alimentos o comidas a agregar'],
            'Sacar': ['Alimentos o comidas a eliminar'],
            'Dejar': ['Aspectos del plan a mantener'],
            'Notas': ['Observaciones adicionales']
        }
        
        return pd.DataFrame(template_data)
    
    def save_template(self, output_path: str):
        """Save template to Excel file"""
        template = self.create_template()
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            template.to_excel(writer, sheet_name='Control Pacientes', index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Control Pacientes']
            
            # Adjust column widths
            column_widths = {
                'A': 20,  # Nombre
                'B': 15,  # Fecha Control
                'C': 15,  # Peso Anterior
                'D': 15,  # Peso Actual
                'E': 30,  # Objetivo
                'F': 20,  # Actividad
                'G': 12,  # Frecuencia
                'H': 12,  # Duracion
                'I': 50,  # Plan Anterior
                'J': 30,  # Agregar
                'K': 30,  # Sacar
                'L': 30,  # Dejar
                'M': 30   # Notas
            }
            
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
            
            # Add instructions in a second sheet
            instructions = pd.DataFrame({
                'Instrucciones': [
                    'Este template está diseñado para facilitar el control de pacientes.',
                    '',
                    'Cómo usar:',
                    '1. Complete una fila por cada paciente a controlar',
                    '2. Los campos obligatorios son: Nombre y (Peso Actual o Plan Anterior)',
                    '3. En "Plan Anterior" pegue el plan nutricional completo del control anterior',
                    '4. Los pesos deben estar en kg (use punto o coma para decimales)',
                    '5. La frecuencia es en veces por semana (0-7)',
                    '6. La duración es en minutos',
                    '',
                    'Puede agregar más filas según necesite.',
                    'Guarde el archivo como Excel (.xlsx) o CSV para subirlo al sistema.'
                ]
            })
            
            instructions.to_excel(writer, sheet_name='Instrucciones', index=False)