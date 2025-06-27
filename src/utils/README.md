# 🛠️ Módulo `utils/` - Utilidades del Sistema

## 📋 Descripción General

El módulo `utils/` contiene herramientas auxiliares y utilidades que son utilizadas por todo el sistema del ChatBot de Hotelería. Este módulo proporciona funcionalidades comunes como logging, procesamiento de texto y utilidades específicas del dominio hotelero.

## 🏗️ Estructura del Módulo

```
utils/
├── __init__.py              # 📦 Inicialización del módulo
├── logger.py                # 📝 Sistema de logging centralizado
├── text_processor.py        # ✍️ Procesamiento y validación de texto
└── hotel_utils.py           # 🏨 Utilidades específicas del hotel
```

## 📄 Documentación por Archivo

### 📝 `logger.py` - Sistema de Logging Centralizado

**Propósito**: Proporciona un sistema de logging unificado y configurable para todo el proyecto.

**Estructura**:
- **setup_logger()**: Función principal para configurar loggers
- **Logger Global**: Instancia singleton del logger principal
- **Handlers Múltiples**: Logging a consola y archivo
- **Configuración Centralizada**: Uso de settings del sistema

**Funcionalidades**:
- ✅ Configuración automática de loggers
- ✅ Logging simultáneo a consola y archivo
- ✅ Formato personalizable de mensajes
- ✅ Niveles de log configurables
- ✅ Creación automática de directorio de logs
- ✅ Codificación UTF-8 para caracteres especiales
- ✅ Prevención de configuración múltiple
- ✅ Logger global accesible desde cualquier módulo

**Estructura de Configuración**:
```python
def setup_logger(name: str = None) -> logging.Logger:
    # Configuración de nivel de log
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Formato de mensajes
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    
    # Handler para archivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    
    return logger
```

**Uso**:
```python
from utils.logger import logger

# Logging básico
logger.info("✅ Sistema iniciado correctamente")
logger.warning("⚠️ Configuración no encontrada")
logger.error("❌ Error en el procesamiento")
logger.debug("🔍 Información de debug")

# Logger específico para un módulo
from utils.logger import setup_logger
module_logger = setup_logger('mi_modulo')
module_logger.info("Mensaje específico del módulo")
```

**Configuración**:
- **LOG_LEVEL**: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **LOG_FORMAT**: Formato de mensajes con timestamp y nivel
- **Archivo de Log**: `logs/bot.log` en la raíz del proyecto
- **Codificación**: UTF-8 para soporte de caracteres especiales

**Dependencias**:
- `logging`: Módulo estándar de Python
- `config.settings`: Configuración del sistema
- `pathlib`: Manejo de rutas de archivos

---

### ✍️ `text_processor.py` - Procesamiento y Validación de Texto

**Propósito**: Proporciona funciones para procesar, validar y sanitizar texto de entrada de usuarios.

**Estructura**:
- **sanitize_text()**: Limpieza y normalización de texto
- **validate_message()**: Validación de mensajes de usuarios
- **normalize_text()**: Normalización de formato
- **extract_keywords()**: Extracción de palabras clave
- **clean_html()**: Limpieza de HTML y formato

**Funcionalidades**:
- ✅ Sanitización de texto de entrada
- ✅ Validación de longitud y contenido
- ✅ Normalización de caracteres especiales
- ✅ Eliminación de HTML y formato no deseado
- ✅ Extracción de palabras clave relevantes
- ✅ Detección de spam y contenido inapropiado
- ✅ Normalización de espacios y puntuación
- ✅ Validación de caracteres permitidos

**Funciones Principales**:

#### `sanitize_text(text: str) -> str`
- **Propósito**: Limpia y normaliza texto de entrada
- **Funcionalidad**:
  - Elimina caracteres especiales no deseados
  - Normaliza espacios múltiples
  - Convierte a minúsculas si es necesario
  - Elimina HTML y formato
  - Retorna texto limpio y normalizado

#### `validate_message(text: str, max_length: int = 1000) -> bool`
- **Propósito**: Valida que un mensaje cumpla con los requisitos
- **Funcionalidad**:
  - Verifica longitud máxima
  - Valida caracteres permitidos
  - Detecta contenido inapropiado
  - Verifica que no esté vacío
  - Retorna True si es válido

