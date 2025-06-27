# 🎓 Módulo `training/` - Entrenamiento y Actualización

## 📋 Descripción General

El módulo `training/` maneja todo el proceso de entrenamiento, actualización y mantenimiento de los modelos de IA del ChatBot de Hotelería. Este módulo permite reentrenar modelos con nuevos datos, actualizar la base de conocimiento y optimizar el rendimiento del sistema.

## 🏗️ Estructura del Módulo

```
training/
├── __init__.py              # 📦 Inicialización del módulo
└── trainer.py               # 🎓 Entrenador principal de modelos
```

## 📄 Documentación por Archivo

### 🎓 `trainer.py` - Entrenador Principal de Modelos

**Propósito**: Gestiona el proceso completo de entrenamiento y actualización de modelos de IA, incluyendo la preparación de datos, entrenamiento y validación.

**Estructura**:
- **ModelTrainer**: Clase principal para entrenamiento
- **Preparación de Datos**: Procesamiento y limpieza de datos
- **Entrenamiento**: Fine-tuning de modelos existentes
- **Validación**: Evaluación de rendimiento
- **Despliegue**: Actualización de modelos en producción

**Funcionalidades**:
- ✅ Entrenamiento de modelos de IA con nuevos datos
- ✅ Actualización de la base de conocimiento vectorial
- ✅ Fine-tuning de modelos de lenguaje
- ✅ Validación automática de rendimiento
- ✅ Backup y rollback de modelos
- ✅ Optimización de hiperparámetros
- ✅ Generación de reportes de entrenamiento
- ✅ Monitoreo de progreso en tiempo real
- ✅ Gestión de versiones de modelos
- ✅ Entrenamiento incremental

**Estructura de Clases**:
```python
class ModelTrainer:
    def __init__(self):
        # Inicialización del entrenador
    
    def prepare_training_data(self, documents_dir):
        # Prepara datos para entrenamiento
    
    def train_models(self, model_type="all"):
        # Entrena modelos específicos
    
    def validate_models(self):
        # Valida rendimiento de modelos
    
    def deploy_models(self):
        # Despliega modelos entrenados
    
    def generate_training_report(self):
        # Genera reporte de entrenamiento
    
    def backup_current_models(self):
        # Crea backup de modelos actuales
    
    def rollback_to_previous_version(self):
        # Revierte a versión anterior
```

**Tipos de Entrenamiento**:

#### 🧠 Entrenamiento de Modelos de Lenguaje
- **Fine-tuning**: Adaptación de modelos pre-entrenados
- **Transfer Learning**: Aprovechamiento de conocimiento previo
- **Domain Adaptation**: Adaptación al dominio hotelero
- **Multi-task Learning**: Entrenamiento en múltiples tareas

#### 📚 Actualización de Base de Conocimiento
- **Vectorización**: Conversión de documentos a embeddings
- **Indexación**: Creación de índices de búsqueda
- **Actualización Incremental**: Adición de nuevos documentos
- **Optimización**: Mejora de relevancia de búsquedas

#### 🎯 Entrenamiento Específico por Dominio
- **Clasificación de Intenciones**: Mejora de detección de intenciones
- **Generación de Respuestas**: Optimización de respuestas contextuales
- **Extracción de Entidades**: Identificación de información relevante
- **Análisis de Sentimientos**: Evaluación de satisfacción

**Uso**:
```python
from training.trainer import ModelTrainer

# Crear instancia del entrenador
trainer = ModelTrainer()

# Preparar datos de entrenamiento
trainer.prepare_training_data("documentos/")

# Entrenar todos los modelos
trainer.train_models("all")

# Validar rendimiento
validation_results = trainer.validate_models()

# Desplegar modelos si la validación es exitosa
if validation_results['overall_score'] > 0.8:
    trainer.deploy_models()
    print("✅ Modelos desplegados exitosamente")
else:
    print("❌ Validación falló, manteniendo modelos anteriores")
```

**Funciones Principales**:

#### `prepare_training_data(documents_dir)`
- **Propósito**: Prepara datos para el entrenamiento
- **Parámetros**:
  - `documents_dir`: Directorio con documentos de entrenamiento
