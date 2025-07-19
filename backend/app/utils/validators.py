"""
Validadores y sanitizadores de entrada
"""

import re
from typing import Optional, List

class InputValidator:
    """Validador de entradas del usuario"""
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Sanitiza texto de entrada eliminando caracteres peligrosos
        """
        if not text:
            return ""
        
        # Eliminar espacios al inicio y final
        text = text.strip()
        
        # Eliminar múltiples espacios
        text = re.sub(r'\s+', ' ', text)
        
        # Eliminar caracteres potencialmente peligrosos
        text = re.sub(r'[<>{}\\]', '', text)
        
        # Eliminar tags HTML
        text = re.sub(r'<[^>]+>', '', text)
        
        return text
    
    @staticmethod
    def format_list_input(text: Optional[str]) -> List[str]:
        """
        Formatea entrada de lista (patologías, alergias, etc) para consistencia
        """
        if not text or text.lower() in ['no', 'ninguno', 'ninguna', 'n/a', '-', '']:
            return []
        
        # Sanitizar primero
        text = InputValidator.sanitize_text(text)
        
        # Separar por comas y limpiar cada elemento
        items = [item.strip() for item in text.split(',')]
        
        # Capitalizar primera letra de cada item
        items = [item.capitalize() if item else '' for item in items]
        
        # Filtrar elementos vacíos
        return [item for item in items if item]
    
    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, Optional[str]]:
        """
        Valida número de teléfono
        """
        # Eliminar espacios, guiones y paréntesis
        phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        if not phone:
            return False, "Por favor, ingresa un número de teléfono"
        
        # Aceptar varios formatos
        if re.match(r'^\+?549?\d{10,}$', phone):
            return True, None
        
        return False, "Número de teléfono inválido"
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, Optional[str]]:
        """
        Valida dirección de email
        """
        email = email.strip().lower()
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "Email inválido"
        
        return True, None
    
    @staticmethod
    def normalize_decimal(value: str) -> str:
        """
        Normaliza decimales aceptando tanto coma como punto
        """
        return value.replace(',', '.')
    
    @staticmethod
    def is_safe_filename(filename: str) -> bool:
        """
        Verifica si un nombre de archivo es seguro
        """
        # Solo permitir caracteres alfanuméricos, guiones y puntos
        return bool(re.match(r'^[a-zA-Z0-9\-_.]+$', filename))
    
    @staticmethod
    def clean_patient_name(name: str) -> str:
        """
        Limpia el nombre del paciente para uso en archivos
        """
        # Sanitizar primero
        name = InputValidator.sanitize_text(name)
        
        # Reemplazar espacios con guiones bajos
        name = name.replace(' ', '_')
        
        # Eliminar caracteres no alfanuméricos excepto guiones y guiones bajos
        name = re.sub(r'[^a-zA-Z0-9_\-]', '', name)
        
        # Limitar longitud
        return name[:50]