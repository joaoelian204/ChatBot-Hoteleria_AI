"""
Configuración centralizada del proyecto
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables de entorno
# Buscar el archivo .env en el directorio del proyecto
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
load_dotenv(env_path)


class Settings:
    """Configuración centralizada del proyecto"""

    # Configuración de la empresa
    EMPRESA_NOMBRE = os.getenv('EMPRESA_NOMBRE', 'Tu Hotel')
    EMPRESA_DESCRIPCION = os.getenv(
        'EMPRESA_DESCRIPCION', 'Hotel de lujo con servicios premium')

    # Configuración de Telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Configuración de modelos de IA
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 500))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 50))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    MAX_LENGTH = int(os.getenv('MAX_LENGTH', 300))

    # Modelos específicos
    MODELO_RESUMEN = os.getenv('MODELO_RESUMEN', 'facebook/bart-large-cnn')
    MODELO_GENERACION = os.getenv(
        'MODELO_GENERACION', 'microsoft/DialoGPT-medium')
    MODELO_EMBEDDINGS = os.getenv(
        'MODELO_EMBEDDINGS', 'sentence-transformers/all-mpnet-base-v2')

    # Configuración del bot
    ENABLE_RICH_RESPONSES = os.getenv(
        'ENABLE_RICH_RESPONSES', 'true').lower() == 'true'
    MAX_MESSAGE_LENGTH = 1000
    MAX_MESSAGES_PER_MINUTE = 10

    # Directorios
    DOCUMENTOS_DIR = project_root / "documentos"
    CONFIG_FILE = project_root / "config" / "entrenamiento_config.json"
    ANALYTICS_FILE = project_root / "data" / "analytics.json"
    FEEDBACK_FILE = project_root / "data" / "feedback.json"
    USAGE_STATS_FILE = project_root / "data" / "usage_stats.json"

    # Configuración de cache
    CACHE_DURATION_HOURS = int(os.getenv('CACHE_DURATION_HOURS', 24))
    MAX_CACHE_SIZE = int(os.getenv('MAX_CACHE_SIZE', 1000))

    # Configuración de recursos y modelos
    ENABLE_MODEL_CACHING = os.getenv(
        'ENABLE_MODEL_CACHING', 'true').lower() == 'true'
    LAZY_LOAD_MODELS = os.getenv('LAZY_LOAD_MODELS', 'true').lower() == 'true'
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', 10))

    # Configuración de respuestas enriquecidas
    ENABLE_EMOJI_FORMATTING = os.getenv(
        'ENABLE_EMOJI_FORMATTING', 'true').lower() == 'true'

    # Configuración de analíticas
    ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'true').lower() == 'true'
    ANALYTICS_SAVE_INTERVAL = int(os.getenv('ANALYTICS_SAVE_INTERVAL', 10))

    # Configuración de monitoreo (deshabilitado - módulo eliminado)
    AUTO_UPDATE_DOCUMENTS = False  # Deshabilitado - sin monitor de documentos
    MONITOR_DOCUMENT_CHANGES = False  # Deshabilitado - módulo eliminado

    # Versión del modelo
    MODEL_VERSION = "1.0.0"

    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @classmethod
    def validate(cls):
        """Valida que la configuración sea correcta"""
        if not cls.TELEGRAM_TOKEN:
            raise ValueError("Token de Telegram no encontrado en .env")

        if not cls.DOCUMENTOS_DIR.exists():
            cls.DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)

        return True


# Instancia global de configuración
settings = Settings()
