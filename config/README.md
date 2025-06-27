# ⚙️ Carpeta `config/` - Configuración del Proyecto

## 🎯 ¿Por qué es Importante esta Carpeta?

La carpeta `config/` de la raíz del proyecto es **fundamental** para el funcionamiento del ChatBot de Hotelería por las siguientes razones:

### 🏗️ **Arquitectura del Proyecto**
- **Configuración Estructural**: Define la organización de carpetas y archivos del proyecto
- **Rutas Centralizadas**: Todas las rutas importantes se definen en un solo lugar
- **Flexibilidad**: Permite cambiar la estructura sin modificar código fuente
- **Portabilidad**: El proyecto puede funcionar en diferentes entornos

### 🔧 **Gestión de Funcionalidades**
- **Control de Features**: Habilita/deshabilita funcionalidades del sistema
- **Configuración de Testing**: Define parámetros para el sistema de pruebas
- **Gestión de Analytics**: Configura el sistema de métricas y reportes
- **Control de Logging**: Define la configuración de logs del sistema

### 📊 **Metadatos del Proyecto**
- **Información del Proyecto**: Nombre, versión, descripción y fecha de creación
- **Trazabilidad**: Permite rastrear versiones y cambios del sistema
- **Documentación**: Información centralizada sobre el proyecto
- **Identificación**: Datos para identificar el proyecto en diferentes contextos

### 🔄 **Configuración de Entrenamiento**
- **Parámetros de IA**: Configuración específica para modelos de inteligencia artificial
- **Auto-actualización**: Control de actualizaciones automáticas del sistema
- **Gestión de Documentos**: Configuración de directorios de entrenamiento
- **Optimización**: Ajustes para mejorar el rendimiento de los modelos

---

## 📁 Contenido de la Carpeta

```
config/
├── project_config.json        # ⚙️ Configuración principal del proyecto
├── entrenamiento_config.json  # 🧠 Configuración de entrenamiento de IA
└── README.md                  # 📚 Documentación de la carpeta
```

## 📄 Documentación por Archivo

### ⚙️ `project_config.json` - Configuración Principal

**Propósito**: Configuración centralizada que define la estructura y funcionalidades del proyecto.

**Estructura**:

#### 🏢 Información del Proyecto
```json
{
  "project": {
    "name": "ChatBot de Hotelería",
    "version": "1.0.0",
    "description": "Sistema de chatbot inteligente para hotelería con IA avanzada",
    "created": "2025-06-25"
  }
}
```

#### 📁 Directorios del Sistema
```json
{
  "directories": {
    "data": "data",
    "models": "data/models",
    "reports": "reports",
    "logs": "logs",
    "config": "config",
    "documentos": "documentos",
    "src": "src"
  }
}
```

#### 📄 Archivos Importantes
```json
{
  "files": {
    "analytics": "data/analytics.json",
    "analytics_db": "data/analytics.db",
    "training_config": "config/entrenamiento_config.json",
    "main_log": "logs/bot.log"
  }
}
```

#### 🧪 Configuración de Testing
```json
{
  "testing": {
    "reports_dir": "reports",
    "report_prefix": "test_report_",
    "max_reports_keep": 10
  }
}
```

#### ⚡ Control de Funcionalidades
```json
{
  "features": {
    "ai_enabled": true,
    "testing_enabled": true,
    "analytics_enabled": true,
    "logging_enabled": true
  }
}
```

### 🧠 `entrenamiento_config.json` - Configuración de IA

**Propósito**: Configuración específica para el entrenamiento y actualización de modelos de inteligencia artificial.

**Estructura**:
```json
{
  "auto_update": true,
  "last_update": "2025-06-25T19:06:24.025852",
  "documentos_dir": "documentos"
}
```

**Parámetros**:
- **auto_update**: Habilita actualizaciones automáticas de modelos
- **last_update**: Timestamp de la última actualización
- **documentos_dir**: Directorio donde se almacenan documentos para entrenamiento

---

## 🔧 Características del Módulo

### 🎯 Centralización
- **Configuración Única**: Todos los parámetros del proyecto en un solo lugar
- **Organización Lógica**: Configuración agrupada por categorías
- **Fácil Acceso**: Archivos JSON legibles y editables
- **Versionado**: Control de cambios en la configuración

### 🔒 Seguridad y Mantenimiento
- **Datos Sensibles**: Algunos archivos pueden contener información confidencial
- **Backup Automático**: Configuración respaldada en el sistema de versiones
- **Validación**: Estructura JSON validada para evitar errores
- **Documentación**: Cada parámetro tiene su propósito documentado

