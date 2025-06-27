"""
Manejador de respuestas por defecto y fallback
Extrae información directamente de los documentos del hotel
"""

import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from utils.logger import logger


def find_documents_directory() -> Path:
    """Busca dinámicamente el directorio de documentos"""
    # Empezar desde el directorio actual
    current_dir = Path(__file__).parent

    # Buscar hacia arriba hasta encontrar la carpeta documentos
    for i in range(5):  # Buscar máximo 5 niveles arriba
        search_dir = current_dir
        for _ in range(i):
            search_dir = search_dir.parent

        docs_dir = search_dir / "documentos"
        if docs_dir.exists() and docs_dir.is_dir():
            logger.info(f"Directorio de documentos encontrado en: {docs_dir}")
            return docs_dir

    # Si no se encuentra, buscar en directorios comunes
    possible_paths = [
        Path("documentos"),
        Path("../documentos"),
        Path("../../documentos"),
        Path("docs"),
        Path("../docs"),
        Path("../../docs"),
    ]

    for path in possible_paths:
        if path.exists() and path.is_dir():
            logger.info(f"Directorio de documentos encontrado en: {path}")
            return path

    logger.warning("No se pudo encontrar el directorio de documentos")
    return Path("documentos")  # Fallback


def find_document_file(filename: str) -> Path:
    """Busca un archivo específico en el directorio de documentos"""
    docs_dir = find_documents_directory()
    file_path = docs_dir / filename

    if file_path.exists():
        return file_path

    # Si no se encuentra, buscar el archivo por nombre en varios directorios
    search_dirs = [
        Path("."),
        Path(".."),
        Path("../.."),
        docs_dir,
    ]

    for search_dir in search_dirs:
        if search_dir.exists():
            # Buscar recursivamente el archivo
            for root, dirs, files in os.walk(search_dir):
                if filename in files:
                    found_path = Path(root) / filename
                    logger.info(f"Documento {filename} encontrado en: {found_path}")
                    return found_path

    logger.warning(f"No se pudo encontrar el archivo: {filename}")
    return docs_dir / filename  # Fallback


def read_document_safely(filename: str) -> str:
    """Lee un documento de manera segura, manejando errores"""
    try:
        file_path = find_document_file(filename)

        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Documento {filename} leído exitosamente")
            return content.strip()
        else:
            logger.error(f"Archivo no encontrado: {file_path}")
            return ""
    except Exception as e:
        logger.error(f"Error al leer {filename}: {e}")
        return ""


def get_time_based_greeting() -> str:
    """Genera un saludo basado en la hora actual"""
    now = datetime.now()
    hour = now.hour

    if 5 <= hour < 12:
        return "¡Buenos días!"
    elif 12 <= hour < 18:
        return "¡Buenas tardes!"
    else:
        return "¡Buenas noches!"


def get_smart_welcome_response(user_input: str = "") -> str:
    """Genera una respuesta de bienvenida inteligente basada en la hora"""
    try:
        greeting = get_time_based_greeting()
        hotel_name = get_hotel_name_from_documents()

        # Emojis según la hora
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

        response = f"{emoji} **{greeting}**\n\n"
        response += f"🏨 **¡Bienvenido a {hotel_name}!**\n\n"
        response += f"💫 {time_message}. Soy tu asistente virtual y estoy aquí para ayudarte.\n\n"

        response += "🔍 **¿En qué puedo ayudarte hoy?**\n\n"
        response += "📋 **Servicios disponibles:**\n"
        response += "• 🏠 **Habitaciones** - Tipos, precios y disponibilidad\n"
        response += "• 🍽️ **Restaurantes** - Menús y horarios\n"
        response += "• 🏊 **Amenidades** - Piscina, spa, actividades\n"
        response += "• 📞 **Contacto** - Reservas y información\n\n"

        response += "💬 **Ejemplos de consultas:**\n"
        response += "• '¿Cuál es la habitación más barata?'\n"
        response += "• 'Información sobre restaurantes'\n"
        response += "• '¿Qué actividades tienen?'\n"
        response += "• 'Quiero hacer una reserva'\n\n"

        # Agregar contacto rápido
        contact_snippet = get_contact_snippet()
        if contact_snippet:
            response += f"📱 **Contacto directo:**\n{contact_snippet[:100]}..."

        return response

    except Exception as e:
        logger.error(f"Error en smart welcome: {e}")
        return get_welcome_info_from_documents()


