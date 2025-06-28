# 🤖 ChatBot de Hotelería con IA

Un **sistema de chatbot inteligente para hotelería** de nivel enterprise que utiliza IA avanzada para responder consultas sobre servicios, habitaciones, restaurantes y más. Diseñado para ser **100% reutilizable** para cualquier hotel cambiando solo los datos en la base de datos.

## 🌟 Características Principales

### 🧠 **IA Avanzada y Modular**
- **Modelos múltiples**: Resumen, generación, embeddings e intenciones
- **Búsqueda semántica**: Vectorstore con FAISS para respuestas precisas
- **Carga perezosa**: Optimización de memoria con lazy loading
- **Cache inteligente**: Respuestas rápidas para preguntas frecuentes
- **Sistema modularizado**: Arquitectura de servicios especializados

### 🏗️ **Arquitectura Profesional Modularizada**
- **Servicios especializados**: Cada funcionalidad en su módulo
- **Base de datos centralizada**: SQLite como fuente única de verdad
- **Escalable**: Manejo de concurrencia y múltiples usuarios
- **Configurable**: Variables de entorno para personalización
- **Mantenible**: Código limpio con type hints y documentación

### 🧪 **Testing Comprehensivo**
- **4 niveles de dificultad**: Fácil, Medio, Difícil, Pesadilla
- **Tests de estrés**: Evaluación bajo alta carga
- **Tests concurrentes**: Validación de acceso simultáneo
- **Métricas detalladas**: Análisis completo de rendimiento
- **Tests de modularización**: Verificación de servicios independientes

### 🛡️ **Seguridad y Validaciones**
- **Protección contra spam**: Rate limiting por usuario
- **Sanitización de texto**: Prevención de inyecciones
- **Validación de entrada**: Múltiples capas de seguridad
- **Logging completo**: Auditoría de todas las operaciones
- **Manejo robusto de errores**: Sistema tolerante a fallos

### 📊 **Analytics y Monitoreo**
- **Base de datos SQLite**: Almacenamiento persistente
- **Métricas en tiempo real**: Seguimiento de uso
- **Estadísticas detalladas**: Análisis de comportamiento
- **Gestión de sesiones**: Tracking de usuarios

## 🚀 Reutilización para Otros Hoteles

### ✅ **100% Reutilizable - Solo Modifica la Base de Datos**

Este sistema está diseñado para ser **completamente reutilizable** para cualquier hotel. El conocimiento se gestiona centralmente desde la base de datos SQLite:

```
src/
├── data/
│   ├── hotel_content.db        # 📊 Base de datos principal con contenido del hotel
│   └── analytics.db            # 📈 Base de datos de análisis y métricas
├── database/
│   ├── services/               # 🔧 Servicios modulares especializados
│   │   ├── room_service.py     #    • Gestión de habitaciones
│   │   ├── amenities_service.py#    • Servicios y amenidades
│   │   ├── contact_service.py  #    • Información de contacto
│   │   ├── price_service.py    #    • Búsquedas por precio
│   │   └── welcome_service.py  #    • Mensajes de bienvenida
│   └── fallback_main.py        # 🎯 Orquestador modular
└── models/                     # 🤖 Modelos de IA entrenados
    └── training_log.json       # 📝 Log de entrenamiento
```
```

**Ventajas de la arquitectura modularizada**:
- ✅ **Gestión centralizada**: Todo el conocimiento en base de datos SQLite
- ✅ **Servicios especializados**: Cada funcionalidad en su módulo independiente
- ✅ **Consultas avanzadas**: SQL para búsquedas complejas  
- ✅ **Integridad de datos**: Validaciones y consistencia automática
- ✅ **Escalabilidad**: Mejor rendimiento y mantenibilidad
- ✅ **Testing granular**: Cada servicio puede probarse independientemente

### 🔄 **Proceso de Migración para Nuevo Hotel**

1. **Clonar el proyecto**
   ```bash
   git clone <tu-repositorio>
   cd chatBot-Hoteleria
   ```

2. **Configurar variables de entorno**
   ```bash
   cp configuracion.env .env
   # Editar .env con datos del nuevo hotel
   ```

3. **Personalizar base de datos**
   ```bash
   # Editar contenido en src/data/hotel_content.db
   # usando scripts SQL o herramientas de BD
   # Para poblar con datos del nuevo hotel
   python tools/populate_hotel_data.py  # Script helper
   ```

4. **Obtener token de Telegram**
   - Habla con @BotFather en Telegram
   - Crea un nuevo bot con `/newbot`
   - Copia el token a `.env`

5. **Verificar sistema modular**
   ```bash
   python src/main.py --check    # Verificar configuración
   python -m database.fallback_main  # Test modularización
   ```

6. **Inicializar sistema**
   ```bash
   python src/main.py --mode train  # Entrenar con nuevos datos
   ```

7. **Iniciar el bot**
   ```bash
   python src/main.py --mode bot
   ```

## 📋 Requisitos del Sistema

- **Python 3.8+**
- **RAM**: Mínimo 4GB (recomendado 8GB+)
- **Almacenamiento**: 2GB libres para modelos
- **Conexión a internet**: Para descargar modelos de IA
- **Token de Telegram Bot**: Obtener de @BotFather

## 🛠️ Instalación y Configuración

### 1. **Preparar el entorno**

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd chatBot-Hoteleria

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. **Configurar el proyecto**

```bash
# Copiar archivo de configuración
cp configuracion.env .env

