# 🧪 Módulo `testing/` - Pruebas y Validación

## 📋 Descripción General

El módulo `testing/` implementa un sistema completo de pruebas automatizadas para el ChatBot de Hotelería. Este módulo incluye pruebas unitarias, de integración, de rendimiento y de funcionalidad para garantizar la calidad y confiabilidad del sistema.

## 🏗️ Estructura del Módulo

```
testing/
├── __init__.py              # 📦 Inicialización del módulo
├── config.py                # ⚙️ Configuración de pruebas
├── run_tests.py             # 🚀 Ejecutor de pruebas
├── test_suite.py            # 🧪 Suite principal de pruebas
└── README.md                # 📖 Documentación del módulo
```

## 📄 Documentación por Archivo

### ⚙️ `config.py` - Configuración de Pruebas

**Propósito**: Centraliza toda la configuración relacionada con las pruebas, incluyendo entornos de testing, parámetros de validación y configuraciones específicas.

**Estructura**:
- **TestConfig**: Clase principal de configuración de pruebas
- **Entornos de Testing**: Configuración para diferentes entornos
- **Parámetros de Validación**: Criterios de éxito para pruebas
- **Configuración de Modelos**: Setup para modelos de testing

**Funcionalidades**:
- ✅ Configuración de entornos de testing (desarrollo, staging, producción)
- ✅ Parámetros de validación personalizables
- ✅ Configuración de modelos dummy para pruebas
- ✅ Timeouts y límites de tiempo
- ✅ Configuración de datos de prueba
- ✅ Logging específico para pruebas
- ✅ Configuración de coverage y reportes
- ✅ Integración con CI/CD

**Estructura de Configuración**:
```python
class TestConfig:
    def __init__(self):
        # Configuración básica de pruebas
        self.TEST_ENVIRONMENT = "development"
        self.USE_DUMMY_MODELS = True
        self.TEST_TIMEOUT = 30
        self.VALIDATION_THRESHOLD = 0.8
        
        # Configuración de datos de prueba
        self.TEST_DATA_DIR = "test_data/"
        self.SAMPLE_QUERIES = [...]
        self.EXPECTED_RESPONSES = {...}
        
        # Configuración de reporting
        self.GENERATE_REPORTS = True
        self.COVERAGE_REPORT = True
        self.HTML_REPORTS = True
```

**Configuraciones por Entorno**:

#### 🛠️ Desarrollo
```python
TEST_ENVIRONMENT = "development"
USE_DUMMY_MODELS = True
TEST_TIMEOUT = 10
VALIDATION_THRESHOLD = 0.7
GENERATE_REPORTS = False
```

#### 🧪 Staging
```python
TEST_ENVIRONMENT = "staging"
USE_DUMMY_MODELS = False
TEST_TIMEOUT = 30
VALIDATION_THRESHOLD = 0.8
GENERATE_REPORTS = True
```

#### 🚀 Producción
```python
TEST_ENVIRONMENT = "production"
USE_DUMMY_MODELS = False
TEST_TIMEOUT = 60
VALIDATION_THRESHOLD = 0.9
GENERATE_REPORTS = True
```

**Uso**:
```python
from testing.config import TestConfig

# Crear configuración de pruebas
config = TestConfig()

# Verificar configuración
if config.USE_DUMMY_MODELS:
    print("🧪 Usando modelos dummy para pruebas")
else:
    print("🚀 Usando modelos reales para pruebas")

# Obtener parámetros de validación
threshold = config.VALIDATION_THRESHOLD
timeout = config.TEST_TIMEOUT
```

**Dependencias**:
- `os`: Variables de entorno
- `pathlib`: Manejo de rutas
- `config.settings`: Configuración del sistema

---

### 🚀 `run_tests.py` - Ejecutor de Pruebas

**Propósito**: Proporciona una interfaz de línea de comandos y programática para ejecutar todas las pruebas del sistema de manera organizada y configurable.