- **Funcionalidad**:
  - Carga y limpia documentos
  - Divide en conjuntos de entrenamiento/validación
  - Preprocesa texto para modelos de IA
  - Valida calidad de datos
  - Genera embeddings de entrenamiento

#### `train_models(model_type="all")`
- **Propósito**: Entrena modelos específicos o todos los modelos
- **Parámetros**:
  - `model_type`: Tipo de modelo ("generator", "classifier", "embeddings", "all")
- **Funcionalidad**:
  - Ejecuta fine-tuning de modelos
  - Monitorea progreso en tiempo real
  - Guarda checkpoints durante entrenamiento
  - Optimiza hiperparámetros
  - Maneja errores de entrenamiento

#### `validate_models()`
- **Propósito**: Evalúa el rendimiento de los modelos entrenados
- **Retorna**: Diccionario con métricas de rendimiento
- **Funcionalidad**:
  - Ejecuta pruebas en conjunto de validación
  - Calcula métricas de precisión y recall
  - Compara con modelos anteriores
  - Identifica áreas de mejora
  - Genera reportes de rendimiento

#### `deploy_models()`
- **Propósito**: Despliega modelos entrenados a producción
- **Funcionalidad**:
  - Crea backup de modelos actuales
  - Reemplaza modelos con versiones entrenadas
  - Actualiza configuración del sistema
  - Verifica funcionamiento correcto
  - Notifica cambios a administradores

#### `generate_training_report()`
- **Propósito**: Genera reporte detallado del entrenamiento
- **Retorna**: Reporte en formato estructurado
- **Funcionalidad**:
  - Resume métricas de entrenamiento
  - Compara con entrenamientos anteriores
  - Identifica mejoras y degradaciones
  - Proporciona recomendaciones
  - Incluye visualizaciones de rendimiento

#### `backup_current_models()`
- **Propósito**: Crea backup de modelos actuales
- **Funcionalidad**:
  - Guarda copia de seguridad
  - Mantiene historial de versiones
  - Permite rollback si es necesario
  - Comprime archivos para ahorrar espacio
  - Registra metadatos de backup

#### `rollback_to_previous_version()`
- **Propósito**: Revierte a versión anterior de modelos
- **Funcionalidad**:
  - Restaura modelos de backup
  - Verifica integridad de restauración
  - Actualiza configuración
  - Notifica rollback
  - Registra motivo del rollback

**Dependencias**:
- `torch`: Framework de machine learning
- `transformers`: Modelos de Hugging Face
- `datasets`: Gestión de conjuntos de datos
- `scikit-learn`: Métricas de evaluación
- `ai.models`: Modelos de IA del sistema
- `ai.vectorstore`: Base de conocimiento
- `config.settings`: Configuración del sistema
- `utils.logger`: Sistema de logging

---

## 🔧 Características del Módulo

### 🎯 Entrenamiento Inteligente
- **Fine-tuning Adaptativo**: Ajuste automático de hiperparámetros
- **Transfer Learning**: Aprovechamiento de modelos pre-entrenados
- **Domain Adaptation**: Especialización en dominio hotelero
- **Multi-task Learning**: Entrenamiento en múltiples tareas simultáneas

### 📊 Validación Robusta
- **Métricas Múltiples**: Evaluación desde diferentes perspectivas
- **Validación Cruzada**: Estimación robusta de rendimiento
- **Comparación Automática**: Análisis de mejora vs degradación
- **Alertas Inteligentes**: Notificaciones de problemas críticos

### 🔄 Gestión de Versiones
- **Control de Versiones**: Seguimiento de cambios en modelos
- **Backup Automático**: Copias de seguridad antes de cambios
- **Rollback Seguro**: Reversión a versiones anteriores
- **Despliegue Gradual**: Implementación controlada de cambios

### 📈 Monitoreo Avanzado
- **Progreso en Tiempo Real**: Seguimiento durante entrenamiento
- **Métricas de Rendimiento**: Evaluación continua de calidad
- **Alertas de Problemas**: Notificaciones de errores críticos
- **Reportes Automáticos**: Documentación de entrenamientos

## 🚀 Configuración del Sistema

