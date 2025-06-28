"""
Servicio especializado en información de habitaciones
"""
import re
from typing import Any, Dict, List

from database.repository import contenido_repository
from utils.logger import logger


def get_room_info_from_documents() -> str:
    """Obtiene información de habitaciones desde la base de datos"""
    try:
        habitaciones = contenido_repository.obtener_por_categoria('habitaciones')
        if not habitaciones:
            habitaciones = contenido_repository.buscar_contenido('habitación')

        if not habitaciones:
            return """🏠 **HABITACIONES**
═══════════════════════════════════════

⚠️ **Información de habitaciones no disponible**

Por favor contacta a la recepción para información actualizada sobre nuestras habitaciones."""

        response = "🏠 **NUESTRAS HABITACIONES**\n"
        response += "═" * 40 + "\n\n"

        for i, habitacion in enumerate(habitaciones, 1):
            titulo = habitacion.get('titulo', f'Habitación {i}')
            contenido = habitacion.get('contenido', '')
            precio = habitacion.get('precio', 0)

            response += f"🛏️ **{titulo}**\n"
            response += "─" * (len(titulo) + 4) + "\n"

            # Mostrar precio si está disponible
            if precio:
                response += f"💰 **Precio:** ${precio:.0f} USD por noche\n\n"

            # Procesar contenido línea por línea
            lineas = contenido.split('\n')
            for linea in lineas:
                linea = linea.strip()
                if linea:
                    # Agregar iconos según el contenido
                    if any(word in linea.lower() for word in ['precio', 'costo', '$']):
                        response += f"💰 {linea}\n"
                    elif any(word in linea.lower() for word in ['cama', 'bed', 'doble', 'king', 'queen']):
                        response += f"🛏️ {linea}\n"
                    elif any(word in linea.lower() for word in ['baño', 'bathroom', 'ducha']):
                        response += f"🚿 {linea}\n"
                    elif any(word in linea.lower() for word in ['vista', 'view', 'mar', 'jardín']):
                        response += f"🌅 {linea}\n"
                    elif any(word in linea.lower() for word in ['wifi', 'internet', 'tv', 'aire']):
                        response += f"📺 {linea}\n"
                    elif any(word in linea.lower() for word in ['metros', 'm2', 'tamaño', 'espacio']):
                        response += f"📐 {linea}\n"
                    elif any(word in linea.lower() for word in ['huésped', 'persona', 'ocupan']):
                        response += f"👥 {linea}\n"
                    else:
                        response += f"✨ {linea}\n"

            # Mostrar metadatos si existen
            metadatos = habitacion.get('metadatos', {})
            if metadatos:
                response += "\n📊 **Detalles adicionales:**\n"
                for key, value in metadatos.items():
                    if value:
                        response += f"• **{key.title()}:** {value}\n"

            response += "\n" + "─" * 40 + "\n\n"

        response += "═" * 40 + "\n"
        response += "📞 **¿Interesado?** Contacta recepción para reservar"

        return response

    except Exception as e:
        logger.error(f"❌ Error obteniendo información de habitaciones desde BD: {e}")
        return """🏠 **HABITACIONES**
═══════════════════════════════════════

❌ **Error temporal**

No pudimos obtener la información de habitaciones en este momento.
Por favor contacta directamente a recepción."""


def get_cheapest_room_info() -> str:
    """Obtiene información de la habitación más barata"""
    try:
        habitaciones = contenido_repository.obtener_por_categoria('habitaciones')
        if not habitaciones:
            habitaciones = contenido_repository.buscar_contenido('habitación')

        if not habitaciones:
            return "🏠 **HABITACIONES**\n\nInformación de habitaciones no disponible."

        # Buscar la habitación más económica usando el campo precio directamente
        precio_min = float('inf')
        habitacion_barata = None

        for habitacion in habitaciones:
            precio = habitacion.get('precio', 0)
            if precio and precio < precio_min:
                precio_min = precio
                habitacion_barata = habitacion

        # Si no hay precios directos, buscar en el contenido
        if not habitacion_barata:
            for habitacion in habitaciones:
                contenido = habitacion['contenido'].lower()
                precios = re.findall(r'\$\s*(\d+)', contenido)
                for precio_str in precios:
                    precio = float(precio_str)
                    if precio < precio_min:
                        precio_min = precio
                        habitacion_barata = habitacion

        if habitacion_barata:
            response = "💰 **HABITACIÓN MÁS ECONÓMICA**\n"
            response += "═" * 40 + "\n\n"
            response += f"🛏️ **{habitacion_barata['titulo']}**\n"
            response += "─" * (len(habitacion_barata['titulo']) + 4) + "\n"
            response += f"💵 **Precio:** ${precio_min:.0f} USD por noche\n\n"

            # Obtener metadatos
            metadatos = habitacion_barata.get('metadatos', {})
            if metadatos:
                response += "📊 **Características principales:**\n"
                for key, value in metadatos.items():
                    if value:
                        response += f"• **{key.title()}:** {value}\n"
                response += "\n"

            # Procesar descripción
            contenido = habitacion_barata.get('contenido', '')
            if contenido:
                response += "📝 **Descripción:**\n"
                lineas = contenido.split('\n')
                for linea in lineas[:3]:  # Solo primeras 3 líneas
                    linea = linea.strip()
                    if linea and '$' not in linea:  # Evitar duplicar precio
                        response += f"✨ {linea}\n"
                response += "\n"

            response += "═" * 40 + "\n"
            response += "📞 **Reserva ahora:** Contacta recepción para disponibilidad"

            return response
        else:
            return "🏠 **HABITACIONES**\n\nNo se encontraron precios disponibles."

    except Exception as e:
        logger.error(f"❌ Error obteniendo habitación más barata: {e}")
        return "🏠 Error obteniendo información de habitaciones baratas."