#### `normalize_text(text: str) -> str`
- **Propósito**: Normaliza el formato del texto
- **Funcionalidad**:
  - Normaliza espacios y saltos de línea
  - Corrige puntuación
  - Elimina caracteres de control
  - Mantiene estructura legible

#### `extract_keywords(text: str) -> List[str]`
- **Propósito**: Extrae palabras clave relevantes
- **Funcionalidad**:
  - Identifica palabras importantes
  - Filtra palabras comunes (stop words)
  - Retorna lista de palabras clave
  - Útil para búsquedas y análisis

**Uso**:
```python
from utils.text_processor import sanitize_text, validate_message

# Sanitizar texto de entrada
clean_text = sanitize_text("  Hola! ¿Qué   habitaciones   tienen?  ")
# Resultado: "Hola! ¿Qué habitaciones tienen?"

# Validar mensaje
is_valid = validate_message("Consulta sobre habitaciones", max_length=100)
# Resultado: True

# Normalizar texto
normalized = normalize_text("texto\ncon\nsaltos\nde\nlínea")
# Resultado: "texto con saltos de línea"
```

**Dependencias**:
- `re`: Expresiones regulares
- `html`: Procesamiento de HTML
- `unicodedata`: Normalización Unicode

---

### 🏨 `hotel_utils.py` - Utilidades Específicas del Hotel

**Propósito**: Contiene funciones específicas del dominio hotelero para procesar información relacionada con hoteles, habitaciones, servicios y reservas.

**Estructura**:
- **parse_room_info()**: Análisis de información de habitaciones
- **extract_prices()**: Extracción de precios de texto
- **validate_dates()**: Validación de fechas de reserva
- **format_currency()**: Formateo de moneda
- **parse_amenities()**: Análisis de amenidades
- **validate_contact()**: Validación de información de contacto

**Funcionalidades**:
- ✅ Análisis de información de habitaciones
- ✅ Extracción y validación de precios
- ✅ Validación de fechas de reserva
- ✅ Formateo de moneda y precios
- ✅ Análisis de amenidades y servicios
- ✅ Validación de información de contacto
- ✅ Conversión de unidades (moneda, tiempo)
- ✅ Generación de resúmenes de servicios

**Funciones Principales**:

#### `parse_room_info(text: str) -> dict`
- **Propósito**: Extrae información estructurada de habitaciones
- **Funcionalidad**:
  - Identifica tipo de habitación
  - Extrae capacidad y características
  - Detecta precios y disponibilidad
  - Retorna diccionario estructurado

#### `extract_prices(text: str) -> List[float]`
- **Propósito**: Extrae precios de texto
- **Funcionalidad**:
  - Identifica patrones de precios
  - Maneja diferentes formatos de moneda
  - Convierte a valores numéricos
  - Retorna lista de precios encontrados

#### `validate_dates(date_text: str) -> bool`
- **Propósito**: Valida fechas de reserva
- **Funcionalidad**:
  - Verifica formato de fecha
  - Valida que sea fecha futura
  - Comprueba disponibilidad de rango
  - Retorna True si es válida

#### `format_currency(amount: float, currency: str = "USD") -> str`
- **Propósito**: Formatea cantidades monetarias
- **Funcionalidad**:
  - Aplica formato de moneda
  - Maneja diferentes divisas
  - Incluye símbolos de moneda
  - Retorna string formateado

#### `parse_amenities(text: str) -> List[str]`
- **Propósito**: Extrae lista de amenidades
- **Funcionalidad**:
  - Identifica servicios mencionados
  - Categoriza amenidades
  - Normaliza nombres
  - Retorna lista estructurada

#### `validate_contact(contact_info: str) -> bool`
- **Propósito**: Valida información de contacto
- **Funcionalidad**:
  - Verifica formato de email
  - Valida números de teléfono
  - Comprueba direcciones
  - Retorna True si es válida

