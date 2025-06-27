# 🤖 Módulo `ai/` - Inteligencia Artificial

## 📋 Descripción General

El módulo `ai/` contiene todos los componentes relacionados con la Inteligencia Artificial del ChatBot de Hotelería. Este módulo implementa un sistema completo de IA que incluye modelos de lenguaje, procesamiento de texto, búsqueda semántica y gestión de recursos.

## 🏗️ Estructura del Módulo

```
ai/
├── __init__.py              # 📦 Inicialización del módulo
├── models.py                # 🧠 Gestión de modelos de IA
├── vectorstore.py           # 📚 Base de conocimiento vectorial
├── intent_detector.py       # 🎯 Detección de intenciones
├── text_generator.py        # ✍️ Generación de respuestas
├── cache.py                 # 💾 Sistema de caché
├── resource_manager.py      # ⚙️ Gestión de recursos
└── fallback_handler.py      # 🛡️ Manejo de fallbacks
```

## 📄 Documentación por Archivo

### 🧠 `models.py` - Gestión de Modelos de IA

**Propósito**: Centraliza la gestión de todos los modelos de IA utilizados en el sistema.

**Estructura**:
- **ModelFactory**: Factory pattern para crear instancias de modelos
- **AIModels**: Clase principal que gestiona todos los modelos
- **Lazy Loading**: Sistema de carga perezosa para optimizar memoria

**Funcionalidades**:
- ✅ Carga de modelos de resumen (BERT2BERT)
- ✅ Carga de modelos de generación (GPT-2 Spanish)
- ✅ Carga de modelos de embeddings (Sentence Transformers)
- ✅ Carga de clasificadores de intenciones (BART)
- ✅ Gestión de recursos con carga perezosa
- ✅ Fallback a modelos dummy en caso de error

**Uso**:
```python
from ai.models import ai_models

# Obtener modelo de generación (async)
generator = await ai_models.get_generador()

# Obtener modelo de embeddings (async)
embeddings = await ai_models.get_embedding_model()

# Obtener estadísticas
stats = ai_models.get_stats()
```

**Dependencias**:
- `torch`: Framework de machine learning
- `transformers`: Modelos de Hugging Face
- `langchain_huggingface`: Integración con LangChain
- `config.settings`: Configuración del sistema

---

### 📚 `vectorstore.py` - Base de Conocimiento Vectorial

**Propósito**: Gestiona la base de conocimiento vectorial para búsquedas semánticas en documentos del hotel.

**Estructura**:
- **VectorStoreManager**: Clase principal para gestión del vectorstore
- **Carga de Documentos**: Soporte para PDF, TXT, DOCX
- **Búsqueda Semántica**: Búsqueda por similitud vectorial
- **Gestión de Chunks**: División inteligente de documentos

**Funcionalidades**:
- ✅ Carga de múltiples formatos de documentos
- ✅ División automática en chunks optimizados
- ✅ Búsqueda semántica con FAISS
- ✅ Actualización dinámica de conocimiento
- ✅ Gestión de memoria con lazy loading
- ✅ Estadísticas de uso y rendimiento

**Uso**:
```python
from ai.vectorstore import vectorstore_manager

# Búsqueda síncrona
results = vectorstore_manager.search_context("¿Qué habitaciones tienen?", k=3)

# Búsqueda asíncrona (recomendado)
results = await vectorstore_manager.search_context_async("¿Cuál es el precio?", k=3)

# Actualizar conocimiento
vectorstore_manager.update_knowledge()

# Añadir documento específico
vectorstore_manager.add_document("nuevo_documento.txt")
```

**Dependencias**:
- `faiss`: Búsqueda vectorial eficiente
- `langchain`: Framework para aplicaciones de IA
- `ai.models`: Modelos de embeddings

---

### 🎯 `intent_detector.py` - Detección de Intenciones

**Propósito**: Clasifica automáticamente las intenciones de los usuarios para proporcionar respuestas más precisas.

**Estructura**:
- **Detección de Intenciones**: Clasificación automática de consultas
- **Mapeo de Intenciones**: Traducción de intenciones a acciones
- **Fallback Inteligente**: Manejo de casos no reconocidos

**Funcionalidades**:
- ✅ Clasificación automática de intenciones
- ✅ Soporte para múltiples categorías (habitaciones, restaurantes, etc.)
- ✅ Fallback inteligente para casos no reconocidos
- ✅ Integración con modelos de IA
- ✅ Cache de clasificaciones frecuentes

**Uso**:
```python
from ai.intent_detector import detect_intent

# Detectar intención
intent = detect_intent("¿Qué habitaciones tienen disponibles?")
# Resultado: "habitaciones"

# Con contexto adicional
intent = detect_intent("¿Cuál es el precio de la suite?", context="precios")
# Resultado: "precios"
```

**Dependencias**:
- `ai.models`: Modelos de clasificación
- `ai.cache`: Sistema de caché

---

### ✍️ `text_generator.py` - Generación de Respuestas

**Propósito**: Genera respuestas contextuales y naturales basadas en la información del hotel y las consultas de los usuarios.

**Estructura**:
- **Generación Contextual**: Respuestas basadas en contexto relevante
- **Formateo de Respuestas**: Aplicación de formato y estilo
- **Validación de Calidad**: Verificación de respuestas generadas

**Funcionalidades**:
- ✅ Generación de respuestas contextuales
- ✅ Integración con base de conocimiento
- ✅ Formateo automático de respuestas
- ✅ Validación de calidad de respuestas
- ✅ Soporte para múltiples idiomas
- ✅ Personalización según tipo de consulta

