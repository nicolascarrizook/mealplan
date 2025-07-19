from pydantic import BaseModel, Field
from typing import Dict, Optional, List

class NewPatientRequest(BaseModel):
    # Datos personales
    nombre: str
    edad: int
    sexo: str
    estatura: float = Field(..., description="Altura en cm")
    peso: float = Field(..., description="Peso en kg")
    
    # Objetivo
    objetivo: str = Field(..., description="bajar/subir/mantener peso")
    objetivo_semanal: Optional[str] = Field(None, description="0.5kg o 1kg por semana")
    
    # Actividad física
    tipo_actividad: str
    frecuencia_semanal: int
    duracion_sesion: int = Field(..., description="Duración en minutos")
    
    # Especificaciones médicas
    suplementacion: Optional[str] = None
    patologias: Optional[str] = None
    no_consume: Optional[str] = None
    le_gusta: Optional[str] = None
    
    # Horarios
    horarios: Dict[str, str] = Field(..., description="Horarios de cada comida")
    
    # Configuración del plan
    nivel_economico: str = "Medio"
    notas_personales: Optional[str] = None
    comidas_principales: int = 4
    colaciones: str = "No"
    tipo_peso: str = "crudo"
    
    @property
    def imc(self) -> float:
        return round(self.peso / (self.estatura/100)**2, 1)

class ControlPatientRequest(BaseModel):
    # Datos del control
    nombre: str
    fecha_control: str
    peso_anterior: float
    peso_actual: float
    objetivo_actualizado: str
    
    # Actividad actual
    tipo_actividad_actual: str
    frecuencia_actual: int
    duracion_actual: int
    
    # Ajustes solicitados
    agregar: str
    sacar: str
    dejar: str
    
    # Plan anterior
    plan_anterior: str = Field(..., description="Plan anterior completo en texto")
    
    tipo_peso: str = "crudo"
    
    @property
    def diferencia_peso(self) -> float:
        return round(self.peso_actual - self.peso_anterior, 1)

class MealReplacementRequest(BaseModel):
    # Datos del reemplazo
    paciente: str
    comida_reemplazar: str = Field(..., description="desayuno/almuerzo/merienda/cena")
    nueva_comida: str = Field(..., description="Descripción de la nueva comida deseada")
    condiciones: Optional[str] = None
    
    # Comida actual
    comida_actual: str = Field(..., description="Descripción completa de la comida actual")
    
    # Macros a mantener
    proteinas: float
    carbohidratos: float
    grasas: float
    calorias: float
    
    tipo_peso: str = "crudo"

class MealPlanResponse(BaseModel):
    meal_plan: str = Field(..., description="Plan generado en formato texto")
    pdf_path: str = Field(..., description="Ruta al PDF generado")