**Estructura**:
- **TestRunner**: Clase principal para ejecución de pruebas
- **Argumentos de Línea de Comandos**: Interfaz CLI
- **Ejecución Programática**: API para ejecutar pruebas
- **Reportes**: Generación de reportes de resultados

**Funcionalidades**:
- ✅ Ejecución de pruebas desde línea de comandos
- ✅ Ejecución programática de suites de pruebas
- ✅ Filtrado de pruebas por categoría
- ✅ Configuración de entornos de testing
- ✅ Generación de reportes detallados
- ✅ Integración con sistemas CI/CD
- ✅ Manejo de errores y timeouts
- ✅ Paralelización de pruebas
- ✅ Coverage reporting
- ✅ Notificaciones de resultados

**Interfaz de Línea de Comandos**:
```bash
# Ejecutar todas las pruebas
python src/testing/run_tests.py

# Ejecutar pruebas específicas
python src/testing/run_tests.py --category unit
python src/testing/run_tests.py --category integration
python src/testing/run_tests.py --category performance

# Configurar entorno
python src/testing/run_tests.py --environment staging
python src/testing/run_tests.py --environment production

# Generar reportes
python src/testing/run_tests.py --generate-reports
python src/testing/run_tests.py --coverage-report

# Configurar timeouts
python src/testing/run_tests.py --timeout 60
python src/testing/run_tests.py --parallel
```

**Uso Programático**:
```python
from testing.run_tests import TestRunner

# Crear ejecutor de pruebas
runner = TestRunner()

# Ejecutar todas las pruebas
results = runner.run_all_tests()

# Ejecutar categoría específica
unit_results = runner.run_tests_by_category("unit")

# Ejecutar con configuración personalizada
custom_results = runner.run_tests(
    categories=["unit", "integration"],
    environment="staging",
    timeout=60,
    generate_reports=True
)

# Verificar resultados
if results.success:
    print(f"✅ Todas las pruebas pasaron: {results.passed}/{results.total}")
else:
    print(f"❌ Algunas pruebas fallaron: {results.failed}/{results.total}")
```

**Funciones Principales**:

#### `run_all_tests()`
- **Propósito**: Ejecuta todas las pruebas disponibles
- **Retorna**: Objeto con resultados completos
- **Funcionalidad**:
  - Ejecuta pruebas unitarias
  - Ejecuta pruebas de integración
  - Ejecuta pruebas de rendimiento
  - Genera reportes consolidados

#### `run_tests_by_category(category)`
- **Propósito**: Ejecuta pruebas de una categoría específica
- **Parámetros**:
  - `category`: Categoría de pruebas ("unit", "integration", "performance")
- **Retorna**: Resultados de la categoría específica

#### `run_tests(categories, environment, timeout, generate_reports)`
- **Propósito**: Ejecuta pruebas con configuración personalizada
- **Parámetros**:
  - `categories`: Lista de categorías a ejecutar
  - `environment`: Entorno de testing
  - `timeout`: Timeout en segundos
  - `generate_reports`: Si generar reportes
- **Retorna**: Resultados personalizados

**Dependencias**:
- `argparse`: Argumentos de línea de comandos
- `unittest`: Framework de pruebas
- `pytest`: Framework de pruebas avanzado
- `coverage`: Análisis de cobertura de código
- `testing.config`: Configuración de pruebas
- `testing.test_suite`: Suite de pruebas

---

### 🧪 `test_suite.py` - Suite Principal de Pruebas

**Propósito**: Contiene todas las pruebas automatizadas del sistema, organizadas por categorías y funcionalidades específicas.

**Estructura**:
- **TestBase**: Clase base para todas las pruebas
- **UnitTests**: Pruebas unitarias de componentes individuales
- **IntegrationTests**: Pruebas de integración entre módulos
- **PerformanceTests**: Pruebas de rendimiento y escalabilidad
- **FunctionalTests**: Pruebas de funcionalidad end-to-end

**Categorías de Pruebas**:

#### 🧩 Pruebas Unitarias
- **AI Models**: Pruebas de modelos de IA
- **Vectorstore**: Pruebas de base de conocimiento
- **Cache System**: Pruebas del sistema de caché
- **Text Processing**: Pruebas de procesamiento de texto
- **Configuration**: Pruebas de configuración del sistema