def normalize_text(text: str) -> str:
    """Normaliza texto removiendo acentos y caracteres especiales"""
    # Convertir a minúsculas
    text = text.lower()
    # Remover acentos
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii')
    # Remover signos de puntuación comunes
    text = text.replace('?', '').replace('¿', '').replace('!', '').replace('¡', '').replace(',', '').replace('.', '')
    return text.strip()


def generate_fallback_response(question: str) -> str:
    """Genera respuesta extrayendo información directamente de los documentos"""
    try:
        # Usar el detector de intenciones avanzado
        from ai.intent_detector import detect_intent as detect_advanced_intent
        
        intent, confidence = detect_advanced_intent(question)
        logger.info(f"Intención detectada: {intent} (confianza: {confidence})")
        
        # Si la confianza es alta, usar el intent detectado
        if confidence > 0:
            if intent == 'economic_room':
                return get_cheapest_room_info()
            elif intent == 'expensive_room':
                return get_most_expensive_room_info()
            elif intent == 'rooms_with_prices' or intent == 'pricing':
                return get_room_info_from_documents()
            elif intent == 'restaurants':
                return get_restaurant_info_from_documents()
            elif intent == 'amenities':
                return get_amenities_info_from_documents()
            elif intent == 'contact':
                return get_contact_info_from_documents()
        
        # Fallback a detección manual si el intent_detector no tiene confianza
        query_normalized = normalize_text(question)

        # Detectar saludos (prioridad alta)
        greeting_keywords = ['hola', 'buenos dias', 'buenas tardes', 'buenas noches', 'buen dia', 'buena tarde', 'buena noche', 'saludos', 'hello', 'hi']
        if any(greeting in query_normalized for greeting in greeting_keywords):
            return get_smart_welcome_response(question)

        # Detectar consultas específicas sobre habitación más barata/económica
        elif any(phrase in query_normalized for phrase in ['mas barata', 'mas economica', 'habitacion barata', 'habitacion economica', 'menor precio', 'precio bajo', 'mas chevere', 'mas accesible']):
            return get_cheapest_room_info()
        # Detectar consultas sobre habitación más cara/costosa
        elif any(phrase in query_normalized for phrase in ['mas cara', 'mas costosa', 'mas costoso', 'habitacion cara', 'habitacion costosa', 'mayor precio', 'precio alto', 'mas lujosa', 'presidencial', 'lujosa', 'cara que tengan', 'mas lujosa o cara']):
            return get_most_expensive_room_info()
        # Detectar consultas sobre menús/restaurantes (mejorado)
        elif any(phrase in query_normalized for phrase in ['precios de menu', 'precios menu', 'precios de menus', 'precios menus', 'precios de los menu', 'precios de los menus', 'menu del restaurante', 'menus restaurante', 'carta restaurante', 'precios comida', 'menu precios', 'menus precios']):
            return get_restaurant_info_from_documents()
        elif any(word in query_normalized for word in ['habitacion', 'cuarto', 'room', 'suite', 'dormir', 'cama', 'precio', 'tarifa', 'economica', 'barata', 'barato']):
            return get_room_info_from_documents()
        elif any(word in query_normalized for word in ['restaurante', 'comida', 'comer', 'menu', 'gastronomia', 'desayuno', 'almuerzo', 'cena']):
            return get_restaurant_info_from_documents()
        elif any(word in query_normalized for word in ['amenidades', 'actividades', 'piscina', 'spa', 'gym', 'deporte']):
            return get_amenities_info_from_documents()
        elif any(word in query_normalized for word in ['contacto', 'telefono', 'reserva', 'ubicacion', 'direccion', 'email']):
            return get_contact_info_from_documents()
        elif any(word in query_normalized for word in ['start', 'inicio', 'bienvenido', 'ayuda', 'help']):
            return get_smart_welcome_response(question)
        else:
            return get_general_info_from_documents()

    except Exception as e:
        logger.error(f"Error en fallback response: {e}")
        return get_general_info_from_documents()


