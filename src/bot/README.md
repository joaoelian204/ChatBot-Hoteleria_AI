# 🤖 Módulo `bot/` - Bot de Telegram

## 📋 Descripción General

El módulo `bot/` contiene toda la lógica relacionada con el bot de Telegram del ChatBot de Hotelería. Este módulo implementa la interfaz de usuario, gestión de comandos, procesamiento de mensajes y la integración con la API de Telegram.

## 🏗️ Estructura del Módulo

```
bot/
├── __init__.py              # 📦 Inicialización del módulo
├── bot_main.py              # 🚀 Bot principal de Telegram
└── callbacks.py             # 🔄 Manejo de callbacks y comandos
```

## 📄 Documentación por Archivo

### 🚀 `bot_main.py` - Bot Principal de Telegram

**Propósito**: Implementa la clase principal del bot de Telegram con todas las funcionalidades de interacción con usuarios.

**Estructura**:
- **HoteleriaBot**: Clase principal del bot
- **Gestión de Handlers**: Configuración de comandos y mensajes
- **Contexto de Usuario**: Persistencia de información de usuarios
- **Respuestas Enriquecidas**: Botones y formato avanzado
- **Métricas y Analytics**: Seguimiento de interacciones

**Funcionalidades**:
- ✅ Configuración automática de handlers de Telegram
- ✅ Gestión de comandos básicos (/start, /help, /stats)
- ✅ Comandos específicos del hotel (/rooms, /restaurants, /amenities, /contact)
- ✅ Procesamiento de mensajes de texto con IA
- ✅ Sistema de botones interactivos (InlineKeyboard)
- ✅ Respuestas enriquecidas con emojis y formato
- ✅ Persistencia de contexto de usuario
- ✅ Rate limiting para prevenir spam
- ✅ Métricas de rendimiento y analytics
- ✅ Gestión de errores centralizada
- ✅ Comando de limpieza de cache (/clear_cache)

**Estructura de Clases**:
```python
class HoteleriaBot:
    def __init__(self):
        # Inicialización del bot y configuración
    
    def _configurar_handlers(self):
        # Configuración de todos los handlers
    
    def _handle_stats(self, update, context):
        # Manejo del comando /stats
    
    def _get_user_context(self, user_id):
        # Gestión de contexto de usuario
    
    def _create_rich_response(self, text, intent):
        # Creación de respuestas enriquecidas
    
    def run(self):
        # Ejecución principal del bot
```

**Uso**:
```python
from bot.bot_main import HoteleriaBot

# Crear instancia del bot
bot = HoteleriaBot()

# Ejecutar el bot
bot.run()
```

**Comandos Disponibles**:
- `/start` - Inicio del bot y bienvenida
- `/help` - Ayuda y comandos disponibles
- `/stats` - Estadísticas del sistema
- `/clear_cache` - Limpiar cache de respuestas
- `/rooms` - Información sobre habitaciones
- `/restaurants` - Información sobre restaurantes
- `/amenities` - Información sobre amenidades
- `/contact` - Información de contacto

**Dependencias**:
- `python-telegram-bot`: API de Telegram
- `ai.models`: Modelos de IA para respuestas
- `ai.vectorstore`: Base de conocimiento
- `ai.cache`: Sistema de cache
- `analytics.manager`: Sistema de analytics
- `config.settings`: Configuración del sistema
- `utils.logger`: Sistema de logging

---

### 🔄 `callbacks.py` - Manejo de Callbacks y Comandos

**Propósito**: Contiene todas las funciones de callback para manejar comandos, mensajes y interacciones del bot.

**Estructura**:
- **Handlers de Comandos**: Funciones para comandos básicos
- **Handlers de Mensajes**: Procesamiento de mensajes de texto
- **Handlers de Callbacks**: Manejo de botones interactivos
- **Handlers de Errores**: Gestión de excepciones
- **Funciones Auxiliares**: Utilidades para respuestas

**Funcionalidades**:
- ✅ `handle_start()` - Comando de inicio y bienvenida
- ✅ `handle_help()` - Comando de ayuda con información detallada
- ✅ `handle_message()` - Procesamiento principal de mensajes
- ✅ `handle_callback_query()` - Manejo de botones interactivos
- ✅ `handle_error()` - Gestión centralizada de errores
- ✅ Funciones auxiliares para formateo de respuestas
- ✅ Integración con sistema de IA para respuestas
- ✅ Validación de mensajes y rate limiting
- ✅ Logging detallado de interacciones

**Funciones Principales**:

#### `handle_start(update, context)`
- **Propósito**: Maneja el comando `/start`
- **Funcionalidad**: 
  - Envía mensaje de bienvenida personalizado
  - Muestra información básica del hotel
  - Proporciona botones de navegación rápida
  - Registra nueva interacción de usuario

