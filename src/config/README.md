# ⚙️ Módulo `config/` - Configuración Centralizada del Sistema

## 🎯 ¿Por qué es Importante esta Carpeta?

La carpeta `config/` es **fundamental** para el funcionamiento del ChatBot de Hotelería por las siguientes razones:

### 🔑 **Punto Único de Configuración**
- **Centralización Total**: Todos los parámetros del sistema se gestionan desde un solo lugar
- **Evita Duplicación**: No hay configuraciones dispersas en diferentes archivos
- **Mantenimiento Simplificado**: Cambios de configuración sin tocar el código principal

### 🛡️ **Seguridad y Gestión de Secretos**
- **Tokens Seguros**: El token de Telegram se maneja de forma segura a través de variables de entorno
- **Separación de Datos Sensibles**: Las credenciales no están hardcodeadas en el código
- **Control de Acceso**: Diferentes configuraciones para desarrollo, testing y producción

### ⚡ **Flexibilidad y Escalabilidad**
- **Configuración por Entorno**: Diferentes settings para desarrollo, testing y producción
- **Fácil Personalización**: Cambios de configuración sin modificar código fuente
- **Escalabilidad**: Nuevos parámetros se agregan fácilmente sin afectar la arquitectura

### 🔧 **Gestión de Recursos**
- **Optimización de IA**: Control de modelos, cache y rendimiento
- **Gestión de Memoria**: Configuración de carga lazy y límites de concurrencia
- **Monitoreo**: Analytics y logging configurable

### 🚀 **Facilita el Desarrollo**
- **Onboarding Rápido**: Nuevos desarrolladores pueden configurar el sistema fácilmente
- **Debugging Simplificado**: Logging configurable para diferentes niveles de detalle
- **Testing Eficiente**: Configuraciones específicas para entornos de prueba

---

## 📋 Descripción General

El módulo `config/` centraliza toda la configuración del ChatBot de Hotelería. Este módulo gestiona variables de entorno, validación de configuración y proporciona acceso global a los settings del sistema.

## 🏗️ Estructura del Módulo

```
config/
├── __init__.py              # 📦 Inicialización del módulo
├── settings.py              # ⚙️ Configuración centralizada
└── README.md                # 📚 Documentación completa
```

## 📄 Documentación por Archivo

### ⚙️ `settings.py` - Configuración Centralizada

**Propósito**: Centraliza toda la configuración del sistema, cargando variables de entorno y proporcionando acceso global a los settings.

**Características Principales**:
- ✅ **Carga Automática**: Variables de entorno desde archivo `.env`
- ✅ **Validación Robusta**: Verificación de configuración requerida
- ✅ **Valores por Defecto**: Configuración sensible para casos no especificados
- ✅ **Patrón Singleton**: Una sola instancia global de configuración
- ✅ **Tipos Seguros**: Conversión automática de tipos de datos
- ✅ **Organización Lógica**: Configuración agrupada por categorías

**Estructura de Configuración**:

#### 🏢 Configuración de Empresa
```python
EMPRESA_NOMBRE = "Tu Hotel"
EMPRESA_DESCRIPCION = "Hotel de lujo con servicios premium"
```

#### 🤖 Configuración de Telegram
```python
TELEGRAM_TOKEN = "tu_token_de_telegram"
ENABLE_RICH_RESPONSES = True
ENABLE_EMOJI_FORMATTING = True
MAX_MESSAGE_LENGTH = 1000
MAX_MESSAGES_PER_MINUTE = 10
```

#### 🧠 Configuración de Modelos de IA
```python
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TEMPERATURE = 0.7
MAX_LENGTH = 300
MODELO_RESUMEN = "facebook/bart-large-cnn"
MODELO_GENERACION = "microsoft/DialoGPT-medium"
MODELO_EMBEDDINGS = "sentence-transformers/all-mpnet-base-v2"
```

#### 📁 Configuración de Directorios
```python
DOCUMENTOS_DIR = Path("documentos")
CONFIG_FILE = Path("config/entrenamiento_config.json")
ANALYTICS_FILE = Path("data/analytics.json")
FEEDBACK_FILE = Path("data/feedback.json")
USAGE_STATS_FILE = Path("data/usage_stats.json")
```

