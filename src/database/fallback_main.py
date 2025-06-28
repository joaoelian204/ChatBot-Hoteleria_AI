"""
Manejador principal de respuestas usando base de datos SQLite (MODULARIZADO)

Este archivo ahora actúa como orquestador/importador de los servicios especializados.
Todas las funciones específicas han sido movidas a módulos especializados para 
mejor mantenibilidad y organización.
"""

# Importar todas las funciones desde los servicios modulares
# pylint: disable=unused-import
from database.services import (
    extract_price_from_query,
    get_amenities_info_from_documents,
    get_cheapest_room_info,
    # Contacto y reservas
    get_contact_info_from_documents,
    get_contact_snippet_from_db,
    get_default_welcome,
    # Información básica y utilidades
    get_hotel_name_from_documents,
    get_most_expensive_room_info,
    get_reservation_info,
    # Restaurantes y amenidades
    get_restaurant_info_from_documents,
    # Búsqueda por precio
    get_room_by_price,
    # Habitaciones
    get_room_info_from_documents,
    get_rooms_with_prices,
    # Bienvenida
    get_smart_welcome_response,
    get_time_based_greeting,
    normalize_text,
    read_document_safely,
)
from utils.logger import logger

# Logging para indicar que el sistema está completamente modularizado
logger.info("🔧 Sistema de fallback modularizado cargado correctamente")
logger.info("📁 Funciones organizadas en servicios especializados:")
logger.info("   • basic_info_service: Información básica y utilidades")
logger.info("   • welcome_service: Mensajes de bienvenida")
logger.info("   • room_service: Gestión de habitaciones")
logger.info("   • contact_service: Información de contacto y reservas")
logger.info("   • facility_service: Restaurantes y amenidades")
logger.info("   • price_search_service: Búsqueda por precios")
logger.info("🗄️ Base de datos SQLite como método principal")

# Mantener compatibilidad hacia atrás - todas las funciones están disponibles
# con los mismos nombres que antes, pero ahora importadas desde módulos especializados

# Las funciones principales que usa el sistema están ahora modularizadas:

# SERVICIO DE BIENVENIDA:
# - get_smart_welcome_response()     → welcome_service.py
# - get_default_welcome()            → basic_info_service.py
# - get_time_based_greeting()        → basic_info_service.py

# SERVICIO DE HABITACIONES:
# - get_room_info_from_documents()   → room_service.py
# - get_cheapest_room_info()         → room_service.py
# - get_most_expensive_room_info()   → room_service.py
# - get_rooms_with_prices()          → room_service.py

# SERVICIO DE CONTACTO:
# - get_contact_info_from_documents() → contact_service.py
# - get_reservation_info()            → contact_service.py

# SERVICIO DE AMENIDADES Y RESTAURANTES:
# - get_restaurant_info_from_documents() → facility_service.py
# - get_amenities_info_from_documents()  → facility_service.py

# SERVICIO DE PRECIOS:
# - get_room_by_price()              → price_search_service.py
# - extract_price_from_query()       → price_search_service.py

# SERVICIO DE INFORMACIÓN BÁSICA:
# - get_hotel_name_from_documents()  → basic_info_service.py
# - get_contact_snippet_from_db()    → basic_info_service.py
# - normalize_text()                 → basic_info_service.py
# - read_document_safely()           → basic_info_service.py


def get_module_info() -> str:
    """
    Función informativa sobre la modularización del sistema

    Returns:
        str: Información sobre la organización modular
    """
    return """🔧 **SISTEMA MODULARIZADO**
═══════════════════════════════════════

✅ **Estado:** Completamente refactorizado

📁 **Estructura de módulos:**

🏠 **room_service.py**
   • Gestión completa de habitaciones
   • Búsqueda por precio, más baratas/caras
   • Metadatos y formateo elegante

🏨 **welcome_service.py**
   • Mensajes de bienvenida inteligentes
   • Detección de hora del día
   • Personalización contextual

📞 **contact_service.py**
   • Información de contacto
   • Gestión de reservas
   • Políticas y procedimientos

🏊 **facility_service.py**
   • Restaurantes y menús
   • Amenidades robustas con manejo de errores
   • Categorización automática con emojis

💰 **price_search_service.py**
   • Extracción inteligente de precios
   • Búsqueda exacta y aproximada
   • Tolerancia configurable

ℹ️ **basic_info_service.py**
   • Funciones utilitarias
   • Normalización de texto
   • Información básica del hotel

💫 **Beneficios de la modularización:**
   • Mayor mantenibilidad
   • Código más organizado
   • Fácil testing independiente
   • Reutilización de componentes
   • Separación de responsabilidades

🔗 **Compatibilidad:** 100% hacia atrás
   • Todas las funciones mantienen sus nombres
   • Sin cambios en la API externa
   • Importación transparente"""


# Ejemplo de uso modular (para testing y documentación)
if __name__ == "__main__":
    # Demostrar que todas las funciones están disponibles
    print("🔧 Testing modularización...")

    try:
        # Test funciones básicas
        hotel_name = get_hotel_name_from_documents()
        print(f"✅ Hotel: {hotel_name}")

        # Test normalización
        test_text = normalize_text("¡Hóla Múndo!")
        print(f"✅ Normalización: '{test_text}'")

        # Test saludo
        greeting = get_time_based_greeting()
        print(f"✅ Saludo: {greeting}")

        print("🎉 ¡Modularización completada exitosamente!")

    except Exception as e:
        print(f"❌ Error en testing: {e}")


# Exposición explícita de todas las funciones para compatibilidad hacia atrás
# Esto asegura que todas las importaciones sean reconocidas como usadas
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

    # Función informativa
    'get_module_info',
]
