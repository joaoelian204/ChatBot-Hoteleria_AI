# 🤖 ChatBot de Hotelería con IA

Un **sistema de chatbot inteligente para hotelería** de nivel enterprise que utiliza IA avanzada para responder consultas sobre servicios, habitaciones, restaurantes y más. Diseñado para ser **100% reutilizable** para cualquier hotel cambiando solo los documentos de conocimiento.

## 🌟 Características Principales

### 🧠 **IA Avanzada y Modular**
- **Modelos múltiples**: Resumen, generación, embeddings e intenciones
- **Búsqueda semántica**: Vectorstore con FAISS para respuestas precisas
- **Carga perezosa**: Optimización de memoria con lazy loading
- **Cache inteligente**: Respuestas rápidas para preguntas frecuentes
- **Fallback robusto**: Sistema de respuestas por defecto bien implementado

### 🏗️ **Arquitectura Profesional**
- **Modular**: Separación clara de responsabilidades
- **Escalable**: Manejo de concurrencia y múltiples usuarios
- **Configurable**: Variables de entorno para personalización
- **Mantenible**: Código limpio con type hints y documentación

### 🧪 **Testing Comprehensivo**
- **4 niveles de dificultad**: Fácil, Medio, Difícil, Pesadilla
- **Tests de estrés**: Evaluación bajo alta carga
- **Tests concurrentes**: Validación de acceso simultáneo
- **Métricas detalladas**: Análisis completo de rendimiento
- **Reportes estructurados**: JSON con timestamp y análisis

### 🛡️ **Seguridad y Validaciones**
- **Protección contra spam**: Rate limiting por usuario
- **Sanitización de texto**: Prevención de inyecciones
- **Validación de entrada**: Múltiples capas de seguridad
- **Logging completo**: Auditoría de todas las operaciones

### 📊 **Analytics y Monitoreo**
- **Base de datos SQLite**: Almacenamiento persistente
- **Métricas en tiempo real**: Seguimiento de uso
- **Estadísticas detalladas**: Análisis de comportamiento
- **Gestión de sesiones**: Tracking de usuarios

## 🚀 Reutilización para Otros Hoteles

### ✅ **100% Reutilizable - Solo Cambia los Documentos**

Este sistema está diseñado para ser **completamente reutilizable** para cualquier hotel. Solo necesitas cambiar los archivos en la carpeta `documentos/`:

```
documentos/
├── hotel_info.txt          # Información específica del hotel
├── habitaciones_precios.txt # Tipos de habitaciones y precios
├── restaurantes_menus.txt   # Información de restaurantes
├── amenidades_actividades.txt # Servicios y actividades
└── politicas.txt           # Políticas del hotel
```

### 🔄 **Proceso de Migración para Nuevo Hotel**

1. **Clonar el proyecto**
   ```bash
   git clone <tu-repositorio>
   cd ejerciico_api
   ```

2. **Configurar variables de entorno**
   ```bash
   cp configuracion.env .env
   # Editar .env con datos del nuevo hotel
   ```

3. **Reemplazar documentos**
   ```bash
   # Reemplazar todos los archivos en documentos/
   # con la información específica del nuevo hotel
   ```

4. **Obtener token de Telegram**
   - Habla con @BotFather en Telegram
   - Crea un nuevo bot con `/newbot`
   - Copia el token a `.env`

5. **Entrenar el sistema**
   ```bash
   python src/main.py --mode train
   ```

6. **Iniciar el bot**
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
cd ejerciico_api

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

### 3. **Preparar documentos del hotel**

Reemplaza los archivos en `documentos/` con la información de tu hotel:

- **`hotel_info.txt`**: Información general, contacto, historia
- **`habitaciones_precios.txt`**: Tipos de habitaciones, precios, servicios
- **`restaurantes_menus.txt`**: Restaurantes, menús, horarios
- **`amenidades_actividades.txt`**: Servicios, actividades, spa
- **`politicas.txt`**: Políticas de reserva, check-in/out

### 4. **Entrenar el sistema**

```bash
# Entrenar con los documentos del hotel
python src/main.py --mode train
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
ejerciico_api/
├── src/                    # 🔧 Código fuente principal
│   ├── ai/                 # 🧠 Módulos de IA y procesamiento
│   │   ├── models.py       # Gestión de modelos de IA
│   │   ├── vectorstore.py  # Búsqueda semántica
│   │   ├── cache.py        # Cache inteligente
│   │   ├── fallback_handler.py # Respuestas por defecto
│   │   └── intent_detector.py # Detección de intenciones
│   ├── bot/                # 🤖 Bot de Telegram y handlers
│   │   ├── bot_main.py     # Bot principal
│   │   └── callbacks.py    # Manejadores de eventos
│   ├── config/             # ⚙️ Configuración del sistema
│   │   └── settings.py     # Configuración centralizada
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
├── documentos/             # 📄 Documentos de conocimiento del hotel
│   ├── hotel_info.txt      # Información general del hotel
│   ├── habitaciones_precios.txt # Habitaciones y precios
│   ├── restaurantes_menus.txt   # Restaurantes y menús
│   ├── amenidades_actividades.txt # Servicios y actividades
│   └── politicas.txt       # Políticas del hotel
├── config/                 # ⚙️ Archivos de configuración
│   ├── entrenamiento_config.json # Configuración de entrenamiento
│   └── README.md           # Documentación de configuración
├── scripts/                # 🔧 Scripts de utilidad
├── data/                   # 💾 Datos generados (auto-gestionado)
├── reports/                # 📋 Reportes de testing (auto-gestionado)
├── logs/                   # 📝 Archivos de log (auto-gestionado)
├── requirements.txt        # 📦 Dependencias del proyecto
├── configuracion.env       # 🔒 Template de variables de entorno
├── .env                    # 🔒 Variables de entorno (crear desde configuracion.env)
├── README.md               # 📖 Esta documentación
└── .gitignore              # 🚫 Configuración Git
```

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

### **Actualización de Documentos**
```bash
# Reentrenar después de cambiar documentos
python src/main.py --mode train
```

### **Limpieza Automática**
- **Reportes**: Solo se mantienen los últimos 10
- **Logs**: Rotación automática según configuración
- **Cache**: Limpieza automática por tiempo y tamaño

### **Backup y Restauración**
```bash
# Backup de configuración
cp .env .env.backup
cp -r documentos/ documentos_backup/

# Restaurar configuración
cp .env.backup .env
cp -r documentos_backup/ documentos/
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

#### **Error: Documentos no encontrados**
```bash
# Verificar que existen archivos en documentos/
ls documentos/
# Reentrenar el sistema
python src/main.py --mode train
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