def get_room_info_from_documents() -> str:
    """Extrae información de habitaciones directamente de los documentos"""
    try:
        content = read_document_safely("habitaciones_precios.txt")

        if content:
            # Formatear la información
            response = "🏠 **Habitaciones Disponibles**\n\n"
            response += content

            # Agregar información de contacto si está disponible
            contact_info = get_contact_snippet()
            if contact_info:
                response += f"\n\n📞 **Para reservas:**\n{contact_info}"

            return response
        else:
            return "❌ Información de habitaciones no disponible temporalmente."
    except Exception as e:
        logger.error(f"Error al leer habitaciones: {e}")
        return "❌ Error al obtener información de habitaciones."


def get_cheapest_room_info() -> str:
    """Extrae información de la habitación más económica"""
    try:
        content = read_document_safely("habitaciones_precios.txt")

        if content:
            # Buscar precios en el contenido
            lines = content.split('\n')
            rooms_with_prices = []
            current_room = ""

            for line in lines:
                line = line.strip()
                # Solo considerar líneas que empiecen directamente con HABITACIÓN o SUITE (sin guión)
                if (line.startswith('HABITACIÓN') or line.startswith('SUITE')) and not line.startswith('-'):
                    current_room = line
                elif 'Precio:' in line and '$' in line and current_room:
                    # Extraer precio numérico solo de líneas que dicen "Precio:"
                    price_match = re.search(r'\$(\d+)', line)
                    if price_match:
                        price = int(price_match.group(1))
                        rooms_with_prices.append((current_room, price, line))

            if rooms_with_prices:
                # Encontrar la habitación más barata
                cheapest = min(rooms_with_prices, key=lambda x: x[1])

                # Agregar saludo contextual al inicio
                greeting = get_time_based_greeting()
                response = f"✨ {greeting}\n\n💰 **Habitación Más Económica**\n\n"
                response += f"🏠 **{cheapest[0]}**\n"
                response += f"💵 **{cheapest[2]}**\n\n"
                response += "✨ Esta es nuestra opción más económica.\n\n"

                # Mostrar solo los detalles de la habitación más barata
                lines = content.split('\n')
                room_details = []
                in_cheapest_room = False

                for line in lines:
                    line_strip = line.strip()
                    if cheapest[0] in line_strip:
                        in_cheapest_room = True
                        continue
                    elif in_cheapest_room and line_strip:
                        # Parar si encontramos otra habitación
                        if (line_strip.startswith('HABITACIÓN') or line_strip.startswith('SUITE')) and not line_strip.startswith('-'):
                            break
                        # Parar si llegamos a una sección diferente
                        if 'SERVICIOS INCLUIDOS' in line_strip.upper() or 'POLÍTICAS' in line_strip.upper():
                            break
                        room_details.append(line)
                    elif in_cheapest_room and not line_strip:
                        break

                if room_details:
                    response += "📋 **Detalles de la habitación:**\n"
                    response += '\n'.join(room_details).strip()

                # Agregar contacto
                contact_info = get_contact_snippet()
                if contact_info:
                    response += f"\n\n📞 **Para reservas:**\n{contact_info}"

                return response
            else:
                # Si no encuentra precios específicos, devolver info completa
                return get_room_info_from_documents()
        else:
            return "❌ Información de habitaciones no disponible temporalmente."
    except Exception as e:
        logger.error(f"Error al buscar habitación más económica: {e}")
        return get_room_info_from_documents()


