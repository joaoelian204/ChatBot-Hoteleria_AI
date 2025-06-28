# 🗄️ Módulo `database/` - Capa de Acceso a Datos

## 📋 Descripción General

El módulo `database/` implementa una capa profesional de acceso a datos para el ChatBot de Hotelería. Este módulo centraliza toda la interacción con las bases de datos SQLite, proporcionando abstracciones robustas, patrón Repository y adaptadores especializados.

## 🏗️ Estructura del Módulo

```
database/
├── __init__.py              # 📦 Inicialización del módulo
├── connection.py            # 🔌 Gestión de conexiones a BD
├── repository.py            # 📚 Patrón Repository para entidades
├── adapter.py               # 🔄 Adaptadores especializados por módulo
└── fallback_main.py         # 🔀 Funciones de compatibilidad y fallback
```

## 📄 Documentación por Archivo

### 🔌 `connection.py` - Gestión de Conexiones

**Propósito**: Centraliza y optimiza las conexiones a las bases de datos SQLite.

**Características**:

- ✅ **Pool de conexiones**: Reutilización eficiente de conexiones
- ✅ **Gestión automática**: Cierre automático y limpieza de recursos
- ✅ **Rutas centralizadas**: Todas las BD en `src/data/`
- ✅ **Validación**: Verificación de integridad de BD al conectar
- ✅ **Thread-safe**: Seguro para uso en aplicaciones concurrentes

**Estructura**:

```python
class DatabaseConnection:
    def __init__(self):
        # Rutas centralizadas en src/data/

    def get_connection(self, db_name: str):
        # Obtiene conexión del pool

    def execute_query(self, query: str, params: tuple):
        # Ejecuta consultas con parámetros seguros
```

### 📚 `repository.py` - Patrón Repository

**Propósito**: Implementa el patrón Repository para acceso estructurado a entidades de negocio.

**Características**:

- ✅ **Abstracción de BD**: Oculta complejidad de SQL al resto del sistema
- ✅ **CRUD completo**: Create, Read, Update, Delete para todas las entidades
- ✅ **Consultas tipadas**: Métodos específicos con tipos Python
- ✅ **Validación de datos**: Validación automática en escritura
- ✅ **Transacciones**: Soporte para operaciones atómicas

**Estructura**:

```python
class HotelRepository:
    def get_all_rooms(self) -> List[Room]:
        # Obtiene todas las habitaciones

    def get_room_by_type(self, room_type: str) -> Room:
        # Busca habitación por tipo

    def get_amenities(self) -> List[Amenity]:
        # Obtiene amenidades del hotel
```

### 🔄 `adapter.py` - Adaptadores Especializados

**Propósito**: Proporciona adaptadores especializados para diferentes módulos del sistema.

**Características**:

- ✅ **Adaptador para VectorStore**: Optimizado para búsquedas semánticas
- ✅ **Adaptador para Analytics**: Métricas y análisis de datos
- ✅ **Adaptador para Bot**: Consultas específicas del chatbot
- ✅ **Cache integrado**: Optimización de consultas frecuentes
- ✅ **Formato específico**: Datos adaptados a cada módulo

**Estructura**:

```python
class DatabaseVectorStoreAdapter:
    def get_all_documents_for_vectorstore(self):
        # Datos optimizados para vectorstore

class DatabaseAnalyticsAdapter:
    def record_interaction(self, user_id, message, response):
        # Registro de interacciones

class DatabaseBotAdapter:
    def get_quick_responses(self):
        # Respuestas rápidas para el bot
```

### `fallback_main.py` - Funciones de Compatibilidad

**Propósito**: Proporciona funciones de compatibilidad para mantener la interfaz del sistema de testing y fallback.

**Características**:

- ✅ **Compatibilidad**: Mantiene funciones esperadas por el sistema de testing
- ✅ **Proxy a BD**: Redirige llamadas al repository apropiado
- ✅ **Funciones utility**: Utilidades específicas del dominio hotelero
- ✅ **Interfaz limpia**: API simple para el resto del sistema
- ✅ **Logging integrado**: Trazabilidad de operaciones

**Funciones Principales**:

```python
def get_cheapest_room_info() -> str:
    # Obtiene información de habitación más económica

def get_most_expensive_room_info() -> str:
    # Obtiene información de habitación más cara

def normalize_text(text: str) -> str:
    # Normaliza texto para búsquedas

def get_hotel_contact_info() -> str:
    # Información de contacto del hotel

def get_room_availability(room_type: str) -> str:
    # Disponibilidad de habitaciones
```