#### `handle_help(update, context)`
- **Propósito**: Maneja el comando `/help`
- **Funcionalidad**:
  - Lista todos los comandos disponibles
  - Explica funcionalidades del bot
  - Proporciona ejemplos de uso
  - Incluye información de contacto

#### `handle_message(update, context)`
- **Propósito**: Procesa mensajes de texto de usuarios
- **Funcionalidad**:
  - Valida entrada del usuario
  - Detecta intención del mensaje
  - Busca contexto relevante en base de conocimiento
  - Genera respuesta con IA
  - Aplica formato y emojis
  - Registra métricas de uso

#### `handle_callback_query(update, context)`
- **Propósito**: Maneja clicks en botones interactivos
- **Funcionalidad**:
  - Procesa diferentes tipos de botones
  - Navega entre secciones del hotel
  - Proporciona información específica
  - Actualiza mensajes existentes

#### `handle_error(update, context)`
- **Propósito**: Maneja errores del bot
- **Funcionalidad**:
  - Captura excepciones no manejadas
  - Registra errores en logs
  - Envía mensaje de error amigable al usuario
  - Notifica a administradores si es necesario

**Uso**:
```python
from bot.callbacks import handle_start, handle_message, handle_error

# Los handlers se registran automáticamente en bot_main.py
# No es necesario llamarlos directamente
```

**Dependencias**:
- `ai.models`: Modelos de IA
- `ai.vectorstore`: Base de conocimiento
- `ai.intent_detector`: Detección de intenciones
- `ai.text_generator`: Generación de respuestas
- `ai.cache`: Sistema de cache
- `analytics.manager`: Sistema de analytics
- `utils.text_processor`: Procesamiento de texto
- `utils.logger`: Sistema de logging

---

## 🔧 Características del Módulo

### 🎯 Interfaz de Usuario Avanzada
- **Botones Interactivos**: Navegación fácil con InlineKeyboard
- **Respuestas Enriquecidas**: Formato con emojis y Markdown
- **Navegación Contextual**: Botones adaptados al contexto
- **Experiencia Fluida**: Transiciones suaves entre secciones

### 🔒 Seguridad y Validación
- **Rate Limiting**: Control de frecuencia de mensajes
- **Validación de Entrada**: Verificación de mensajes de usuarios
- **Sanitización**: Limpieza de texto de entrada
- **Manejo de Errores**: Gestión robusta de excepciones

### 📊 Analytics y Métricas
- **Seguimiento de Usuarios**: Registro de interacciones
- **Métricas de Rendimiento**: Tiempo de respuesta y uso
- **Análisis de Comportamiento**: Patrones de uso
- **Reportes Automáticos**: Estadísticas del sistema

### ⚡ Optimización de Rendimiento
- **Cache de Respuestas**: Almacenamiento temporal
- **Procesamiento Asíncrono**: Respuestas no bloqueantes
- **Gestión de Memoria**: Control eficiente de recursos
- **Lazy Loading**: Carga de modelos bajo demanda

## 🚀 Configuración del Bot

### Variables de Entorno Requeridas
```bash
TELEGRAM_TOKEN=tu_token_de_telegram
ENABLE_RICH_RESPONSES=true
ENABLE_EMOJI_FORMATTING=true
MAX_MESSAGES_PER_MINUTE=10
```

### Configuración Opcional
```bash
ENABLE_ANALYTICS=true
ANALYTICS_SAVE_INTERVAL=10
LOG_LEVEL=INFO
```

## 📱 Funcionalidades del Bot

### 🏨 Información del Hotel
- **Habitaciones**: Tipos, precios, disponibilidad
- **Restaurantes**: Menús, horarios, especialidades
- **Amenidades**: Servicios, instalaciones, actividades
- **Contacto**: Información de reservas y atención

### 🎯 Comandos Especializados
- **Búsqueda Inteligente**: Respuestas basadas en IA
- **Navegación Contextual**: Botones adaptativos
- **Información Personalizada**: Respuestas según contexto
- **Soporte Multilingüe**: Preparado para múltiples idiomas

### 📊 Funciones Administrativas
- **Estadísticas del Sistema**: Métricas de rendimiento
- **Gestión de Cache**: Limpieza y monitoreo
- **Logs Detallados**: Seguimiento de actividad
- **Monitoreo de Recursos**: Uso de memoria y CPU

## 🚀 Inicio Rápido

```python
# Ejecutar el bot directamente
python src/main.py --mode bot

# O desde el código
from bot.bot_main import HoteleriaBot
bot = HoteleriaBot()
bot.run()
```

## 📝 Notas de Desarrollo

- **Handlers**: Todos los handlers se registran automáticamente
- **Contexto**: El contexto de usuario se mantiene por sesión
- **Errores**: Todos los errores se capturan y registran
- **Logging**: Todas las interacciones se registran para debugging
- **Testing**: Cada función tiene pruebas unitarias
- **Documentación**: Mantener docstrings actualizados 