def get_most_expensive_room_info() -> str:
    """Extrae información de la habitación más costosa"""
    try:
        content = read_document_safely("habitaciones_precios.txt")

        if content:
            # Buscar precios en el contenido
            lines = content.split('\n')
            rooms_with_prices = []
            current_room = ""

            for line in lines:
                line = line.strip()
                # Solo considerar líneas que empiecen directamente con HABITACIÓN o SUITE (sin guión)
                if (line.startswith('HABITACIÓN') or line.startswith('SUITE')) and not line.startswith('-'):
                    current_room = line
                elif 'Precio:' in line and '$' in line and current_room:
                    # Extraer precio numérico solo de líneas que dicen "Precio:"
                    price_match = re.search(r'\$(\d+)', line)
                    if price_match:
                        price = int(price_match.group(1))
                        rooms_with_prices.append((current_room, price, line))

            if rooms_with_prices:
                # Encontrar la habitación más cara
                most_expensive = max(rooms_with_prices, key=lambda x: x[1])

                # Agregar saludo contextual al inicio
                greeting = get_time_based_greeting()
                response = f"✨ {greeting}\n\n💎 **Habitación Más Lujosa**\n\n"
                response += f"🏠 **{most_expensive[0]}**\n"
                response += f"💵 **{most_expensive[2]}**\n\n"
                response += "✨ Esta es nuestra opción más exclusiva y lujosa.\n\n"

                # Mostrar solo los detalles de la habitación más cara
                lines = content.split('\n')
                room_details = []
                in_expensive_room = False
                
                for line in lines:
                    line_strip = line.strip()
                    if most_expensive[0] in line_strip:
                        in_expensive_room = True
                        continue
                    elif in_expensive_room and line_strip:
                        # Parar si encontramos otra habitación
                        if (line_strip.startswith('HABITACIÓN') or line_strip.startswith('SUITE')) and not line_strip.startswith('-'):
                            break
                        # Parar si llegamos a una sección diferente
                        if 'SERVICIOS INCLUIDOS' in line_strip.upper() or 'POLÍTICAS' in line_strip.upper():
                            break
                        room_details.append(line)
                    elif in_expensive_room and not line_strip:
                        break

                if room_details:
                    response += "📋 **Detalles de la habitación:**\n"
                    response += '\n'.join(room_details).strip()

                # Agregar contacto
                contact_info = get_contact_snippet()
                if contact_info:
                    response += f"\n\n📞 **Para reservas:**\n{contact_info}"

                return response
            else:
                # Si no encuentra precios específicos, devolver info completa
                return get_room_info_from_documents()
        else:
            return "❌ Información de habitaciones no disponible temporalmente."
    except Exception as e:
        logger.error(f"Error al buscar habitación más costosa: {e}")
        return get_room_info_from_documents()


def get_restaurant_info_from_documents() -> str:
    """Extrae información de restaurantes directamente de los documentos"""
    try:
        content = read_document_safely("restaurantes_menus.txt")

        if content:
            response = "🍽️ **Restaurantes y Menús**\n\n"
            response += content
            return response
        else:
            return "❌ Información de restaurantes no disponible temporalmente."
    except Exception as e:
        logger.error(f"Error al leer restaurantes: {e}")
        return "❌ Error al obtener información de restaurantes."


def get_amenities_info_from_documents() -> str:
    """Extrae información de amenidades directamente de los documentos"""
    try:
        content = read_document_safely("amenidades_actividades.txt")

        if content:
            response = "🏊 **Amenidades y Actividades**\n\n"
            response += content
            return response
        else:
            return "❌ Información de amenidades no disponible temporalmente."
    except Exception as e:
        logger.error(f"Error al leer amenidades: {e}")
        return "❌ Error al obtener información de amenidades."


def get_contact_info_from_documents() -> str:
    """Extrae información de contacto directamente de los documentos"""
    try:
        content = read_document_safely("hotel_info.txt")

        if content:
            # Buscar sección de contacto
            lines = content.split('\n')
            contact_section = []
            in_contact_section = False

            for line in lines:
                if 'CONTACTO' in line.upper() or 'TELÉFONO' in line.upper() or 'EMAIL' in line.upper():
                    in_contact_section = True
                    contact_section.append(line)
                elif in_contact_section and line.strip():
                    contact_section.append(line)
                elif in_contact_section and not line.strip():
                    break

            if contact_section:
                response = "📞 **Información de Contacto**\n\n"
                response += '\n'.join(contact_section)
                return response
            else:
                response = "📞 **Información de Contacto**\n\n"
                response += content
                return response
        else:
            return "❌ Información de contacto no disponible temporalmente."
    except Exception as e:
        logger.error(f"Error al leer contacto: {e}")
        return "❌ Error al obtener información de contacto."