## 🔧 Configuración y Uso

### **Configuración de Rutas**

Las bases de datos están centralizadas en `src/data/`:

```python
# En connection.py
DATABASE_PATHS = {
    'hotel_content': 'src/data/hotel_content.db',
    'analytics': 'src/data/analytics.db'
}
```

### **Uso Básico**

```python
from database.repository import HotelRepository
from database.adapter import db_vectorstore_adapter

# Usar repository para operaciones CRUD
repo = HotelRepository()
rooms = repo.get_all_rooms()

# Usar adapter para casos específicos
documents = db_vectorstore_adapter.get_all_documents_for_vectorstore()
```

## 🚀 Ventajas de esta Arquitectura

### **🎯 Separación de Responsabilidades**

- **Repository**: Lógica de negocio y entidades
- **Adapter**: Adaptación a necesidades específicas
- **Connection**: Gestión técnica de conexiones
- **Fallback**: Funciones de compatibilidad y testing

### **⚡ Rendimiento Optimizado**

- **Pool de conexiones**: Reutilización eficiente
- **Cache inteligente**: Reducción de consultas repetitivas
- **Consultas optimizadas**: SQL específico por caso de uso
- **Lazy loading**: Carga bajo demanda

### **🛡️ Robustez y Mantenibilidad**

- **Transacciones**: Operaciones atómicas
- **Validación**: Integridad de datos garantizada
- **Logging**: Trazabilidad completa
- **Error handling**: Gestión robusta de errores

### **🔄 Flexibilidad**

- **Múltiples adaptadores**: Diferentes vistas de los mismos datos
- **Extensibilidad**: Fácil agregar nuevas funcionalidades
- **Testing**: Mockeable para pruebas unitarias
- **Evolución controlada**: Esquemas bien definidos y documentados

## 🔍 Integración con Otros Módulos

### **Con `ai/vectorstore.py`**

```python
# VectorStore usa adapter especializado
documents = db_vectorstore_adapter.get_all_documents_for_vectorstore()
```

### **Con `analytics/manager.py`**

```python
# Analytics usa adapter optimizado
db_analytics_adapter.record_interaction(user_id, message, response)
```

### **Con `ai/fallback_handler.py`**

```python
# Fallback usa funciones de compatibilidad
from database.fallback_main import get_cheapest_room_info
```

## 📈 Evolución Futura

### **Características Planificadas**

- ✅ **Réplicas**: Soporte para múltiples réplicas de lectura
- ✅ **Sharding**: Particionamiento horizontal para escalabilidad
- ✅ **Cache distribuido**: Redis para cache en múltiples instancias
- ✅ **Métricas avanzadas**: Monitoreo de rendimiento de BD
- ✅ **Backup automático**: Respaldos programados

### **Evolución de Bases de Datos**

- **PostgreSQL**: Migración a BD más robusta para producción
- **MongoDB**: Soporte para datos no estructurados
- **GraphQL**: API moderna para consultas complejas

---

## 💡 Mejores Prácticas

### **Para Desarrolladores**

1. **Usar Repository**: Para operaciones de negocio usar `repository.py`
2. **Usar Adapters**: Para casos específicos usar adaptadores apropiados
3. **Gestión de conexiones**: Nunca manejar conexiones directamente
4. **Transacciones**: Usar transacciones para operaciones críticas
5. **Validación**: Validar datos antes de persistir

### **Para Administradores**

1. **Backups regulares**: Respaldar `src/data/` periódicamente
2. **Monitoreo**: Vigilar logs de BD en `logs/bot.log`
3. **Validación**: Verificar integridad de datos regularmente
4. **Limpieza**: Ejecutar limpieza de datos antiguos regularmente

## 🔧 Solución de Problemas

### **BD No Encontrada**

```bash
# Verificar estructura
ls -la src/data/

# Verificar que las bases de datos existen
ls -la src/data/*.db
```

### **Datos Inconsistentes**

```bash
# Verificar integridad
python -c "from database.connection import DatabaseConnection; DatabaseConnection().validate_integrity()"
```

### **Rendimiento Lento**

```bash
# Analizar consultas
python -c "from database.repository import HotelRepository; HotelRepository().analyze_performance()"
```

Este módulo representa el corazón de la arquitectura moderna del ChatBot de Hotelería, proporcionando una base sólida y escalable para toda la gestión de datos del sistema.