# Editar .env con tus valores
# - TELEGRAM_TOKEN: Token de tu bot
# - EMPRESA_NOMBRE: Nombre de tu hotel
# - EMPRESA_DESCRIPCION: Descripción del hotel
```

### 3. **Configurar contenido del hotel**

El contenido del hotel se gestiona directamente en la base de datos SQLite (`src/data/hotel_content.db`):

- **Información general**: Datos básicos, contacto, historia del hotel
- **Habitaciones**: Tipos, precios, servicios incluidos  
- **Restaurantes**: Menús, horarios, especialidades
- **Servicios**: Spa, actividades, amenidades disponibles
- **Políticas**: Reservas, check-in/out, cancelaciones

**Para modificar el contenido**:
```bash
# Usar herramientas SQLite para editar la BD
sqlite3 src/data/hotel_content.db

# O crear scripts de poblado personalizados
python tools/populate_hotel_data.py
```

### 4. **Inicializar el sistema**

```bash
# El sistema se inicializa automáticamente con la BD
python src/main.py --mode bot
```

## 🚀 Uso del Sistema

### **Modos de Operación**

```bash
# Ejecutar el bot
python src/main.py --mode bot

# Entrenar con documentos
python src/main.py --mode train

# Ver analíticas
python src/main.py --mode analytics

# Verificar configuración
python src/main.py --mode check

# Menú interactivo
python src/main.py
```

### **🧪 Sistema de Testing Universal**

```bash
# Modo interactivo (recomendado)
python -m src.testing.run_tests

# Tests rápidos
python -m src.testing.run_tests --quick

# Nivel específico
python -m src.testing.run_tests --difficulty hard