### ⚡ Flexibilidad
- **Configuración Dinámica**: Cambios sin reiniciar el sistema
- **Entornos Múltiples**: Diferentes configuraciones para desarrollo y producción
- **Escalabilidad**: Fácil agregar nuevos parámetros
- **Portabilidad**: Funciona en diferentes sistemas operativos

### 📊 Monitoreo
- **Trazabilidad**: Registro de cambios en la configuración
- **Auditoría**: Control de qué funcionalidades están habilitadas
- **Reportes**: Generación de reportes basados en configuración
- **Debugging**: Información detallada para desarrollo

## 🚀 Uso del Sistema

### Carga de Configuración
```python
import json
from pathlib import Path

# Cargar configuración principal
with open('config/project_config.json', 'r', encoding='utf-8') as f:
    project_config = json.load(f)

# Cargar configuración de entrenamiento
with open('config/entrenamiento_config.json', 'r', encoding='utf-8') as f:
    training_config = json.load(f)

# Acceder a configuración
project_name = project_config['project']['name']
data_dir = project_config['directories']['data']
ai_enabled = project_config['features']['ai_enabled']
```

### Validación de Configuración
```python
def validate_config():
    """Valida que la configuración sea correcta"""
    try:
        with open('config/project_config.json', 'r') as f:
            config = json.load(f)
        
        # Verificar directorios requeridos
        required_dirs = ['data', 'logs', 'documentos', 'src']
        for dir_name in required_dirs:
            if dir_name not in config['directories']:
                raise ValueError(f"Directorio requerido no encontrado: {dir_name}")
        
        # Verificar features críticas
        if not config['features']['ai_enabled']:
            print("⚠️ IA deshabilitada en configuración")
        
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False
```

### Actualización de Configuración
```python
def update_training_config(last_update):
    """Actualiza la configuración de entrenamiento"""
    config = {
        "auto_update": True,
        "last_update": last_update,
        "documentos_dir": "documentos"
    }
    
    with open('config/entrenamiento_config.json', 'w') as f:
        json.dump(config, f, indent=2)
```

## 🔄 Flujo de Trabajo

### 1. **Configuración Inicial**
```bash
# Verificar que la carpeta config existe
ls config/

# Validar archivos JSON
python -m json.tool config/project_config.json
python -m json.tool config/entrenamiento_config.json
```

### 2. **Carga en el Código**
```python
from config.project_config import load_project_config
from config.training_config import load_training_config

# Cargar configuraciones
project_config = load_project_config()
training_config = load_training_config()
```

### 3. **Uso en el Sistema**
```python
# Usar rutas de directorios
data_dir = project_config['directories']['data']
logs_dir = project_config['directories']['logs']

# Verificar funcionalidades
if project_config['features']['ai_enabled']:
    # Ejecutar funcionalidades de IA
    pass

# Configurar testing
reports_dir = project_config['testing']['reports_dir']
```

## 📝 Notas de Desarrollo

### ✅ **Buenas Prácticas**
- **Validación**: Siempre validar JSON antes de usar
- **Backup**: Hacer copias antes de cambios importantes
- **Documentación**: Mantener README actualizado
- **Versionado**: Documentar cambios en configuración
- **Testing**: Probar configuración en todos los entornos

### ⚠️ **Consideraciones Importantes**
- **Seguridad**: Revisar qué archivos contienen datos sensibles
- **Gitignore**: Algunos archivos pueden estar excluidos del repositorio
- **Permisos**: Asegurar permisos correctos en archivos de configuración
- **Compatibilidad**: Mantener compatibilidad entre versiones

### 🔧 **Mantenimiento**
- **Actualizaciones**: Revisar regularmente valores de configuración
- **Optimización**: Ajustar parámetros según el uso del sistema
- **Limpieza**: Eliminar configuraciones obsoletas
- **Documentación**: Mantener ejemplos de uso actualizados

---

## 🎯 Resumen de Importancia

La carpeta `config/` de la raíz es **esencial** para el proyecto porque:

1. **🏗️ Define** la arquitectura y estructura del proyecto
2. **🔧 Controla** qué funcionalidades están habilitadas
3. **📊 Gestiona** metadatos y información del proyecto
4. **🧠 Configura** el sistema de entrenamiento de IA
5. **🔄 Permite** cambios sin modificar código fuente
6. **📁 Centraliza** todas las rutas y archivos importantes

**Sin esta carpeta, el proyecto no tendría una estructura definida ni control sobre sus funcionalidades.**
