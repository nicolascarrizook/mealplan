# Prompt Técnico Completo - Sistema de Planes Nutricionales

## Contexto del Proyecto

Necesito desarrollar una aplicación web completa para generar planes nutricionales personalizados. El sistema debe reemplazar a una secretaria que genera planes manualmente. La aplicación utiliza el método "Tres Días y Carga | Dieta Inteligente® & Nutrición Evolutiva" y debe generar planes de 3 días iguales con recetas específicas.

## Stack Tecnológico Requerido

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React 18 con TypeScript
- **UI Components**: shadcn/ui (ya tengo context7 instalado, úsalo para las librerías actualizadas)
- **Base de Datos**: PostgreSQL para usuarios/pacientes, ChromaDB para búsqueda vectorial de recetas
- **LLM**: OpenAI GPT-4 para generación de planes
- **Autenticación**: JWT
- **ORM**: SQLAlchemy
- **Validación**: Pydantic
- **PDF Generation**: ReportLab o WeasyPrint
- **Deployment**: Docker + docker-compose

## Estructura del Proyecto

```
meal-planner/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── patient.py
│   │   │   ├── meal_plan.py
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── patient.py
│   │   │   ├── meal_plan.py
│   │   │   └── auth.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── patients.py
│   │   │   ├── meal_plans.py
│   │   │   └── recipes.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── openai_service.py
│   │   │   ├── chromadb_service.py
│   │   │   ├── meal_plan_generator.py
│   │   │   ├── prompt_generator.py
│   │   │   └── pdf_generator.py
│   │   └── prompts/
│   │       ├── __init__.py
│   │       └── nutritional_prompt.py
│   ├── data/
│   │   └── recipes_structured.json
│   ├── scripts/
│   │   └── load_recipes.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── forms/
│   │   │   │   ├── PatientForm.tsx
│   │   │   │   ├── ControlForm.tsx
│   │   │   │   └── MealReplacementForm.tsx
│   │   │   ├── ui/ (shadcn components)
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Layout.tsx
│   │   │   └── meal-plan/
│   │   │       ├── MealPlanView.tsx
│   │   │       └── MealPlanPDF.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── NewPatient.tsx
│   │   │   ├── PatientControl.tsx
│   │   │   ├── MealReplacement.tsx
│   │   │   └── Patients.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useMealPlan.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Funcionalidades Principales

### 1. Sistema de Autenticación

- Login para nutricionistas
- JWT tokens con refresh
- Middleware de autenticación en FastAPI

### 2. Tres Motores de Generación de Planes

#### Motor 1: Paciente Nuevo

Formulario con campos:

- Datos personales (nombre, edad, sexo, peso, altura)
- Objetivo (bajar/subir/mantener peso con opciones de 0.5kg o 1kg por semana)
- Actividad física (tipo, frecuencia, duración)
- Restricciones alimentarias
- Preferencias
- Horarios
- Nivel económico (Sin restricciones, Medio, Limitado, Bajo recursos)
- Tipo de peso (crudo/cocido)
- Número de comidas principales (3 o 4)
- Colaciones (No, Por saciedad, Pre-entreno, Post-entreno)

#### Motor 2: Control de Paciente

- Buscar paciente existente
- Mostrar plan anterior
- Campos para ajustes (AGREGAR/SACAR/DEJAR)
- Actualización de peso y objetivos

#### Motor 3: Reemplazo de Comida

- Seleccionar paciente y plan actual
- Elegir comida a reemplazar
- Especificar nueva comida deseada
- Mantener macros equivalentes

### 3. Base de Datos de Recetas

Tengo un archivo `recipes_structured.json` con 85 recetas estructuradas que te proporcionaré por separado. Este archivo contiene:

- ID único
- Nombre de la receta
- Tipo de comida (desayuno, almuerzo, cena, merienda)
- Ingredientes con cantidades exactas
- Preparación detallada
- Información nutricional completa (calorías, proteínas, carbohidratos, grasas)
- Tags y categorías
- Compatibilidad con diferentes dietas

### 4. Generación de PDF

- Formato profesional con logo
- Plan de 3 días
- Resumen nutricional
- Recomendaciones personalizadas

## Implementación del Generador de Prompts

El sistema debe seguir exactamente el método del nutricionista. Aquí está la clase completa para generar los prompts:

```python
# backend/app/services/prompt_generator.py