#### 🔗 Pruebas de Integración
- **Bot Integration**: Pruebas de integración del bot
- **AI Pipeline**: Pruebas del pipeline completo de IA
- **Analytics Integration**: Pruebas del sistema de analytics
- **Training Integration**: Pruebas del sistema de entrenamiento

#### ⚡ Pruebas de Rendimiento
- **Response Time**: Pruebas de tiempo de respuesta
- **Memory Usage**: Pruebas de uso de memoria
- **Concurrency**: Pruebas de concurrencia
- **Scalability**: Pruebas de escalabilidad

#### 🎯 Pruebas Funcionales
- **User Interactions**: Pruebas de interacciones de usuario
- **Command Processing**: Pruebas de procesamiento de comandos
- **Error Handling**: Pruebas de manejo de errores
- **Edge Cases**: Pruebas de casos límite

**Estructura de Clases**:
```python
class TestBase:
    """Clase base para todas las pruebas"""
    def setUp(self):
        # Configuración inicial de pruebas
    
    def tearDown(self):
        # Limpieza después de pruebas

class AIModelsTests(TestBase):
    """Pruebas de modelos de IA"""
    def test_model_loading(self):
        # Prueba carga de modelos
    
    def test_model_inference(self):
        # Prueba inferencia de modelos

class BotIntegrationTests(TestBase):
    """Pruebas de integración del bot"""
    def test_message_processing(self):
        # Prueba procesamiento de mensajes
    
    def test_command_handling(self):
        # Prueba manejo de comandos

class PerformanceTests(TestBase):
    """Pruebas de rendimiento"""
    def test_response_time(self):
        # Prueba tiempo de respuesta
    
    def test_memory_usage(self):
        # Prueba uso de memoria
```

**Ejemplos de Pruebas**:

#### Prueba de Carga de Modelos
```python
def test_model_loading(self):
    """Prueba que los modelos se carguen correctamente"""
    from ai.models import ai_models
    
    # Verificar que los modelos estén disponibles
    self.assertIsNotNone(ai_models.get_generador_sync())
    self.assertIsNotNone(ai_models.get_embedding_model_sync())
    
    # Verificar estadísticas
    stats = ai_models.get_stats()
    self.assertIn('models_loaded', stats)
    self.assertGreater(stats['models_loaded'], 0)
```

#### Prueba de Procesamiento de Mensajes
```python
def test_message_processing(self):
    """Prueba el procesamiento completo de mensajes"""
    from bot.bot_main import HoteleriaBot
    
    bot = HoteleriaBot()
    
    # Simular mensaje de usuario
    test_message = "¿Qué habitaciones tienen disponibles?"
    
    # Procesar mensaje
    response = bot._get_ai_response(test_message)
    
    # Verificar respuesta
    self.assertIsNotNone(response)
    self.assertGreater(len(response), 0)
    self.assertIn("habitación", response.lower())
```

#### Prueba de Rendimiento
```python
def test_response_time(self):
    """Prueba que el tiempo de respuesta sea aceptable"""
    import time
    from ai.text_generator import generate_response
    
    start_time = time.time()
    
    # Generar respuesta
    response = await generate_response("Consulta de prueba")
    
    end_time = time.time()
    response_time = end_time - start_time
    
    # Verificar tiempo de respuesta
    self.assertLess(response_time, 5.0)  # Máximo 5 segundos
    self.assertIsNotNone(response)
```

**Dependencias**:
- `unittest`: Framework de pruebas
- `asyncio`: Pruebas asíncronas
- `time`: Medición de tiempo
- `ai.models`: Modelos de IA
- `ai.vectorstore`: Base de conocimiento
- `bot.bot_main`: Bot principal
- `config.settings`: Configuración del sistema

---

## 🔧 Características del Módulo

