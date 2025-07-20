from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, List, Any
from enum import Enum

# Enums para mejor validación y consistencia
class Sexo(str, Enum):
    masculino = "masculino"
    femenino = "femenino"

class Objetivo(str, Enum):
    mantener = "mantener"
    bajar_025 = "bajar_025"  # Bajar 0.25 kg/semana
    bajar_05 = "bajar_05"    # Bajar 0.5 kg/semana
    bajar_075 = "bajar_075"  # Bajar 0.75 kg/semana
    bajar_1 = "bajar_1"      # Bajar 1 kg/semana
    subir_025 = "subir_025"  # Subir 0.25 kg/semana
    subir_05 = "subir_05"    # Subir 0.5 kg/semana
    subir_075 = "subir_075"  # Subir 0.75 kg/semana
    subir_1 = "subir_1"      # Subir 1 kg/semana

class NivelEconomico(str, Enum):
    sin_restricciones = "Sin restricciones"
    medio = "Medio"
    limitado = "Limitado"
    bajo_recursos = "Bajo recursos"

class TipoPeso(str, Enum):
    crudo = "crudo"
    cocido = "cocido"

class TipoColacion(str, Enum):
    no = "No"
    por_saciedad = "Por saciedad"
    pre_entreno = "Pre-entreno"
    post_entreno = "Post-entreno"

class ProteinLevel(str, Enum):
    muy_baja = "muy_baja"        # 0.5-0.8 g/kg (patologías renales)
    conservada = "conservada"     # 0.8-1.2 g/kg (normal)
    moderada = "moderada"         # 1.2-1.6 g/kg (personas activas no deportistas)
    alta = "alta"                 # 1.6-2.2 g/kg (uso deportivo)
    muy_alta = "muy_alta"        # 2.2-2.8 g/kg (deportistas alto rendimiento)
    extrema = "extrema"          # 3.0-3.5 g/kg (atletas con requerimientos especiales)

class DistributionType(str, Enum):
    traditional = "traditional"   # Distribución variable de calorías (más en almuerzo)
    equitable = "equitable"      # Distribución equitativa entre comidas
    custom = "custom"            # Distribución personalizada por el usuario

# Schemas para suplementos con información clínica
class SupplementInfo(BaseModel):
    id: str
    name: str
    servings: float = 1
    custom_dose: Optional[str] = None  # Ej: "400mg", "10g", "2000UI"
    frequency: Optional[str] = None    # Ej: "1 vez al día", "con desayuno y cena"
    clinical_relevance: bool = False   # Marca si tiene incidencia clínica
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fats: float = 0
    serving_size: Optional[str] = None
    notes: Optional[str] = None

# Schema para medicamentos con más detalle
class MedicationInfo(BaseModel):
    id: str
    name: str
    dose: Optional[str] = None
    frequency: Optional[str] = None
    impact: Optional[str] = None
    considerations: Optional[str] = None

class NewPatientRequest(BaseModel):
    # Datos personales
    nombre: str = Field(..., min_length=2, max_length=100)
    edad: int = Field(..., ge=1, le=120)
    sexo: Sexo
    estatura: float = Field(..., gt=50, le=250, description="Altura en cm")
    peso: float = Field(..., gt=20, le=300, description="Peso en kg")
    
    # Objetivo
    objetivo: Objetivo
    
    # Actividad física
    tipo_actividad: str
    frecuencia_semanal: int = Field(..., ge=0, le=7)
    duracion_sesion: int = Field(..., description="Duración en minutos (30/45/60/75/90/120)")
    
    # Especificaciones médicas
    suplementacion: Optional[str] = None
    patologias: Optional[str] = None
    no_consume: Optional[str] = None
    le_gusta: Optional[str] = None
    
    # Configuración del plan
    nivel_economico: NivelEconomico = NivelEconomico.medio
    notas_personales: Optional[str] = None
    comidas_principales: int = Field(default=4, ge=3, le=4)
    colaciones: TipoColacion = TipoColacion.no
    tipo_peso: TipoPeso = TipoPeso.crudo
    
    # Personalización de macros (nuevos campos)
    carbs_percentage: Optional[int] = Field(None, ge=0, le=55, description="Porcentaje de carbohidratos (0-55%)")
    protein_level: Optional[ProteinLevel] = Field(None, description="Nivel de proteína según actividad")
    fat_percentage: Optional[int] = Field(None, ge=15, le=45, description="Porcentaje de grasas")
    distribution_type: DistributionType = Field(default=DistributionType.traditional)
    
    # Distribución personalizada por comida (solo si distribution_type == "custom")
    custom_meal_distribution: Optional[Dict[str, Dict[str, float]]] = Field(
        None, 
        description="Distribución personalizada de calorías y macros por comida"
    )
    
    # Nuevos campos para actividades, suplementos y medicamentos
    activities: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Lista de actividades físicas con duración, frecuencia y calorías"
    )
    supplements: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Lista de suplementos con porciones y macros"
    )
    medications: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Lista de medicamentos con impacto nutricional"
    )
    
    @validator('duracion_sesion')
    def validate_duration(cls, v):
        valid_durations = [30, 45, 60, 75, 90, 120]
        if v not in valid_durations:
            raise ValueError(f'La duración debe ser una de: {valid_durations}')
        return v
    
    @validator('carbs_percentage')
    def validate_carbs(cls, v):
        if v is not None:
            if v % 5 != 0:
                raise ValueError('El porcentaje de carbohidratos debe ser múltiplo de 5')
            if v < 0 or v > 55:
                raise ValueError('El porcentaje de carbohidratos debe estar entre 0 y 55')
        return v
    
    @property
    def imc(self) -> float:
        return round(self.peso / (self.estatura/100)**2, 1)
    
    @property
    def imc_category(self) -> str:
        """Categoría del IMC"""
        if self.imc < 18.5:
            return "bajo peso"
        elif self.imc < 25:
            return "normal"
        elif self.imc < 30:
            return "sobrepeso"
        else:
            return "obesidad"

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
    
    tipo_peso: TipoPeso = TipoPeso.crudo
    
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
    
    tipo_peso: TipoPeso = TipoPeso.crudo

class MealPlanResponse(BaseModel):
    meal_plan: str = Field(..., description="Plan generado en formato texto")
    pdf_path: str = Field(..., description="Ruta al PDF generado")