# Ver último reporte
python -m src.testing.run_tests --report-only
```

### **Niveles de Testing**

- **🟢 Fácil**: Tests básicos (10 iteraciones) - Desarrollo diario
- **🟡 Medio**: Tests completos (50 iteraciones) - Pre-producción
- **🔴 Difícil**: Tests intensivos (100 iteraciones) - Testing de carga
- **💀 Pesadilla**: Tests extremos (500 iteraciones) - Benchmarking

## 📁 Arquitectura del Proyecto

```
chatBot-Hoteleria/
├── src/                    # 🔧 Código fuente principal
│   ├── ai/                 # 🧠 Módulos de IA y procesamiento
│   │   ├── models.py       # Gestión de modelos de IA
│   │   ├── vectorstore.py  # Búsqueda semántica con BD
│   │   ├── cache.py        # Cache inteligente
│   │   ├── fallback_handler.py # Proxy a BD y respuestas por defecto
│   │   ├── intent_detector.py # Detección de intenciones
│   │   └── text_generator.py # Generación de respuestas
│   ├── bot/                # 🤖 Bot de Telegram y handlers
│   │   ├── bot_main.py     # Bot principal
│   │   └── callbacks.py    # Manejadores de eventos
│   ├── config/             # ⚙️ Configuración del sistema
│   │   └── settings.py     # Configuración centralizada
│   ├── database/           # 🗄️ Capa de acceso a datos MODULARIZADA
│   │   ├── services/       # 🔧 Servicios modulares especializados
│   │   │   ├── basic_info_service.py    # Información básica y utilidades
│   │   │   ├── welcome_service.py       # Mensajes de bienvenida
│   │   │   ├── room_service.py          # Gestión de habitaciones
│   │   │   ├── contact_service.py       # Información de contacto
│   │   │   ├── facility_service.py      # Restaurantes y amenidades
│   │   │   └── price_search_service.py  # Búsqueda por precios
│   │   ├── connection.py   # Conexiones a BD
│   │   ├── repository.py   # Repositorios de datos
│   │   ├── adapter.py      # Adaptadores de BD
│   │   └── fallback_main.py # Orquestador modular (importa servicios)
│   ├── data/               # 💾 Bases de datos centralizadas
│   │   └── hotel_content.db # Base de datos principal del hotel
│   ├── testing/            # 🧪 Sistema de testing universal
│   │   ├── test_suite.py   # Suite principal de tests
│   │   ├── run_tests.py    # Ejecutor de tests
│   │   └── config.py       # Configuración de tests
│   ├── training/           # 📚 Entrenamiento y actualización
│   ├── analytics/          # 📊 Sistema de analíticas
│   │   └── manager.py      # Gestión de métricas
│   ├── utils/              # 🛠️ Utilidades comunes
│   │   ├── logger.py       # Sistema de logging
│   │   └── text_processor.py # Procesamiento de texto
│   └── main.py             # 🚀 Script principal
├── config/                 # ⚙️ Archivos de configuración
│   ├── entrenamiento_config.json # Configuración de entrenamiento
│   └── README.md           # Documentación de configuración
├── scripts/                # 🔧 Scripts de utilidad
├── logs/                   # 📝 Archivos de log (auto-gestionado)
├── requirements.txt        # 📦 Dependencias del proyecto
├── configuracion.env       # 🔒 Template de variables de entorno
├── .env                    # 🔒 Variables de entorno (crear desde configuracion.env)
├── README.md               # 📖 Esta documentación
└── .gitignore              # 🚫 Configuración Git
```

**Cambios principales en la arquitectura**:
- ✅ **Eliminada carpeta `documentos/`**: Ya no se necesitan archivos de texto
- ✅ **Nueva carpeta `src/data/`**: Bases de datos centralizadas
- ✅ **Nueva carpeta `src/database/`**: Capa de acceso a datos profesional
- ✅ **Fallback modernizado**: Ahora funciona como proxy a la base de datos

## 🎯 Comandos del Bot

### **Comandos Básicos**
- `/start` - Iniciar conversación
- `/help` - Mostrar ayuda
- `/stats` - Ver estadísticas del sistema
- `/clear_cache` - Limpiar cache de respuestas

### **Comandos de Información**
- `/rooms` - Información de habitaciones
- `/restaurants` - Información de restaurantes
- `/amenities` - Servicios y actividades
- `/contact` - Información de contacto

### **Ejemplos de Consultas Naturales**
- "¿Cuál es la habitación más barata?"
- "Información sobre restaurantes"
- "¿Qué actividades tienen?"
- "Quiero hacer una reserva"
- "¿Cuál es el precio de la suite?"

## 🔧 Configuración Avanzada

### **Modelos de IA Personalizables**

Puedes cambiar los modelos en `.env`:

```env
# Modelos específicos
MODELO_RESUMEN=facebook/bart-large-cnn
MODELO_GENERACION=microsoft/DialoGPT-medium
MODELO_EMBEDDINGS=sentence-transformers/all-mpnet-base-v2
```

### **Parámetros de Rendimiento**

```env
# Configuración de procesamiento
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TEMPERATURE=0.7
MAX_LENGTH=300

# Configuración de cache
CACHE_DURATION_HOURS=24
MAX_CACHE_SIZE=1000

# Configuración de concurrencia
MAX_CONCURRENT_REQUESTS=10
```

### **Configuración de Seguridad**

```env
# Límites de uso
MAX_MESSAGE_LENGTH=1000
MAX_MESSAGES_PER_MINUTE=10

# Validaciones
ENABLE_RICH_RESPONSES=true
ENABLE_EMOJI_FORMATTING=true
```

## 📊 Analytics y Métricas

### **Métricas Automáticas**
- Preguntas más frecuentes
- Tiempos de respuesta
- Rendimiento del cache
- Feedback de usuarios
- Estadísticas diarias

### **Acceso a Analytics**
```bash
# Ver analíticas en consola
python src/main.py --mode analytics

