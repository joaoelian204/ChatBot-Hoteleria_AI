"""
Servicio especializado en información de contacto y reservas
"""
from database.repository import contenido_repository
from utils.logger import logger


def get_contact_info_from_documents() -> str:
    """Obtiene información de contacto desde la base de datos"""
    try:
        # Buscar información de contacto
        info_contacto = contenido_repository.buscar_contenido('contacto')
        if not info_contacto:
            info_contacto = contenido_repository.buscar_contenido('teléfono')
        if not info_contacto:
            info_contacto = contenido_repository.buscar_contenido('reservas')

        if not info_contacto:
            return """📞 **INFORMACIÓN DE CONTACTO**
═══════════════════════════════════════

⚠️ **Información de contacto no disponible**

Por favor contacta a la recepción del hotel para obtener los datos actualizados."""

        response = "📞 **INFORMACIÓN DE CONTACTO**\n"
        response += "═" * 40 + "\n\n"

        for item in info_contacto:
            titulo = item.get('titulo', 'Contacto')
            contenido = item.get('contenido', '')

            response += f"📋 **{titulo}**\n"
            response += "─" * (len(titulo) + 4) + "\n"

            # Procesar el contenido línea por línea para mejor formato
            lineas = contenido.split('\n')
            for linea in lineas:
                linea = linea.strip()
                if linea:
                    # Agregar emojis según el tipo de información
                    if any(word in linea.lower() for word in ['teléfono', 'tel', 'phone']):
                        response += f"📱 {linea}\n"
                    elif any(word in linea.lower() for word in ['email', 'correo', '@']):
                        response += f"📧 {linea}\n"
                    elif any(word in linea.lower() for word in ['dirección', 'direccion', 'address']):
                        response += f"📍 {linea}\n"
                    elif any(word in linea.lower() for word in ['horario', 'hora', 'abierto']):
                        response += f"🕐 {linea}\n"
                    elif any(word in linea.lower() for word in ['web', 'www', 'http']):
                        response += f"🌐 {linea}\n"
                    else:
                        response += f"ℹ️ {linea}\n"

            response += "\n"

        # Obtener metadatos adicionales
        metadatos = info_contacto[0].get('metadatos', {})
        if metadatos:
            response += "📊 **Información Adicional:**\n"
            for key, value in metadatos.items():
                if value:
                    response += f"• **{key.title()}:** {value}\n"
            response += "\n"

        response += "═" * 40 + "\n"
        response += "💬 **¡Estamos aquí para ayudarte!**"

        return response

    except Exception as e:
        logger.error(f"❌ Error obteniendo información de contacto desde BD: {e}")
        return """📞 **INFORMACIÓN DE CONTACTO**
═══════════════════════════════════════

❌ **Error temporal**

No pudimos obtener la información de contacto en este momento. 
Por favor intenta nuevamente o contacta directamente a la recepción."""


def get_reservation_info() -> str:
    """Obtiene información sobre reservas y políticas"""
    try:
        # Buscar información específica de reservas
        info_reservas = contenido_repository.buscar_contenido('reserva')
        if not info_reservas:
            info_reservas = contenido_repository.buscar_contenido('booking')
        if not info_reservas:
            info_reservas = contenido_repository.buscar_contenido('política')

        if not info_reservas:
            # Información por defecto si no hay datos específicos
            return """📅 **RESERVAS E INFORMACIÓN**
═══════════════════════════════════════

🎯 **¿Cómo hacer una reserva?**

📞 **Por teléfono:**
• Llama a recepción durante horario de atención
• Proporciona fechas de entrada y salida
• Especifica número de huéspedes

📧 **Por email:**
• Envía un correo con tus datos
• Incluye fechas y preferencias
• Te responderemos en 24 horas

🏨 **En persona:**
• Visita nuestra recepción
• Atención personalizada
• Confirmación inmediata

═══════════════════════════════════════
💡 **¿Necesitas más información?** Pregunta por nuestros servicios específicos."""

        response = "📅 **RESERVAS E INFORMACIÓN**\n"
        response += "═" * 40 + "\n\n"

        for item in info_reservas:
            titulo = item.get('titulo', 'Información de Reservas')
            contenido = item.get('contenido', '')

            response += f"📋 **{titulo}**\n"
            response += "─" * (len(titulo) + 4) + "\n"

            # Procesar contenido con formato mejorado
            lineas = contenido.split('\n')
            for linea in lineas:
                linea = linea.strip()
                if linea:
                    # Agregar iconos según el contexto
                    if any(word in linea.lower() for word in ['cancelación', 'cancelacion', 'cancel']):
                        response += f"❌ {linea}\n"
                    elif any(word in linea.lower() for word in ['política', 'politica', 'policy']):
                        response += f"📋 {linea}\n"
                    elif any(word in linea.lower() for word in ['precio', 'costo', 'tarifa']):
                        response += f"💰 {linea}\n"
                    elif any(word in linea.lower() for word in ['check-in', 'entrada', 'llegada']):
                        response += f"🔑 {linea}\n"
                    elif any(word in linea.lower() for word in ['check-out', 'salida']):
                        response += f"🚪 {linea}\n"
                    elif any(word in linea.lower() for word in ['horario', 'hora']):
                        response += f"🕐 {linea}\n"
                    else:
                        response += f"ℹ️ {linea}\n"

            response += "\n"

        # Información de contacto para reservas
        contacto_info = contenido_repository.buscar_contenido('teléfono')
        if contacto_info:
            response += "📞 **Contacto para Reservas:**\n"
            # Extraer solo la información relevante de contacto
            contenido_contacto = contacto_info[0]['contenido']
            lineas = contenido_contacto.split('\n')
            for linea in lineas[:2]:  # Solo primeras 2 líneas
                if linea.strip() and any(char.isdigit() for char in linea):
                    response += f"📱 {linea.strip()}\n"
            response += "\n"

        response += "═" * 40 + "\n"
        response += "🎉 **¡Esperamos recibirte pronto!**"

        return response

    except Exception as e:
        logger.error(f"❌ Error obteniendo información de reservas: {e}")
        return """📅 **RESERVAS E INFORMACIÓN**
═══════════════════════════════════════

❌ **Error temporal**

No pudimos obtener la información de reservas en este momento.
Por favor contacta directamente a recepción para hacer tu reserva.

📞 **Contacto directo recomendado**"""