def get_most_expensive_room_info() -> str:
    """Obtiene información de la habitación más cara"""
    try:
        habitaciones = contenido_repository.obtener_por_categoria('habitaciones')
        if not habitaciones:
            habitaciones = contenido_repository.buscar_contenido('habitación')

        if not habitaciones:
            return "🏠 **HABITACIONES**\n\nInformación de habitaciones no disponible."

        # Buscar la habitación más cara usando el campo precio directamente
        precio_max = 0
        habitacion_cara = None

        for habitacion in habitaciones:
            precio = habitacion.get('precio', 0)
            if precio and precio > precio_max:
                precio_max = precio
                habitacion_cara = habitacion

        # Si no hay precios directos, buscar en el contenido
        if not habitacion_cara:
            for habitacion in habitaciones:
                contenido = habitacion['contenido'].lower()
                precios = re.findall(r'\$\s*(\d+)', contenido)
                for precio_str in precios:
                    precio = float(precio_str)
                    if precio > precio_max:
                        precio_max = precio
                        habitacion_cara = habitacion

        if habitacion_cara:
            response = "👑 **HABITACIÓN MÁS LUJOSA**\n"
            response += "═" * 40 + "\n\n"
            response += f"🏨 **{habitacion_cara['titulo']}**\n"
            response += "─" * (len(habitacion_cara['titulo']) + 4) + "\n"
            response += f"💎 **Precio:** ${precio_max:.0f} USD por noche\n\n"

            # Obtener metadatos
            metadatos = habitacion_cara.get('metadatos', {})
            if metadatos:
                response += "✨ **Características exclusivas:**\n"
                for key, value in metadatos.items():
                    if value:
                        response += f"• **{key.title()}:** {value}\n"
                response += "\n"

            # Procesar descripción
            contenido = habitacion_cara.get('contenido', '')
            if contenido:
                response += "📝 **Descripción premium:**\n"
                lineas = contenido.split('\n')
                for linea in lineas[:4]:  # Primeras 4 líneas para habitación premium
                    linea = linea.strip()
                    if linea and '$' not in linea:  # Evitar duplicar precio
                        response += f"🌟 {linea}\n"
                response += "\n"

            response += "═" * 40 + "\n"
            response += "🎉 **¡Experiencia de lujo!** Contacta recepción para reservar"

            return response
        else:
            return "🏠 **HABITACIONES**\n\nNo se encontraron precios disponibles."

    except Exception as e:
        logger.error(f"❌ Error obteniendo habitación más cara: {e}")
        return "🏠 Error obteniendo información de habitaciones de lujo."


def get_rooms_with_prices() -> List[Dict[str, Any]]:
    """
    Obtiene todas las habitaciones con precios válidos

    Returns:
        List[Dict]: Lista de habitaciones con precios
    """
    try:
        habitaciones = contenido_repository.obtener_por_categoria('habitaciones')
        if not habitaciones:
            habitaciones = contenido_repository.buscar_contenido('habitación')

        rooms_with_prices = []

        for habitacion in habitaciones:
            precio = habitacion.get('precio', 0)

            # Si no hay precio directo, buscar en el contenido
            if not precio:
                contenido = habitacion.get('contenido', '')
                precios = re.findall(r'\$\s*(\d+)', contenido)
                if precios:
                    precio = float(precios[0])

            if precio and precio > 0:
                room_data = habitacion.copy()
                room_data['precio'] = precio
                rooms_with_prices.append(room_data)

        return rooms_with_prices

    except Exception as e:
        logger.error(f"❌ Error obteniendo habitaciones con precios: {e}")
        return []