#### 💾 Configuración de Cache
```python
CACHE_DURATION_HOURS = 24
MAX_CACHE_SIZE = 1000
ENABLE_MODEL_CACHING = True
```

#### ⚡ Configuración de Recursos
```python
LAZY_LOAD_MODELS = True
MAX_CONCURRENT_REQUESTS = 10
```

#### 📊 Configuración de Analytics
```python
ENABLE_ANALYTICS = True
ANALYTICS_SAVE_INTERVAL = 10
```

#### 📝 Configuración de Logging
```python
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

**Uso Básico**:
```python
from config.settings import settings

# Acceder a configuración
token = settings.TELEGRAM_TOKEN
chunk_size = settings.CHUNK_SIZE
enable_analytics = settings.ENABLE_ANALYTICS

# Validar configuración
settings.validate()

# Verificar directorios
if not settings.DOCUMENTOS_DIR.exists():
    settings.DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)
```

**Métodos Principales**:

#### `validate()`
- **Propósito**: Valida que la configuración sea correcta
- **Funcionalidad**:
  - Verifica que el token de Telegram esté presente
  - Crea directorios necesarios si no existen
  - Valida valores críticos de configuración
  - Retorna True si todo está correcto

**Dependencias**:
- `python-dotenv`: Carga de variables de entorno
- `pathlib`: Manejo de rutas de archivos
- `os`: Acceso a variables de entorno

---

## 🔧 Características del Módulo

### 🎯 Centralización
- **Configuración Única**: Todos los settings en un solo lugar
- **Acceso Global**: Instancia singleton para acceso desde cualquier parte
- **Organización Lógica**: Configuración agrupada por categorías
- **Documentación Clara**: Cada setting tiene su propósito documentado

### 🔒 Validación y Seguridad
- **Validación Automática**: Verificación de configuración requerida
- **Valores por Defecto**: Configuración sensible para casos no especificados
- **Manejo de Errores**: Gestión robusta de configuración faltante
- **Tipos Seguros**: Conversión automática de tipos de datos

### ⚡ Flexibilidad
- **Variables de Entorno**: Configuración desde archivos .env
- **Configuración Opcional**: Valores por defecto para settings no críticos
- **Fácil Modificación**: Cambios sin modificar código
- **Entornos Múltiples**: Soporte para desarrollo, testing y producción

### 📊 Monitoreo
- **Logging Configurable**: Niveles de log ajustables
- **Analytics Opcional**: Sistema de métricas configurable
- **Debugging**: Información detallada para desarrollo
- **Auditoría**: Registro de cambios de configuración

## 🚀 Configuración del Sistema

### Archivo `.env` Requerido
```bash
# Configuración de Telegram (OBLIGATORIO)
TELEGRAM_TOKEN=tu_token_de_telegram_aqui

# Configuración de Empresa
EMPRESA_NOMBRE=Mi Hotel de Lujo
EMPRESA_DESCRIPCION=Hotel 5 estrellas con servicios premium

# Configuración de IA (Opcional - valores por defecto)
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TEMPERATURE=0.7
MAX_LENGTH=300

# Configuración de Rendimiento (Opcional)
LAZY_LOAD_MODELS=true
ENABLE_MODEL_CACHING=true
MAX_CONCURRENT_REQUESTS=10

# Configuración de Cache (Opcional)
CACHE_DURATION_HOURS=24
MAX_CACHE_SIZE=1000

# Configuración de Analytics (Opcional)
ENABLE_ANALYTICS=true
ANALYTICS_SAVE_INTERVAL=10