def get_welcome_info_from_documents() -> str:
    """Extrae información de bienvenida directamente de los documentos"""
    try:
        # Obtener nombre del hotel desde hotel_info.txt
        hotel_name = get_hotel_name_from_documents()
        content = read_document_safely("hotel_info.txt")

        if content:
            # Extraer descripción
            lines = content.split('\n')
            description = ""
            for line in lines:
                if 'DESCRIPCIÓN' in line.upper():
                    idx = lines.index(line)
                    if idx + 1 < len(lines):
                        description = lines[idx + 1].strip()
                    break

            response = f"🏨 **¡Bienvenido a {hotel_name}!**\n\n"
            if description:
                response += f"📝 {description}\n\n"

            response += "💡 **Puedo ayudarte con información sobre:**\n"
            response += "🏠 Habitaciones y precios\n"
            response += "🍽️ Restaurantes y menús\n"
            response += "🏊 Amenidades y actividades\n"
            response += "📞 Contacto y reservas\n\n"
            response += "💬 **Escribe tu pregunta o usa los comandos disponibles**"

            return response
        else:
            return "🏨 **¡Bienvenido!**\n\nSoy tu asistente virtual. ¿En qué puedo ayudarte?"
    except Exception as e:
        logger.error(f"Error al generar bienvenida: {e}")
        return "🏨 **¡Bienvenido!**\n\nSoy tu asistente virtual. ¿En qué puedo ayudarte?"


def get_general_info_from_documents() -> str:
    """Extrae información general directamente de los documentos"""
    try:
        hotel_name = get_hotel_name_from_documents()

        response = f"🏨 **{hotel_name}**\n\n"
        response += "💡 **¿En qué puedo ayudarte?**\n\n"
        response += "🔍 **Información disponible:**\n"
        response += "• 🏠 Habitaciones y precios\n"
        response += "• 🍽️ Restaurantes y menús\n"
        response += "• 🏊 Amenidades y actividades\n"
        response += "• 📞 Contacto y reservas\n\n"
        response += "💬 **Ejemplos de preguntas:**\n"
        response += "• '¿Qué tipos de habitaciones tienen?'\n"
        response += "• '¿Cuáles son sus restaurantes?'\n"
        response += "• '¿Cómo puedo hacer una reserva?'\n"
        response += "• '¿Qué actividades ofrecen?'"

        # Agregar snippet de contacto
        contact_snippet = get_contact_snippet()
        if contact_snippet:
            response += f"\n\n📱 **Contacto rápido:**\n{contact_snippet}"

        return response
    except Exception as e:
        logger.error(f"Error al generar info general: {e}")
        return "🏨 **Asistente Virtual**\n\n¿En qué puedo ayudarte hoy?"


def get_hotel_name_from_documents() -> str:
    """Extrae el nombre del hotel desde los documentos"""
    try:
        content = read_document_safely("hotel_info.txt")

        if content:
            # Buscar el nombre en la primera línea no vacía
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            if lines:
                return lines[0]

        return "Hotel"
    except Exception as e:
        logger.error(f"Error al extraer nombre del hotel: {e}")
        return "Hotel"


def get_contact_snippet() -> str:
    """Extrae un snippet de información de contacto"""
    try:
        content = read_document_safely("hotel_info.txt")

        if content:
            # Buscar teléfono y email
            lines = content.split('\n')
            contact_info = []

            for line in lines:
                line = line.strip()
                if 'teléfono' in line.lower() or 'phone' in line.lower():
                    contact_info.append(line)
                elif 'email' in line.lower() or '@' in line:
                    contact_info.append(line)
                elif 'whatsapp' in line.lower():
                    contact_info.append(line)

            return '\n'.join(contact_info[:2])  # Máximo 2 líneas

        return ""
    except Exception as e:
        logger.error(f"Error al extraer contacto snippet: {e}")
        return ""
        return ""
