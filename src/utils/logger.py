"""
Configuración de logging centralizada
"""
import logging
from pathlib import Path

from config.settings import settings


def setup_logger(name: str = None) -> logging.Logger:
    """Configura y retorna un logger"""
    logger = logging.getLogger(name or __name__)

    # Evitar configurar múltiples veces
    if logger.handlers:
        return logger

    # Configurar nivel
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Configurar formato
    formatter = logging.Formatter(settings.LOG_FORMAT)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Obtener la ruta absoluta de la raíz del proyecto
    # Desde src/utils/ subir 3 niveles para llegar a la raíz
    project_root = Path(__file__).parent.parent.parent
    logs_dir = project_root / "logs"
    
    # Crear directorio logs en la raíz del proyecto si no existe
    logs_dir.mkdir(exist_ok=True)

    # Handler para archivo en la raíz del proyecto
    log_file = logs_dir / "bot.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Logger global
logger = setup_logger('hoteleria_bot')
