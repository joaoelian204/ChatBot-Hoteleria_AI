# 📊 Módulo `analytics/` - Análisis y Métricas

## 📋 Descripción General

El módulo `analytics/` implementa un sistema completo de recolección, análisis y reporte de datos del ChatBot de Hotelería. Este módulo proporciona insights sobre el uso del sistema, rendimiento y comportamiento de los usuarios.

## 🏗️ Estructura del Módulo

```
analytics/
├── __init__.py              # 📦 Inicialización del módulo
└── manager.py               # 📊 Gestor principal de analytics
```

## 📄 Documentación por Archivo

### 📊 `manager.py` - Gestor Principal de Analytics

**Propósito**: Centraliza toda la funcionalidad de analytics, incluyendo recolección de datos, análisis y generación de reportes.

**Estructura**:
- **AnalyticsManager**: Clase principal para gestión de analytics
- **Recolección de Datos**: Captura de métricas en tiempo real
- **Almacenamiento**: Persistencia de datos en archivos JSON
- **Análisis**: Procesamiento y cálculo de estadísticas
- **Reportes**: Generación de informes automáticos

**Funcionalidades**:
- ✅ Recolección automática de métricas de uso
- ✅ Seguimiento de interacciones de usuarios
- ✅ Análisis de rendimiento del sistema
- ✅ Métricas de modelos de IA
- ✅ Estadísticas de cache y vectorstore
- ✅ Reportes automáticos y manuales
- ✅ Exportación de datos en múltiples formatos
- ✅ Limpieza automática de datos antiguos
- ✅ Alertas de rendimiento
- ✅ Dashboard de métricas en tiempo real

**Estructura de Clases**:
```python
class AnalyticsManager:
    def __init__(self):
        # Inicialización del sistema de analytics
    
    def record_interaction(self, user_id, message, response, response_time):
        # Registra una interacción de usuario
    
    def record_model_usage(self, model_name, usage_time, success):
        # Registra uso de modelos de IA
    
    def record_cache_hit(self, cache_type, hit_rate):
        # Registra estadísticas de cache
    
    def generate_report(self, report_type="daily"):
        # Genera reportes automáticos
    
    def get_system_stats(self):
        # Obtiene estadísticas del sistema
    
    def save_data(self):
        # Guarda datos en archivos JSON
```

**Métricas Recolectadas**:

#### 📈 Métricas de Usuario
- **Interacciones**: Número de mensajes por usuario
- **Tiempo de Respuesta**: Latencia del sistema
- **Satisfacción**: Feedback implícito (repetición de preguntas)
- **Patrones de Uso**: Horarios y frecuencia de uso
- **Comandos Más Usados**: Popularidad de funcionalidades

#### 🤖 Métricas de IA
- **Uso de Modelos**: Frecuencia de uso de cada modelo
- **Tiempo de Procesamiento**: Latencia de modelos
- **Tasa de Éxito**: Porcentaje de respuestas exitosas
- **Fallbacks**: Uso de respuestas de respaldo
- **Calidad de Respuestas**: Evaluación de relevancia

#### ⚡ Métricas de Rendimiento
- **Cache Hit Rate**: Efectividad del sistema de cache
- **Uso de Memoria**: Consumo de recursos del sistema
- **Tiempo de Carga**: Velocidad de inicialización
- **Errores**: Frecuencia y tipos de errores
- **Concurrencia**: Número de usuarios simultáneos

#### 📊 Métricas de Negocio
- **Consultas por Categoría**: Habitaciones, restaurantes, etc.
- **Horarios Pico**: Momentos de mayor actividad
- **Retención**: Usuarios recurrentes
- **Conversión**: Consultas que llevan a acciones
- **Satisfacción**: Métricas de calidad de servicio

**Uso**:
```python
from analytics.manager import analytics_manager

# Registrar interacción de usuario
analytics_manager.record_interaction(
    user_id=12345,
    message="¿Qué habitaciones tienen?",
    response="Tenemos suites disponibles...",
    response_time=1.2
)

# Registrar uso de modelo
analytics_manager.record_model_usage(
    model_name="generator",
    usage_time=0.8,
    success=True
)

# Generar reporte
report = analytics_manager.generate_report("daily")

# Obtener estadísticas del sistema
stats = analytics_manager.get_system_stats()
```

**Funciones Principales**:

#### `record_interaction(user_id, message, response, response_time)`
- **Propósito**: Registra una interacción completa de usuario
- **Parámetros**:
  - `user_id`: ID único del usuario
  - `message`: Mensaje enviado por el usuario
  - `response`: Respuesta del bot
  - `response_time`: Tiempo de respuesta en segundos
- **Funcionalidad**:
  - Almacena datos de la interacción
  - Calcula métricas de calidad
  - Actualiza contadores de uso
  - Detecta patrones de comportamiento

#### `record_model_usage(model_name, usage_time, success)`
- **Propósito**: Registra el uso de modelos de IA
- **Parámetros**:
  - `model_name`: Nombre del modelo utilizado
  - `usage_time`: Tiempo de procesamiento
  - `success`: Si el modelo funcionó correctamente
- **Funcionalidad**:
  - Rastrea rendimiento de modelos
  - Identifica modelos problemáticos
  - Optimiza carga de recursos
  - Planifica mantenimiento

#### `generate_report(report_type="daily")`
- **Propósito**: Genera reportes automáticos
- **Parámetros**:
  - `report_type`: Tipo de reporte (daily, weekly, monthly)
