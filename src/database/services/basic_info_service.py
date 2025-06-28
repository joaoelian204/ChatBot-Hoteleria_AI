"""
Servicio para información básica del hotel y funciones utilitarias
"""
import re
import unicodedata
from datetime import datetime
from typing import Optional

from database.repository import contenido_repository
from utils.logger import logger


def get_hotel_name_from_documents() -> str:
    """Obtiene el nombre del hotel desde la base de datos"""
    try:
        # Buscar información del hotel
        info_hotel = contenido_repository.obtener_por_categoria('informacion')

        for item in info_hotel:
            contenido = item['contenido'].upper()
            if 'HOTEL' in contenido:
                # Extraer nombre del hotel
                lineas = item['contenido'].split('\n')
                for linea in lineas:
                    if 'HOTEL' in linea.upper() and len(linea.strip()) < 100:
                        # Limpiar la línea del nombre del hotel
                        nombre = linea.strip()
                        nombre = nombre.replace('HOTEL', '').replace('Hotel', '').strip()
                        if nombre and len(nombre) > 2:
                            return f"Hotel {nombre}"

        # Si no se encuentra, usar el primer título de información
        if info_hotel:
            return info_hotel[0]['titulo']

        return "Nuestro Hotel"

    except Exception as e:
        logger.error(f"❌ Error obteniendo nombre del hotel desde BD: {e}")
        return "Nuestro Hotel"


def get_contact_snippet_from_db() -> Optional[str]:
    """Obtiene un snippet corto de contacto"""
    try:
        info_contacto = contenido_repository.buscar_contenido('teléfono')
        if info_contacto:
            contenido = info_contacto[0]['contenido']
            # Extraer líneas relevantes
            lineas = contenido.split('\n')
            snippet = ""
            for linea in lineas[:3]:  # Primeras 3 líneas
                if linea.strip() and any(char.isdigit() for char in linea):
                    snippet += linea.strip() + "\n"

            return snippet.strip() if snippet else None

        return None

    except Exception as e:
        logger.error(f"❌ Error obteniendo snippet de contacto: {e}")
        return None


def get_time_based_greeting() -> str:
    """Genera saludo basado en la hora del día"""
    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        return "¡Buenos días!"
    elif 12 <= hour < 18:
        return "¡Buenas tardes!"
    else:
        return "¡Buenas noches!"


def get_default_welcome() -> str:
    """Respuesta de bienvenida por defecto"""
    greeting = get_time_based_greeting()
    return f"""🏨 **{greeting}**

¡Bienvenido a nuestro hotel! Soy tu asistente virtual y estoy aquí para ayudarte.

🔍 **¿En qué puedo ayudarte?**
• Información sobre habitaciones
• Servicios del hotel  
• Amenidades disponibles
• Información de contacto

💬 Solo pregúntame lo que necesites saber."""


def normalize_text(text: str) -> str:
    """
    Normaliza texto para comparaciones: minúsculas, sin acentos, sin signos de puntuación

    Args:
        text: Texto a normalizar

    Returns:
        str: Texto normalizado
    """
    if not text:
        return ""

    # Convertir a minúsculas
    text = text.lower()

    # Remover acentos
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')

    # Remover signos de puntuación y caracteres especiales, mantener solo letras y números
    text = re.sub(r'[^\w\s]', ' ', text)

    # Remover espacios extra
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def read_document_safely(file_path: str) -> str:
    """
    Lee un documento de manera segura con manejo de errores

    Args:
        file_path: Ruta del archivo

    Returns:
        str: Contenido del archivo o mensaje de error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.warning(f"⚠️ Archivo no encontrado: {file_path}")
        return f"Archivo no encontrado: {file_path}"
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            logger.error(f"❌ Error leyendo archivo {file_path}: {e}")
            return f"Error leyendo archivo: {e}"
    except Exception as e:
        logger.error(f"❌ Error general leyendo archivo {file_path}: {e}")
        return f"Error leyendo archivo: {e}"
