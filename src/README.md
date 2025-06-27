# 📁 Carpeta `src` - Estructura del Proyecto ChatBot de Hotelería

## 🏗️ Estructura General

La carpeta `src` contiene toda la lógica principal del ChatBot de Hotelería, organizada en módulos especializados para facilitar el mantenimiento y escalabilidad del proyecto.

```
src/
├── main.py                 # 🚀 Punto de entrada principal del sistema
├── ai/                     # 🤖 Módulo de Inteligencia Artificial
├── analytics/              # 📊 Módulo de Análisis y Métricas
├── bot/                    # 🤖 Módulo del Bot de Telegram
├── config/                 # ⚙️ Módulo de Configuración
├── testing/                # 🧪 Módulo de Pruebas
├── training/               # 🎓 Módulo de Entrenamiento
└── utils/                  # 🛠️ Módulo de Utilidades
```

## 📋 Descripción de Módulos

### 🤖 Módulo `ai/` - Inteligencia Artificial
Contiene todos los componentes relacionados con la IA del sistema:
- **Modelos de IA**: Gestión de modelos de lenguaje, embeddings y clasificación
- **Vectorstore**: Base de conocimiento vectorial para búsquedas semánticas
- **Detección de Intenciones**: Clasificación automática de consultas de usuarios
- **Generación de Texto**: Creación de respuestas contextuales
- **Cache**: Sistema de caché para optimizar rendimiento
- **Gestión de Recursos**: Control de memoria y carga perezosa de modelos

### 📊 Módulo `analytics/` - Análisis y Métricas
Sistema de recolección y análisis de datos:
- **Métricas de Uso**: Seguimiento de interacciones de usuarios
- **Análisis de Rendimiento**: Estadísticas del sistema
- **Reportes**: Generación de informes automáticos

### 🤖 Módulo `bot/` - Bot de Telegram
Implementación del bot de Telegram:
- **Gestión de Comandos**: Manejo de comandos y callbacks
- **Procesamiento de Mensajes**: Lógica de respuesta a usuarios
- **Interfaz de Usuario**: Botones y elementos interactivos

### ⚙️ Módulo `config/` - Configuración
Gestión centralizada de configuración:
- **Variables de Entorno**: Configuración desde archivos .env
- **Validación**: Verificación de configuración correcta
- **Configuración Global**: Acceso centralizado a settings

### 🧪 Módulo `testing/` - Pruebas
Sistema de pruebas automatizadas:
- **Suite de Pruebas**: Tests unitarios y de integración
- **Configuración de Tests**: Setup para diferentes entornos
- **Ejecución**: Herramientas para correr pruebas

### 🎓 Módulo `training/` - Entrenamiento
Sistema de entrenamiento y actualización:
- **Entrenamiento de Modelos**: Proceso de fine-tuning
- **Actualización de Conocimiento**: Reentrenamiento con nuevos datos

### 🛠️ Módulo `utils/` - Utilidades
Herramientas auxiliares del sistema:
- **Logger**: Sistema de logging centralizado
- **Procesamiento de Texto**: Utilidades para manejo de texto
- **Utilidades de Hotel**: Funciones específicas del dominio

## 🚀 Archivo Principal: `main.py`

El archivo `main.py` es el punto de entrada principal que:
- **Valida el Sistema**: Verifica dependencias y configuración
- **Gestiona Modos**: Ejecuta diferentes modos (bot, entrenamiento, analytics)
- **Monitorea Recursos**: Controla uso de memoria y rendimiento
- **Proporciona Interfaz**: Menú interactivo para gestión del sistema

## 🔧 Características Principales

### 🎯 Arquitectura Modular
- **Separación de Responsabilidades**: Cada módulo tiene una función específica
- **Bajo Acoplamiento**: Los módulos se comunican a través de interfaces bien definidas
- **Alta Cohesión**: Funcionalidades relacionadas están agrupadas

### ⚡ Optimización de Rendimiento
- **Lazy Loading**: Carga de modelos solo cuando es necesario
- **Sistema de Cache**: Almacenamiento temporal de respuestas frecuentes
- **Gestión de Recursos**: Control eficiente de memoria y CPU

### 🔒 Seguridad y Robustez
- **Validación de Entrada**: Verificación de mensajes de usuarios
- **Manejo de Errores**: Gestión centralizada de excepciones
- **Rate Limiting**: Control de frecuencia de mensajes

### 📈 Escalabilidad
- **Configuración Flexible**: Ajustes mediante variables de entorno
- **Módulos Independientes**: Fácil adición de nuevas funcionalidades
- **Testing Automatizado**: Pruebas para garantizar calidad

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **LangChain**: Framework para aplicaciones de IA
- **FAISS**: Búsqueda vectorial eficiente
- **Transformers**: Modelos de Hugging Face
- **python-telegram-bot**: API de Telegram
- **PyTorch**: Framework de machine learning

## 📖 Documentación por Archivo

Cada archivo en la carpeta `src` tiene su propio README detallado que explica:
- **Propósito**: Qué hace el archivo
- **Estructura**: Cómo está organizado el código
- **Funcionalidades**: Características principales
- **Uso**: Cómo utilizar las funciones
- **Dependencias**: Qué otros módulos necesita

## 🚀 Inicio Rápido

Para ejecutar el sistema:

```bash
# Modo bot (predeterminado)
python src/main.py

# Modo entrenamiento
python src/main.py --mode train

# Modo analytics
python src/main.py --mode analytics

# Modo interactivo
python src/main.py --mode interactive
```

## 📝 Notas de Desarrollo

- **Convenciones**: Seguir PEP 8 para estilo de código
- **Documentación**: Mantener docstrings actualizados
- **Testing**: Añadir pruebas para nuevas funcionalidades
- **Logging**: Usar el logger centralizado para debugging 