### 🎯 Cobertura Completa
- **Pruebas Unitarias**: Cobertura de componentes individuales
- **Pruebas de Integración**: Verificación de interacciones entre módulos
- **Pruebas de Rendimiento**: Validación de escalabilidad y velocidad
- **Pruebas Funcionales**: Verificación de funcionalidad end-to-end

### ⚡ Ejecución Eficiente
- **Paralelización**: Ejecución concurrente de pruebas independientes
- **Filtrado Inteligente**: Ejecución selectiva por categoría
- **Timeouts Configurables**: Control de tiempo de ejecución
- **Recursos Optimizados**: Uso eficiente de memoria y CPU

### 📊 Reportes Detallados
- **Reportes HTML**: Visualización interactiva de resultados
- **Coverage Reports**: Análisis de cobertura de código
- **Métricas de Rendimiento**: Estadísticas de tiempo y recursos
- **Logs Detallados**: Información para debugging

### 🔄 Integración CI/CD
- **Automatización**: Ejecución automática en pipelines
- **Notificaciones**: Alertas de fallos en pruebas
- **Thresholds**: Criterios de éxito configurables
- **Rollback**: Reversión automática en caso de fallos

## 🚀 Configuración del Sistema

### Variables de Entorno
```bash
# Configuración de Pruebas
TEST_ENVIRONMENT=development
USE_DUMMY_MODELS=true
TEST_TIMEOUT=30
VALIDATION_THRESHOLD=0.8

# Configuración de Reportes
GENERATE_REPORTS=true
COVERAGE_REPORT=true
HTML_REPORTS=true

# Configuración de CI/CD
CI_MODE=false
NOTIFY_ON_FAILURE=true
AUTO_ROLLBACK_ON_FAILURE=false
```

### Configuración por Entorno

#### Desarrollo
```bash
TEST_ENVIRONMENT=development
USE_DUMMY_MODELS=true
TEST_TIMEOUT=10
GENERATE_REPORTS=false
```

#### Staging
```bash
TEST_ENVIRONMENT=staging
USE_DUMMY_MODELS=false
TEST_TIMEOUT=30
GENERATE_REPORTS=true
```

#### Producción
```bash
TEST_ENVIRONMENT=production
USE_DUMMY_MODELS=false
TEST_TIMEOUT=60
GENERATE_REPORTS=true
AUTO_ROLLBACK_ON_FAILURE=true
```

## 📁 Estructura de Reportes

### Archivos de Pruebas
```
testing/
├── reports/                 # 📋 Reportes de pruebas
│   ├── html/                # Reportes HTML
│   │   ├── test_results.html
│   │   └── coverage_report.html
│   ├── json/                # Reportes JSON
│   │   ├── test_results.json
│   │   └── performance_metrics.json
│   └── logs/                # Logs de pruebas
│       ├── test_execution.log
│       └── error_logs.log
├── test_data/               # 📊 Datos de prueba
│   ├── sample_queries.txt
│   ├── expected_responses.json
│   └── test_documents/
└── coverage/                # 📈 Datos de cobertura
    ├── .coverage
    └── htmlcov/
```

## 🚀 Inicio Rápido

```bash
# Ejecutar todas las pruebas
python src/testing/run_tests.py

# Ejecutar pruebas específicas
python src/testing/run_tests.py --category unit

# Ejecutar con configuración personalizada
python src/testing/run_tests.py --environment staging --timeout 60

# Generar reportes
python src/testing/run_tests.py --generate-reports --coverage-report
```

```python
# Ejecución programática
from testing.run_tests import TestRunner

runner = TestRunner()
results = runner.run_all_tests()

if results.success:
    print("✅ Todas las pruebas pasaron")
else:
    print(f"❌ {results.failed} pruebas fallaron")
```

## 📝 Notas de Desarrollo

- **Cobertura**: Mantener cobertura de código > 80%
- **Pruebas Regulares**: Ejecutar pruebas antes de cada commit
- **Documentación**: Mantener pruebas actualizadas con cambios
- **Performance**: Monitorear tiempo de ejecución de pruebas
- **Debugging**: Usar logs detallados para debugging
- **CI/CD**: Integrar pruebas en pipeline de deployment