class PromptGenerator:
    def __init__(self):
        self.base_rules = """
REGLAS FUNDAMENTALES DEL MÉTODO:
1. Plan de 3 días iguales
2. Todas las cantidades en GRAMOS
3. Verduras tipo C (papa, batata, choclo) en gramos específicos
4. Otras verduras: porción libre pero coherente
5. Frutas siempre en gramos
6. Incluir forma de preparación para cada comida
7. No usar suplementos salvo indicación expresa
8. Usar léxico argentino
9. Respetar horarios del paciente
10. Adaptarse al nivel económico
"""

    def generate_motor1_prompt(self, patient_data, recipes_json):
        """Motor 1: Paciente Nuevo"""

        prompt = f"""
{self.base_rules}

MOTOR 1 - PACIENTE NUEVO
Generá un plan alimentario de 3 días iguales siguiendo el método.

DATOS DEL PACIENTE:
- Nombre: {patient_data.nombre}
- Edad: {patient_data.edad} años
- Sexo: {patient_data.sexo}
- Estatura: {patient_data.estatura} cm
- Peso: {patient_data.peso} kg
- IMC: {patient_data.imc}
- Objetivo: {patient_data.objetivo}

ACTIVIDAD FÍSICA:
- Tipo: {patient_data.tipo_actividad}
- Frecuencia: {patient_data.frecuencia_semanal}x por semana
- Duración: {patient_data.duracion_sesion} minutos

ESPECIFICACIONES MÉDICAS:
- Suplementación: {patient_data.suplementacion or 'Ninguna'}
- Patologías/Medicación: {patient_data.patologias or 'Sin patologías'}
- NO consume: {patient_data.no_consume or 'Sin restricciones'}
- Le gusta: {patient_data.le_gusta}
- Nivel económico: {patient_data.nivel_economico}

HORARIOS:
{self._format_horarios(patient_data.horarios)}

CONFIGURACIÓN DEL PLAN:
- Comidas principales: {patient_data.comidas_principales}
- Colaciones: {patient_data.colaciones}
- Tipo de peso: Gramos en {patient_data.tipo_peso}

RECETAS DISPONIBLES:
{recipes_json}

INSTRUCCIONES PARA LA GENERACIÓN:
1. USAR ÚNICAMENTE las recetas proporcionadas arriba
2. Adaptar las cantidades según los objetivos
3. Respetar las restricciones alimentarias
4. Cada día debe tener exactamente las mismas comidas
5. Incluir preparación detallada
6. Calcular macros totales al final

FORMATO DE SALIDA ESPERADO:

PLAN ALIMENTARIO - 3 DÍAS IGUALES

DESAYUNO (horario)
- [Nombre de la receta de la base de datos]
- Ingredientes con cantidades ajustadas:
  * Ingrediente 1: XXg
  * Ingrediente 2: XXg
- Preparación: [de la receta]

ALMUERZO (horario)
[Mismo formato]

MERIENDA (horario)
[Mismo formato]

CENA (horario)
[Mismo formato]

COLACIÓN PRE/POST ENTRENO (si aplica)
[Mismo formato]

RESUMEN NUTRICIONAL DIARIO:
- Proteínas: XXg
- Carbohidratos: XXg
- Grasas: XXg
- Calorías totales: XXXX kcal
- Déficit/Superávit: apropiado para objetivo

RECOMENDACIONES PERSONALIZADAS:
- Hidratación
- Timing de suplementos
- Tips de preparación
"""
        return prompt

    def generate_motor2_prompt(self, control_data, previous_plan, recipes_json):
        """Motor 2: Control y Ajuste"""

        prompt = f"""
{self.base_rules}

MOTOR 2 - CONTROL DE PACIENTE
Reformulá el plan completo con base en los nuevos requerimientos.

DATOS ACTUALIZADOS:
- Nombre: {control_data.nombre}
- Fecha del control: {control_data.fecha_control}
- Peso anterior: {control_data.peso_anterior} kg
- Peso actual: {control_data.peso_actual} kg
- Diferencia: {control_data.diferencia_peso} kg
- Objetivo actualizado: {control_data.objetivo_actualizado}

CAMBIOS EN ACTIVIDAD:
- Tipo actual: {control_data.tipo_actividad_actual}
- Frecuencia: {control_data.frecuencia_actual}
- Duración: {control_data.duracion_actual}

AJUSTES SOLICITADOS:
- AGREGAR: {control_data.agregar}
- SACAR: {control_data.sacar}
- DEJAR: {control_data.dejar}

PLAN ANTERIOR:
{previous_plan}

RECETAS DISPONIBLES:
{recipes_json}

INSTRUCCIONES:
1. Analizar la evolución del paciente
2. Ajustar calorías según nuevo objetivo
3. Implementar los cambios solicitados
4. Mantener la estructura de 3 días iguales
5. Usar solo recetas de la base de datos

[Formato de salida igual que Motor 1]
"""
        return prompt

    def generate_motor3_prompt(self, meal_data, current_meal, recipes_json):
        """Motor 3: Reemplazo de Comida"""

        prompt = f"""
{self.base_rules}

MOTOR 3 - REEMPLAZO DE COMIDA ESPECÍFICA
Reemplazá una comida manteniendo los mismos macros y calorías.

DATOS:
- Paciente: {meal_data.paciente}
- Comida a reemplazar: {meal_data.comida_reemplazar}
- Nueva comida deseada: {meal_data.nueva_comida}
- Condiciones especiales: {meal_data.condiciones}
- Tipo de peso: Gramos en {meal_data.tipo_peso}

COMIDA ACTUAL:
{current_meal}

MACROS A MANTENER:
- Proteínas: {meal_data.proteinas}g ±5g
- Carbohidratos: {meal_data.carbohidratos}g ±5g
- Grasas: {meal_data.grasas}g ±3g
- Calorías: {meal_data.calorias} kcal ±50 kcal

RECETAS DISPONIBLES:
{recipes_json}

INSTRUCCIONES:
1. Buscar en las recetas una opción similar a lo solicitado
2. Ajustar cantidades para mantener macros
3. Respetar el método de preparación
4. Incluir comparación de macros (original vs nuevo)

FORMATO DE SALIDA:

REEMPLAZO DE {meal_data.comida_reemplazar}

OPCIÓN NUEVA:
- [Nombre de la receta]
- Ingredientes ajustados:
  * [Lista con cantidades]
- Preparación: [Detallada]

COMPARACIÓN NUTRICIONAL:
Original | Nuevo
Proteínas: XXg | XXg
Carbohidratos: XXg | XXg
Grasas: XXg | XXg
Calorías: XXX | XXX

✓ Diferencia dentro de rangos aceptables
"""
        return prompt

    def _format_horarios(self, horarios):
        """Formatea los horarios del paciente"""
        return "\n".join([f"- {comida}: {hora}" for comida, hora in horarios.items()])

    def filter_recipes_by_criteria(self, recipes, criteria):
        """Filtra recetas según criterios del paciente"""
        filtered = []

        for recipe in recipes:
            # Filtrar por restricciones
            if criteria.get('no_consume'):
                ingredients_text = " ".join([ing['item'] for ing in recipe['ingredientes']])
                if any(restricted in ingredients_text for restricted in criteria['no_consume']):
                    continue

            # Filtrar por tipo de comida
            if criteria.get('tipo_comida'):
                if criteria['tipo_comida'] not in recipe['tipo_comida']:
                    continue

            # Filtrar por dieta especial
            if criteria.get('dieta_especial'):
                if criteria['dieta_especial'] not in recipe['apto_para']:
                    continue

            # Filtrar por nivel económico
            if criteria.get('nivel_economico') == 'Bajo recursos':
                # Evitar recetas con ingredientes caros
                expensive = ['salmón', 'lomo', 'camarones', 'langostinos']
                ingredients_text = " ".join([ing['item'] for ing in recipe['ingredientes']])
                if any(exp in ingredients_text for exp in expensive):
                    continue

            filtered.append(recipe)

        return filtered

    def format_recipes_for_prompt(self, recipes, tipo_comida=None):
        """Formatea las recetas para incluir en el prompt"""
        if tipo_comida:
            recipes = [r for r in recipes if tipo_comida in r['tipo_comida']]

        formatted = []
        for recipe in recipes[:20]:  # Limitar a 20 recetas por tipo
            ing_list = "\n  ".join([f"- {ing['item']}: {ing['cantidad']}"
                                   for ing in recipe['ingredientes']])

            formatted.append(f"""
RECETA: {recipe['nombre']}
ID: {recipe['id']}
Tipo: {', '.join(recipe['tipo_comida'])}
Ingredientes:
  {ing_list}
Preparación: {recipe['preparacion']}
Nutrición: {recipe['calorias_aprox']} kcal | P: {recipe['proteinas_aprox']}g | C: {recipe['carbohidratos_aprox']}g | G: {recipe['grasas_aprox']}g
Apto para: {', '.join(recipe['apto_para'])}
Tags: {', '.join(recipe['tags'])}
""")

        return "\n".join(formatted)