# Configuración de Logging (Opcional)
LOG_LEVEL=INFO
```

### Configuración por Entorno

#### 🛠️ Desarrollo
```bash
LOG_LEVEL=DEBUG
ENABLE_ANALYTICS=false
LAZY_LOAD_MODELS=false
```

#### 🚀 Producción
```bash
LOG_LEVEL=WARNING
ENABLE_ANALYTICS=true
LAZY_LOAD_MODELS=true
MAX_CONCURRENT_REQUESTS=20
```

#### 🧪 Testing
```bash
LOG_LEVEL=ERROR
ENABLE_ANALYTICS=false
USE_DUMMY_MODELS=true
```

## 📁 Estructura de Directorios

El módulo configura automáticamente la siguiente estructura:

```
proyecto/
├── src/data/                # � Bases de datos centralizadas
│   ├── hotel_content.db     # 🏨 Base de datos principal del hotel
│   ├── analytics.db         # 📈 Base de datos de análisis
│   └── models/              # 🤖 Modelos de IA entrenados
├── config/                  # ⚙️ Archivos de configuración
│   └── entrenamiento_config.json
├── logs/                    # 📝 Archivos de log
│   └── bot.log
└── .env                     # 🔐 Variables de entorno
```

**Cambios importantes**:
- ✅ **Eliminada carpeta `documentos/`**: El conocimiento se gestiona vía BD
- ✅ **Centralizada carpeta `src/data/`**: Todas las bases de datos en un lugar
- ✅ **Arquitectura moderna**: Basada en SQLite para mejor rendimiento

## 🔍 Validación de Configuración

### Verificación Automática
```python
from config.settings import settings

try:
    settings.validate()
    print("✅ Configuración válida")
except ValueError as e:
    print(f"❌ Error en configuración: {e}")
```

### Configuración Requerida
- **TELEGRAM_TOKEN**: Token del bot de Telegram (obligatorio)
- **DOCUMENTOS_DIR**: Directorio de documentos (se crea automáticamente)

### Configuración Opcional
- **Modelos de IA**: Valores por defecto optimizados
- **Cache**: Configuración de rendimiento
- **Analytics**: Sistema de métricas
- **Logging**: Niveles de debug

## 🚀 Inicio Rápido

```python
# Importar configuración
from config.settings import settings

# Validar configuración al inicio
settings.validate()

# Usar configuración en cualquier parte del código
bot_token = settings.TELEGRAM_TOKEN
chunk_size = settings.CHUNK_SIZE
enable_rich = settings.ENABLE_RICH_RESPONSES
```

## 🔄 Flujo de Trabajo

### 1. **Configuración Inicial**
```bash
# Crear archivo .env en la raíz del proyecto
cp configuracion.env .env
# Editar .env con tus valores
```

### 2. **Validación**
```python
from config.settings import settings
settings.validate()
```

### 3. **Uso en el Código**
```python
# En cualquier módulo
from config.settings import settings

# Acceder a configuración
token = settings.TELEGRAM_TOKEN
```

## 📝 Notas de Desarrollo

### ✅ **Buenas Prácticas**
- **Singleton**: Solo una instancia de Settings en toda la aplicación
- **Inmutabilidad**: La configuración no se modifica en tiempo de ejecución
- **Validación**: Siempre validar configuración al inicio
- **Logging**: Usar LOG_LEVEL para controlar verbosidad
- **Testing**: Usar variables de entorno específicas para tests
- **Documentación**: Mantener actualizada la documentación de cada setting

### ⚠️ **Consideraciones Importantes**
- **Seguridad**: Nunca committear el archivo `.env` al repositorio
- **Backup**: Mantener copias de seguridad de configuraciones críticas
- **Versionado**: Documentar cambios en configuración entre versiones
- **Testing**: Probar configuración en todos los entornos

### 🔧 **Mantenimiento**
- **Actualizaciones**: Revisar regularmente valores por defecto
- **Optimización**: Ajustar parámetros de rendimiento según uso
- **Monitoreo**: Revisar logs y analytics para ajustar configuración
- **Documentación**: Mantener README actualizado con nuevos parámetros

---

## 🎯 Resumen de Importancia

La carpeta `config/` es el **corazón de la configuración** del sistema porque:

1. **🔑 Centraliza** toda la configuración en un solo lugar
2. **🛡️ Protege** información sensible mediante variables de entorno
3. **⚡ Optimiza** el rendimiento con configuraciones inteligentes
4. **🔧 Facilita** el desarrollo y mantenimiento del sistema
5. **📊 Permite** monitoreo y analytics configurable
6. **🚀 Escala** fácilmente para diferentes entornos y necesidades

**Sin esta carpeta, el sistema no podría funcionar de manera segura, eficiente y mantenible.** 