- **Funcionalidad**:
  - Agrega datos por período
  - Calcula tendencias
  - Identifica anomalías
  - Genera visualizaciones

#### `get_system_stats()`
- **Propósito**: Obtiene estadísticas en tiempo real
- **Retorna**: Diccionario con métricas actuales
- **Funcionalidad**:
  - Métricas de uso actual
  - Estado del sistema
  - Rendimiento en tiempo real
  - Alertas de problemas

#### `save_data()`
- **Propósito**: Persiste datos en archivos JSON
- **Funcionalidad**:
  - Guarda datos en formato estructurado
  - Mantiene historial completo
  - Permite análisis offline
  - Facilita backup y restauración

**Dependencias**:
- `json`: Serialización de datos
- `datetime`: Manejo de fechas y tiempos
- `pathlib`: Manejo de rutas de archivos
- `config.settings`: Configuración del sistema
- `utils.logger`: Sistema de logging

---

## 🔧 Características del Módulo

### 📊 Recolección Automática
- **Métricas en Tiempo Real**: Captura automática de datos
- **Sin Interferencia**: No afecta el rendimiento del sistema
- **Datos Completos**: Registro de todas las interacciones
- **Contexto Rico**: Información detallada de cada evento

### 📈 Análisis Inteligente
- **Tendencias**: Identificación de patrones temporales
- **Anomalías**: Detección de comportamientos inusuales
- **Correlaciones**: Relaciones entre diferentes métricas
- **Predicciones**: Estimaciones basadas en datos históricos

### 📋 Reportes Automáticos
- **Reportes Diarios**: Resumen diario de actividad
- **Reportes Semanales**: Análisis de tendencias semanales
- **Reportes Mensuales**: Resumen ejecutivo mensual
- **Alertas**: Notificaciones de problemas críticos

### 💾 Persistencia de Datos
- **Almacenamiento JSON**: Formato legible y portable
- **Backup Automático**: Copias de seguridad regulares
- **Limpieza Inteligente**: Eliminación de datos antiguos
- **Integridad**: Verificación de consistencia de datos

## 🚀 Configuración del Sistema

### Variables de Entorno
```bash
# Habilitar Analytics
ENABLE_ANALYTICS=true

# Configuración de Guardado
ANALYTICS_SAVE_INTERVAL=10

# Configuración de Limpieza
ANALYTICS_RETENTION_DAYS=90

# Configuración de Alertas
ANALYTICS_ALERT_THRESHOLD=0.8
```

### Configuración por Entorno

#### Desarrollo
```bash
ENABLE_ANALYTICS=true
ANALYTICS_SAVE_INTERVAL=5
ANALYTICS_RETENTION_DAYS=7
```

#### Producción
```bash
ENABLE_ANALYTICS=true
ANALYTICS_SAVE_INTERVAL=30
ANALYTICS_RETENTION_DAYS=365
```

## 📁 Estructura de Datos

### Archivos de Analytics
```
data/
├── analytics.json           # 📊 Datos principales de analytics
├── user_interactions.json   # 👥 Interacciones de usuarios
├── model_usage.json         # 🤖 Uso de modelos de IA
├── performance_metrics.json # ⚡ Métricas de rendimiento
├── business_metrics.json    # 💼 Métricas de negocio
└── reports/                 # 📋 Reportes generados
    ├── daily/
    ├── weekly/
    └── monthly/
```

### Estructura de Datos JSON
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "user_id": 12345,
  "interaction_type": "message",
  "message": "¿Qué habitaciones tienen?",
  "response": "Tenemos suites disponibles...",
  "response_time": 1.2,
  "model_used": "generator",
  "cache_hit": false,
  "success": true,
  "metadata": {
    "user_agent": "TelegramBot",
    "session_id": "abc123",
    "intent_detected": "habitaciones"
  }
}
```

## 📊 Tipos de Reportes

### 📅 Reporte Diario
- **Resumen**: Actividad del día
- **Métricas Clave**: Usuarios únicos, interacciones totales
- **Rendimiento**: Tiempo de respuesta promedio
- **Problemas**: Errores y fallbacks

### 📊 Reporte Semanal
- **Tendencias**: Comparación con semanas anteriores
- **Patrones**: Horarios de mayor actividad
- **Calidad**: Satisfacción de usuarios
- **Optimización**: Oportunidades de mejora

### 📈 Reporte Mensual
- **Crecimiento**: Evolución del uso del sistema
- **ROI**: Retorno de inversión
- **Escalabilidad**: Capacidad del sistema
- **Planificación**: Recomendaciones futuras

## 🚀 Inicio Rápido

```python
# Importar analytics manager
from analytics.manager import analytics_manager

# Verificar si analytics está habilitado
if analytics_manager.is_enabled():
    # Registrar interacción
    analytics_manager.record_interaction(
        user_id=12345,
        message="Consulta de usuario",
        response="Respuesta del bot",
        response_time=1.0
    )
    
    # Generar reporte
    report = analytics_manager.generate_report("daily")
    print(f"Reporte generado: {report}")
```

## 📝 Notas de Desarrollo

- **Privacidad**: Los datos se anonimizan para proteger usuarios
- **Rendimiento**: Analytics no debe afectar la velocidad del bot
- **Almacenamiento**: Monitorear el tamaño de archivos de datos
- **Backup**: Realizar copias de seguridad regulares
- **Limpieza**: Configurar retención de datos apropiada
- **Testing**: Verificar que analytics funcione en todos los entornos 