```

## Modelos de Datos (Pydantic)

```python
# backend/app/schemas/patient.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PatientData:
    # Motor 1 - Paciente Nuevo
    nombre: str
    edad: int
    sexo: str
    estatura: float
    peso: float
    objetivo: str
    tipo_actividad: str
    frecuencia_semanal: int
    duracion_sesion: int
    suplementacion: Optional[str] = None
    patologias: Optional[str] = None
    no_consume: Optional[str] = None
    le_gusta: Optional[str] = None
    horarios: Optional[Dict[str, str]] = None
    nivel_economico: str = "Medio"
    notas_personales: Optional[str] = None
    comidas_principales: int = 4
    colaciones: str = "No"
    tipo_peso: str = "crudo"

    @property
    def imc(self):
        return round(self.peso / (self.estatura/100)**2, 1)

@dataclass
class ControlData:
    # Motor 2 - Control
    nombre: str
    fecha_control: str
    peso_anterior: float
    peso_actual: float
    objetivo_actualizado: str
    tipo_actividad_actual: str
    frecuencia_actual: int
    duracion_actual: int
    agregar: str
    sacar: str
    dejar: str
    tipo_peso: str = "crudo"

    @property
    def diferencia_peso(self):
        return round(self.peso_actual - self.peso_anterior, 1)

