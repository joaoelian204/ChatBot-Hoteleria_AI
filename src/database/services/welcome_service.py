"""
Servicio especializado en respuestas de bienvenida inteligentes
"""
from datetime import datetime

from database.services.basic_info_service import (
    get_contact_snippet_from_db,
    get_default_welcome,
    get_hotel_name_from_documents,
    get_time_based_greeting,
)
from utils.logger import logger


def get_smart_welcome_response(user_input: str = "") -> str:
    """Genera una respuesta de bienvenida inteligente usando datos de la BD"""
    try:
        greeting = get_time_based_greeting()
        hotel_name = get_hotel_name_from_documents()

        # Emojis según la hora
        emoji, time_message = _get_time_based_emoji_and_message()

        response = f"{emoji} **{greeting}**\n\n"
        response += f"🏨 **¡Bienvenido a {hotel_name}!**\n\n"
        response += f"💫 {time_message}. Soy tu asistente virtual y estoy aquí para ayudarte.\n\n"

        response += "🔍 **¿En qué puedo ayudarte hoy?**\n\n"
        response += _get_services_section()
        response += _get_examples_section()

        # Agregar contacto rápido
        contact_snippet = get_contact_snippet_from_db()
        if contact_snippet:
            response += f"📱 **Contacto directo:**\n{contact_snippet}"

        return response

    except Exception as e:
        logger.error(f"❌ Error generando bienvenida desde BD: {e}")
        return get_default_welcome()


# ===== FUNCIONES AUXILIARES PRIVADAS =====

def _get_time_based_emoji_and_message() -> tuple:
    """Obtiene emoji y mensaje basado en la hora del día"""
    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        emoji = "🌅"
        time_message = "Esperamos que tengas un excelente día"
    elif 12 <= hour < 18:
        emoji = "☀️"
        time_message = "Esperamos que estés teniendo una buena tarde"
    else:
        emoji = "🌙"
        time_message = "Esperamos que tengas una agradable noche"

    return emoji, time_message


def _get_services_section() -> str:
    """Obtiene la sección de servicios disponibles"""
    return """📋 **Servicios disponibles:**
• 🏠 **Habitaciones** - Tipos, precios y disponibilidad
• 🍽️ **Restaurantes** - Menús y horarios
• 🏊 **Amenidades** - Piscina, spa, actividades
• 📞 **Contacto** - Reservas e información

"""


def _get_examples_section() -> str:
    """Obtiene la sección de ejemplos de consultas"""
    return """💬 **Ejemplos de consultas:**
• '¿Cuál es la habitación más barata?'
• 'Información sobre restaurantes'
• '¿Qué actividades tienen?'
• 'Quiero hacer una reserva'

"""