**Uso**:
```python
from ai.text_generator import generate_response

# Generar respuesta simple
response = await generate_response("¿Qué habitaciones tienen?")

# Generar respuesta con contexto específico
response = await generate_response(
    "¿Cuál es el precio?", 
    context="habitaciones_precios.txt"
)
```

**Dependencias**:
- `ai.models`: Modelos de generación
- `ai.vectorstore`: Base de conocimiento
- `ai.intent_detector`: Detección de intenciones

---

### 💾 `cache.py` - Sistema de Caché

**Propósito**: Optimiza el rendimiento del sistema mediante el almacenamiento temporal de respuestas frecuentes.

**Estructura**:
- **Cache de Respuestas**: Almacenamiento de respuestas generadas
- **Cache de Modelos**: Cache de modelos cargados
- **Gestión de Memoria**: Control automático del tamaño del cache
- **Políticas de Evicción**: LRU para gestión de memoria

**Funcionalidades**:
- ✅ Cache de respuestas con TTL configurable
- ✅ Cache de modelos para evitar recarga
- ✅ Gestión automática de memoria
- ✅ Estadísticas de rendimiento
- ✅ Limpieza automática de cache expirado
- ✅ Política LRU para evicción

**Uso**:
```python
from ai.cache import response_cache

# Obtener respuesta del cache
response = response_cache.get("clave_consulta")

# Almacenar respuesta en cache
response_cache.set("clave_consulta", "respuesta", ttl=3600)

# Obtener estadísticas
stats = response_cache.get_stats()
```

**Dependencias**:
- `config.settings`: Configuración de cache
- `utils.logger`: Sistema de logging

---

### ⚙️ `resource_manager.py` - Gestión de Recursos

**Propósito**: Gestiona eficientemente los recursos del sistema, especialmente la memoria y la carga de modelos pesados.

**Estructura**:
- **Gestión de Memoria**: Control del uso de RAM
- **Carga Lazy**: Carga de modelos solo cuando es necesario
- **Control de Concurrencia**: Gestión de múltiples requests simultáneos
- **Monitoreo de Recursos**: Seguimiento del uso de recursos

**Funcionalidades**:
- ✅ Carga perezosa de modelos pesados
- ✅ Control de concurrencia
- ✅ Gestión automática de memoria
- ✅ Monitoreo de recursos en tiempo real
- ✅ Limpieza automática de recursos no utilizados
- ✅ Fallback en caso de escasez de recursos

**Uso**:
```python
from ai.resource_manager import resource_manager

# Registrar modelo para carga perezosa
resource_manager.register_model("mi_modelo", create_function)

# Obtener modelo (se carga si es necesario)
model = await resource_manager.get_model("mi_modelo")

# Obtener estadísticas de recursos
stats = resource_manager.get_stats()
```

**Dependencias**:
- `config.settings`: Configuración de recursos
- `utils.logger`: Sistema de logging

---

### 🛡️ `fallback_handler.py` - Manejo de Fallbacks

**Propósito**: Proporciona respuestas de respaldo cuando los modelos principales fallan o no están disponibles.

**Estructura**:
- **Respuestas de Fallback**: Respuestas predefinidas para casos de error
- **Detección de Errores**: Identificación automática de fallos
- **Recuperación**: Mecanismos de recuperación automática
- **Logging de Errores**: Registro detallado de fallos

**Funcionalidades**:
- ✅ Respuestas de fallback predefinidas
- ✅ Detección automática de errores
- ✅ Recuperación automática de servicios
- ✅ Logging detallado de errores
- ✅ Respuestas contextuales de fallback
- ✅ Notificaciones de estado del sistema

**Uso**:
```python
from ai.fallback_handler import handle_fallback

# Manejar fallback automáticamente
response = await handle_fallback("consulta_usuario", error_type="model_error")

# Obtener respuesta de fallback específica
fallback_response = get_fallback_response("habitaciones")
```

**Dependencias**:
- `config.settings`: Configuración del sistema
- `utils.logger`: Sistema de logging

---

## 🔧 Características del Módulo

### ⚡ Optimización de Rendimiento
- **Lazy Loading**: Carga de modelos solo cuando es necesario
- **Sistema de Cache**: Almacenamiento temporal de respuestas
- **Gestión de Memoria**: Control eficiente de recursos
- **Búsqueda Vectorial**: FAISS para búsquedas rápidas

### 🔒 Robustez y Confiabilidad
- **Fallbacks Inteligentes**: Respuestas de respaldo automáticas
- **Manejo de Errores**: Gestión centralizada de excepciones
- **Validación**: Verificación de calidad de respuestas
- **Recuperación**: Mecanismos de recuperación automática

### 📈 Escalabilidad
- **Arquitectura Modular**: Fácil adición de nuevos modelos
- **Configuración Flexible**: Ajustes mediante variables de entorno
- **Monitoreo**: Seguimiento de rendimiento y recursos
- **Testing**: Pruebas automatizadas para cada componente

## 🚀 Inicio Rápido

```python
# Importar módulo completo
from ai import *

# Usar modelos de IA
generator = await ai_models.get_generador()
response = await generate_response("¿Qué servicios ofrecen?")

# Usar vectorstore
results = await vectorstore_manager.search_context_async("habitaciones")

# Usar cache
cached_response = response_cache.get("mi_consulta")
```

## 📝 Notas de Desarrollo

- **Lazy Loading**: Habilitado por defecto para optimizar memoria
- **Cache**: Configurable mediante variables de entorno
- **Logging**: Todos los componentes usan el logger centralizado
- **Testing**: Cada componente tiene pruebas unitarias
- **Documentación**: Mantener docstrings actualizados 