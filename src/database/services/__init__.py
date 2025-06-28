"""
Servicios especializados para el manejo de datos del hotel
"""

# Importar todas las funciones principales de los servicios
from .basic_info_service import (
    get_contact_snippet_from_db,
    get_default_welcome,
    get_hotel_name_from_documents,
    get_time_based_greeting,
    normalize_text,
    read_document_safely,
)
from .contact_service import get_contact_info_from_documents, get_reservation_info
from .facility_service import (
    get_amenities_info_from_documents,
    get_restaurant_info_from_documents,
)
from .price_search_service import extract_price_from_query, get_room_by_price
from .room_service import (
    get_cheapest_room_info,
    get_most_expensive_room_info,
    get_room_info_from_documents,
    get_rooms_with_prices,
)
from .welcome_service import get_smart_welcome_response

# Exportar todas las funciones para mantener compatibilidad
__all__ = [
    # Información básica y utilidades
    'get_hotel_name_from_documents',
    'get_contact_snippet_from_db',
    'get_time_based_greeting',
    'get_default_welcome',
    'normalize_text',
    'read_document_safely',

    # Bienvenida
    'get_smart_welcome_response',

    # Habitaciones
    'get_room_info_from_documents',
    'get_cheapest_room_info',
    'get_most_expensive_room_info',
    'get_rooms_with_prices',

    # Contacto y reservas
    'get_contact_info_from_documents',
    'get_reservation_info',

    # Restaurantes y amenidades
    'get_restaurant_info_from_documents',
    'get_amenities_info_from_documents',

    # Búsqueda por precio
    'get_room_by_price',
    'extract_price_from_query',
]