@dataclass
class MealReplacementData:
    # Motor 3 - Reemplazo
    paciente: str
    comida_reemplazar: str
    nueva_comida: str
    condiciones: Optional[str] = None
    tipo_peso: str = "crudo"
    proteinas: float = 0
    carbohidratos: float = 0
    grasas: float = 0
    calorias: float = 0
```

## API Endpoints Necesarios

```
POST /auth/login
POST /auth/refresh
GET /patients
POST /patients
GET /patients/{id}
PUT /patients/{id}
POST /meal-plans/generate (motor 1)
POST /meal-plans/control (motor 2)
POST /meal-plans/replace-meal (motor 3)
GET /meal-plans/{id}
GET /meal-plans/{id}/pdf
GET /recipes/search
```

## Configuración de Docker

```yaml
# docker-compose.yml
version: "3.8"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mealplanner
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - chromadb
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mealplanner
    volumes:
      - postgres_data:/var/lib/postgresql/data

  chromadb:
    image: chromadb/chroma
    ports:
      - "8001:8000"
    volumes:
      - chromadb_data:/chroma/chroma

volumes:
  postgres_data:
  chromadb_data:
```

## Script para Cargar Recetas en ChromaDB

```python
# backend/scripts/load_recipes.py
import json
import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()

def load_recipes_to_chromadb():
    # Cargar recetas del JSON
    with open('../data/recipes_structured.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Configurar ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-ada-002"
    )

    # Crear o obtener colección
    collection = client.get_or_create_collection(
        name="recipes",
        embedding_function=embedding_function
    )

    # Preparar documentos
    documents = []
    metadatas = []
    ids = []

    for recipe in data['recipes']:
        # Crear texto para embedding
        ingredients_text = ", ".join([
            f"{ing['cantidad']} de {ing['item']}"
            for ing in recipe['ingredientes']
        ])

        document = f"""
        Receta: {recipe['nombre']}
        Tipo de comida: {', '.join(recipe['tipo_comida'])}
        Ingredientes: {ingredients_text}
        Preparación: {recipe['preparacion']}
        Información nutricional: {recipe['calorias_aprox']} calorías,
        {recipe['proteinas_aprox']}g proteínas,
        {recipe['carbohidratos_aprox']}g carbohidratos,
        {recipe['grasas_aprox']}g grasas
        Apto para: {', '.join(recipe['apto_para'])}
        """

        documents.append(document)
        ids.append(recipe['id'])
        metadatas.append({
            "recipe_id": recipe['id'],
            "nombre": recipe['nombre'],
            "tipo_comida": ",".join(recipe['tipo_comida']),
            "calorias": recipe['calorias_aprox'],
            "proteinas": recipe['proteinas_aprox'],
            "carbohidratos": recipe['carbohidratos_aprox'],
            "grasas": recipe['grasas_aprox'],
            "tiempo_preparacion": recipe['tiempo_preparacion'],
            "apto_para": ",".join(recipe['apto_para']),
            "tags": ",".join(recipe['tags'])
        })

    # Cargar en ChromaDB
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"✅ {len(documents)} recetas cargadas exitosamente en ChromaDB")