# Comando /stats en el bot
/stats
```

## 🛡️ Seguridad y Validaciones

### **Protección Implementada**
- **Rate limiting**: 10 mensajes por minuto por usuario
- **Sanitización**: Limpieza automática de mensajes
- **Validación**: Verificación de longitud y contenido
- **Logging**: Registro de intentos de abuso
- **Fallback**: Respuestas seguras por defecto

### **Monitoreo de Seguridad**
- Detección de comportamiento sospechoso
- Bloqueo temporal automático
- Alertas de seguridad
- Auditoría completa de eventos

## 🧪 Testing y Calidad

### **Sistema de Testing Universal**
- **Tests funcionales**: Validación de respuestas
- **Tests de rendimiento**: Evaluación de velocidad
- **Tests de seguridad**: Validación de inputs maliciosos
- **Tests de concurrencia**: Manejo de múltiples usuarios
- **Tests de estrés**: Evaluación bajo alta carga

### **Métricas de Calidad**
- **Tasa de éxito**: Porcentaje de tests pasados
- **Tiempo de respuesta**: Promedio y máximo
- **Score de rendimiento**: Basado en velocidad y precisión
- **Robustez**: Manejo de casos extremos

## 🔄 Actualización y Mantenimiento

### **Actualización de Contenido del Hotel**
```bash
# Actualizar contenido en la base de datos
sqlite3 src/data/hotel_content.db "UPDATE hotel_info SET descripcion = 'Nueva descripción';"

# Reentrenar después de cambios en BD
python src/main.py --mode train
```

### **Limpieza Automática**
- **Reportes**: Solo se mantienen los últimos 10
- **Logs**: Rotación automática según configuración
- **Cache**: Limpieza automática por tiempo y tamaño

### **Backup y Restauración**
```bash
# Backup de configuración y base de datos
cp .env .env.backup
cp src/data/hotel_content.db src/data/hotel_content.db.backup

# Restaurar configuración
cp .env.backup .env
cp src/data/hotel_content.db.backup src/data/hotel_content.db

# Verificar integridad de la base de datos
python -c "import sqlite3; print('BD OK') if sqlite3.connect('src/data/hotel_content.db').execute('SELECT 1').fetchone() else print('BD ERROR')"
```

## 🤝 Contribuir al Proyecto

### **Proceso de Contribución**
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### **Estándares de Código**
- Usar type hints en todas las funciones
- Documentar con docstrings
- Seguir PEP 8
- Incluir tests para nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte y Troubleshooting

### **Problemas Comunes**

#### **Error: Token de Telegram no encontrado**
```bash
# Verificar que .env existe y tiene TELEGRAM_TOKEN
cat .env | grep TELEGRAM_TOKEN
```

#### **Error: Modelos no se cargan**
```bash
# Verificar conexión a internet
# Verificar espacio en disco (necesita 2GB+)
# Verificar RAM disponible (necesita 4GB+)
```

#### **Error: Base de datos no encontrada**
```bash
# Verificar que existe la base de datos
ls -la src/data/hotel_content.db
# Verificar integridad de la BD
python -c "import sqlite3; conn=sqlite3.connect('src/data/hotel_content.db'); print(f'Tablas: {[t[0] for t in conn.execute(\"SELECT name FROM sqlite_master WHERE type=table\").fetchall()]}')"
```

#### **Bot no responde**
```bash
# Verificar que el bot está activo
python src/main.py --mode check
# Verificar logs
tail -f logs/chatbot.log
```

### **Obtener Ayuda**
1. Revisar la configuración en `.env`
2. Verificar que todos los archivos estén en su lugar
3. Asegurarte de tener conexión a internet
4. Revisar los logs para errores específicos
5. Ejecutar tests para diagnosticar problemas

## 🏆 Características Destacadas

### **Nivel Enterprise**
- Arquitectura modular y escalable
- Testing comprehensivo y automatizado
- Seguridad robusta y validaciones
- Analytics y monitoreo en tiempo real
- Documentación completa y profesional

### **Fácil Reutilización**
- Configuración centralizada
- Documentos separados del código
- Proceso de migración simplificado
- Templates y ejemplos incluidos
- Soporte para múltiples idiomas

### **Alto Rendimiento**
- Cache inteligente
- Carga perezosa de modelos
- Optimización de memoria
- Manejo de concurrencia
- Búsqueda semántica eficiente

---

**⭐ Si este proyecto te ha sido útil, considera darle una estrella en GitHub!**

**🤝 Contribuciones, reportes de bugs y sugerencias son bienvenidos.**
