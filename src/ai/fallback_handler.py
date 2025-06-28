"""
Manejador de respuestas por defecto
SIMPLIFICADO - Proxy directo a base de datos SQLite con normalización de texto
"""

# Importar todas las funciones directamente desde la base de datos
from database.fallback_main import (
    extract_price_from_query,
    get_amenities_info_from_documents,
    get_cheapest_room_info,
    get_contact_info_from_documents,
    get_most_expensive_room_info,
    get_reservation_info,
    get_restaurant_info_from_documents,
    get_room_by_price,
    get_room_info_from_documents,
    get_smart_welcome_response,
)
from utils.logger import logger
from utils.text_processor import normalize_text

logger.info(
    "🗄️ Fallback handler usando base de datos SQLite con normalización de texto")


def generate_fallback_response(question: str) -> str:
    """
    Genera una respuesta de fallback usando la base de datos
    con normalización de texto para mejorar la coincidencia
    """
    # Normalizar el texto para una mejor coincidencia
    normalized_question = normalize_text(question)

    # Detectar consultas sobre precios específicos
    price = extract_price_from_query(question)
    if price > 0:
        return get_room_by_price(price)

    # Detectar consultas específicas sobre reservas
    reservation_keywords = [
        'reserva', 'reservar', 'reservacion', 'booking', 'book',
        'quiero reservar', 'hacer reserva', 'como reservar',
        'informacion reservas', 'contacto reservas'
    ]
    if any(keyword in normalized_question for keyword in reservation_keywords):
        return get_reservation_info()

    # Detectar consultas específicas sobre habitaciones más baratas
    cheap_keywords = [
        'habitacion mas barata', 'cuarto mas barato', 'room mas barato',
        'habitacion economica', 'cuarto economico', 'habitacion barata',
        'cuarto barato', 'room barato', 'la mas barata', 'el mas barato',
        'cheapest room', 'cheapest habitacion', 'cual es la barata',
        'cual es la mas barata', 'cual es el mas barato', 'la barata',
        'el barato', 'mas barata', 'mas barato', 'cual barata',
        'que barata', 'habitaciones baratas', 'cuartos baratos'
    ]
    if any(keyword in normalized_question for keyword in cheap_keywords):
        return get_cheapest_room_info()

    # Detectar consultas específicas sobre habitaciones más caras
    expensive_keywords = [
        'habitacion mas cara', 'cuarto mas caro', 'room mas caro',
        'habitacion lujosa', 'cuarto lujoso', 'habitacion cara',
        'cuarto caro', 'room caro', 'la mas cara', 'el mas caro',
        'suite', 'lujo', 'premium', 'executive', 'deluxe',
        'most expensive', 'expensive room', 'luxury room',
        'cual es la cara', 'cual es la mas cara', 'cual es el mas caro',
        'la cara', 'el caro', 'mas cara', 'mas caro', 'cual cara',
        'que cara', 'habitaciones caras', 'cuartos caros', 'lujosa'
    ]
    if any(keyword in normalized_question for keyword in expensive_keywords):
        return get_most_expensive_room_info()

    # Consultas generales sobre habitaciones
    room_keywords = ['habitacion', 'cuarto', 'room', 'alojamiento', 'dormitorio', 'cama']
    if any(keyword in normalized_question for keyword in room_keywords):
        return get_room_info_from_documents()

    # Consultas sobre restaurantes y comida
    restaurant_keywords = ['restaurante', 'comida', 'restaurant', 'menu', 'gastronomia', 'cena', 'almuerzo', 'desayuno']
    if any(keyword in normalized_question for keyword in restaurant_keywords):
        return get_restaurant_info_from_documents()

    # Consultas sobre amenidades
    amenity_keywords = ['amenidad', 'piscina', 'spa', 'actividad', 'gimnasio', 'servicio', 'entretenimiento']
    if any(keyword in normalized_question for keyword in amenity_keywords):
        return get_amenities_info_from_documents()

    # Consultas sobre contacto
    contact_keywords = ['contacto', 'telefono', 'email', 'llamar', 'direccion', 'ubicacion']
    if any(keyword in normalized_question for keyword in contact_keywords):
        return get_contact_info_from_documents()

    # Respuesta por defecto
    return get_smart_welcome_response(question)


def get_welcome_info_from_documents() -> str:
    """Alias para compatibilidad"""
    return get_smart_welcome_response()


def handle_fallback(question: str) -> str:
    """Maneja respuestas de fallback - alias para compatibilidad"""
    return generate_fallback_response(question)


# Funciones adicionales para compatibilidad con callbacks.py
def get_smart_welcome_response_fallback() -> str:
    """Función de bienvenida para callbacks"""
    return get_smart_welcome_response()


def get_cheapest_room_info_fallback() -> str:
    """Función de habitación más barata para callbacks"""
    return get_cheapest_room_info()


def get_most_expensive_room_info_fallback() -> str:
    """Función de habitación más cara para callbacks"""
    return get_most_expensive_room_info()


# Exportar las funciones importadas para que estén disponibles
__all__ = [
    'generate_fallback_response',
    'get_welcome_info_from_documents',
    'handle_fallback',
    'get_smart_welcome_response_fallback',
    'get_amenities_info_from_documents',
    'get_cheapest_room_info',
    'get_contact_info_from_documents',
    'get_most_expensive_room_info',
    'get_restaurant_info_from_documents',
    'get_room_info_from_documents',
    'get_smart_welcome_response',
]


def get_greeting_response() -> str:
    """Respuesta de saludo"""
    return get_smart_welcome_response()