if __name__ == "__main__":
    load_recipes_to_chromadb()
```

## Configuración de Variables de Entorno

```bash
# .env.example
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mealplanner

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# JWT
JWT_SECRET_KEY=your_super_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# ChromaDB
CHROMADB_HOST=localhost
CHROMADB_PORT=8001

# Application
APP_NAME=Meal Planner Pro
APP_VERSION=1.0.0
DEBUG=True

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

## Consideraciones Importantes para la Implementación

1. **Arquitectura de Microservicios**: Considera separar el servicio de generación de planes del resto de la aplicación para escalar independientemente.

2. **Cache de Respuestas**: Implementa un sistema de cache para respuestas de OpenAI similares para reducir costos.

3. **Queue System**: Para planes complejos, usa Celery o similar para procesamiento asíncrono.

4. **Monitoring**: Implementa logging detallado y métricas para trackear uso de OpenAI y rendimiento.

5. **Backup**: Sistema automático de backup para la base de datos de pacientes y planes.

6. **Rate Limiting**: Implementa rate limiting en los endpoints de generación para evitar abuso.

7. **Validación Estricta**: Toda entrada de usuario debe ser validada exhaustivamente.

8. **Testing**: Implementa tests unitarios y de integración desde el inicio.

## UI/UX con shadcn/ui

Para el frontend, usa estos componentes de shadcn/ui:

- **Form** con react-hook-form para validación
- **Card** para secciones del formulario
- **Select** para opciones predefinidas
- **RadioGroup** para objetivos
- **Checkbox** para preferencias múltiples
- **Button** con estados de loading
- **Toast** para notificaciones
- **Dialog** para confirmaciones
- **Table** para lista de pacientes
- **Tabs** para los 3 motores
- **Skeleton** para loading states

## Flujo de Usuario

1. **Login**: Nutricionista se autentica
2. **Dashboard**: Ve estadísticas y accesos rápidos
3. **Selección de Motor**: Elige entre los 3 motores
4. **Formulario**: Completa datos según el motor
5. **Generación**: Sistema genera el plan con GPT-4
6. **Vista Previa**: Muestra el plan generado
7. **Edición**: Permite ajustes manuales si es necesario
8. **PDF**: Descarga el plan en formato PDF
9. **Guardado**: Se almacena en la base de datos

## Pasos para Comenzar

1. **Crea la estructura de carpetas** exactamente como se muestra
2. **Configura Docker** y las variables de entorno
3. **Solicítame el archivo de recetas** por separado
4. **Copia las recetas** al archivo `backend/data/recipes_structured.json`
5. **Ejecuta el script** para cargar recetas en ChromaDB
6. **Implementa la autenticación** básica
7. **Crea el primer formulario** (Motor 1)
8. **Integra con OpenAI**
9. **Genera el primer plan** de prueba
10. **Continúa con los demás features**

## Notas Adicionales

- El sistema debe ser **responsive** para uso en tablets
- Implementar **modo oscuro** con shadcn/ui
- Añadir **breadcrumbs** para navegación
- Incluir **atajos de teclado** para acciones frecuentes
- Implementar **autoguardado** en formularios largos
- Considerar **PWA** para uso offline básico

Comienza organizando el proyecto con esta estructura y configurando el entorno base con Docker. Una vez que tengas la estructura lista, solicítame el archivo de recetas por separado.