**Uso**:
```python
from utils.hotel_utils import parse_room_info, extract_prices, format_currency

# Analizar información de habitación
room_info = parse_room_info("Suite de lujo con vista al mar, 2 personas, $200/noche")
# Resultado: {
#     'type': 'Suite de lujo',
#     'capacity': 2,
#     'view': 'mar',
#     'price': 200,
#     'currency': 'USD'
# }

# Extraer precios
prices = extract_prices("Habitación desde $150 hasta $300 por noche")
# Resultado: [150.0, 300.0]

# Formatear moneda
formatted = format_currency(250.50, "USD")
# Resultado: "$250.50"
```

**Dependencias**:
- `re`: Expresiones regulares
- `datetime`: Manejo de fechas
- `locale`: Formateo de moneda

---

## 🔧 Características del Módulo

### 🎯 Reutilización
- **Funciones Comunes**: Utilidades utilizadas por múltiples módulos
- **Interfaces Consistentes**: APIs uniformes para funcionalidades similares
- **Configuración Centralizada**: Uso de settings del sistema
- **Documentación Clara**: Cada función tiene su propósito documentado

### 🔒 Robustez
- **Validación de Entrada**: Verificación de datos de entrada
- **Manejo de Errores**: Gestión de casos edge
- **Sanitización**: Limpieza de datos no confiables
- **Fallbacks**: Valores por defecto para casos de error

### ⚡ Rendimiento
- **Funciones Optimizadas**: Código eficiente para operaciones comunes
- **Cache Interno**: Almacenamiento temporal de resultados
- **Lazy Loading**: Carga bajo demanda de recursos pesados
- **Procesamiento Batch**: Operaciones en lotes cuando es posible

### 📊 Monitoreo
- **Logging Detallado**: Registro de operaciones importantes
- **Métricas de Uso**: Seguimiento de funciones más utilizadas
- **Debugging**: Información detallada para desarrollo
- **Auditoría**: Registro de cambios y operaciones críticas

## 🚀 Configuración del Sistema

### Variables de Entorno Relacionadas
```bash
# Configuración de Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Configuración de Procesamiento de Texto
MAX_MESSAGE_LENGTH=1000
ENABLE_TEXT_SANITIZATION=true
ENABLE_SPAM_DETECTION=true

# Configuración de Hotel
DEFAULT_CURRENCY=USD
DEFAULT_TIMEZONE=UTC
ENABLE_DATE_VALIDATION=true
```

### Configuración por Entorno

#### Desarrollo
```bash
LOG_LEVEL=DEBUG
ENABLE_TEXT_SANITIZATION=false
ENABLE_SPAM_DETECTION=false
```

#### Producción
```bash
LOG_LEVEL=WARNING
ENABLE_TEXT_SANITIZATION=true
ENABLE_SPAM_DETECTION=true
```

## 📁 Estructura de Archivos

```
proyecto/
├── logs/                    # 📝 Archivos de log
│   └── bot.log
├── utils/                   # 🛠️ Módulo de utilidades
│   ├── __init__.py
│   ├── logger.py
│   ├── text_processor.py
│   └── hotel_utils.py
└── .env                     # 🔐 Variables de entorno
```

## 🚀 Inicio Rápido

```python
# Importar utilidades principales
from utils.logger import logger
from utils.text_processor import sanitize_text, validate_message
from utils.hotel_utils import parse_room_info, format_currency

# Configurar logging
logger.info("🛠️ Utilidades inicializadas")

# Procesar texto de usuario
user_input = "  Hola! ¿Qué   habitaciones   tienen?  "
clean_input = sanitize_text(user_input)

if validate_message(clean_input):
    logger.info(f"✅ Mensaje válido: {clean_input}")
else:
    logger.warning("⚠️ Mensaje inválido")
```

## 📝 Notas de Desarrollo

- **Logging**: Usar el logger centralizado para todas las operaciones
- **Validación**: Siempre validar entrada antes de procesar
- **Sanitización**: Limpiar texto de usuarios antes de usar
- **Testing**: Cada función tiene pruebas unitarias
- **Documentación**: Mantener docstrings actualizados
- **Performance**: Optimizar funciones frecuentemente utilizadas 