### Variables de Entorno
```bash
# Configuración de Entrenamiento
TRAINING_BATCH_SIZE=16
TRAINING_EPOCHS=10
TRAINING_LEARNING_RATE=0.0001
TRAINING_VALIDATION_SPLIT=0.2

# Configuración de Modelos
MODEL_VERSION=1.0.0
ENABLE_MODEL_BACKUP=true
AUTO_DEPLOY_ON_SUCCESS=true

# Configuración de Validación
MIN_VALIDATION_SCORE=0.8
ENABLE_AUTO_ROLLBACK=true
VALIDATION_METRICS=accuracy,precision,recall,f1
```

### Configuración por Entorno

#### Desarrollo
```bash
TRAINING_EPOCHS=3
TRAINING_BATCH_SIZE=8
MIN_VALIDATION_SCORE=0.7
AUTO_DEPLOY_ON_SUCCESS=false
```

#### Producción
```bash
TRAINING_EPOCHS=20
TRAINING_BATCH_SIZE=32
MIN_VALIDATION_SCORE=0.85
AUTO_DEPLOY_ON_SUCCESS=true
ENABLE_MODEL_BACKUP=true
```

## 📁 Estructura de Datos

### Archivos de Entrenamiento
```
training/
├── data/                    # 📊 Datos de entrenamiento
│   ├── raw/                 # Datos sin procesar
│   ├── processed/           # Datos procesados
│   └── validation/          # Conjunto de validación
├── models/                  # 🧠 Modelos entrenados
│   ├── current/             # Modelos actuales
│   ├── backup/              # Copias de seguridad
│   └── versions/            # Historial de versiones
├── logs/                    # 📝 Logs de entrenamiento
│   ├── training.log
│   └── validation.log
└── reports/                 # 📋 Reportes de entrenamiento
    ├── training_reports/
    └── validation_reports/
```

### Estructura de Configuración
```json
{
  "training_config": {
    "model_type": "generator",
    "batch_size": 16,
    "epochs": 10,
    "learning_rate": 0.0001,
    "validation_split": 0.2,
    "early_stopping": true,
    "patience": 3
  },
  "data_config": {
    "documents_dir": "documentos/",
    "preprocessing": {
      "clean_text": true,
      "normalize": true,
      "remove_stopwords": false
    }
  },
  "validation_config": {
    "metrics": ["accuracy", "precision", "recall", "f1"],
    "min_score": 0.8,
    "auto_rollback": true
  }
}
```

## 📊 Métricas de Entrenamiento

### 🎯 Métricas de Clasificación
- **Accuracy**: Precisión general del modelo
- **Precision**: Precisión por clase
- **Recall**: Sensibilidad por clase
- **F1-Score**: Media armónica de precisión y recall
- **Confusion Matrix**: Matriz de confusión detallada

### 📈 Métricas de Generación
- **BLEU Score**: Calidad de texto generado
- **ROUGE Score**: Coincidencia con referencias
- **Perplexity**: Medida de incertidumbre del modelo
- **Response Relevance**: Relevancia de respuestas

### ⚡ Métricas de Rendimiento
- **Training Time**: Tiempo total de entrenamiento
- **Inference Time**: Tiempo de inferencia
- **Memory Usage**: Uso de memoria durante entrenamiento
- **GPU Utilization**: Utilización de GPU si está disponible

## 🚀 Inicio Rápido

```python
# Importar entrenador
from training.trainer import ModelTrainer

# Crear instancia
trainer = ModelTrainer()

# Ejecutar entrenamiento completo
try:
    # Preparar datos
    trainer.prepare_training_data("documentos/")
    
    # Entrenar modelos
    trainer.train_models("all")
    
    # Validar rendimiento
    results = trainer.validate_models()
    
    # Desplegar si es exitoso
    if results['overall_score'] > 0.8:
        trainer.deploy_models()
        print("✅ Entrenamiento completado exitosamente")
    else:
        print("❌ Validación falló, manteniendo modelos anteriores")
        
except Exception as e:
    print(f"❌ Error durante entrenamiento: {e}")
    trainer.rollback_to_previous_version()
```

## 📝 Notas de Desarrollo

- **Backup**: Siempre crear backup antes de entrenar
- **Validación**: Validar modelos antes de desplegar
- **Monitoreo**: Seguir progreso durante entrenamiento
- **Rollback**: Tener plan de rollback en caso de problemas
- **Documentación**: Mantener registro de cambios en modelos
- **Testing**: Probar modelos en entorno de desarrollo antes de producción 