"""
Configuración para el sistema de testing universal
"""

# Configuración de dificultades de testing
DIFFICULTY_CONFIGS = {
    "easy": {
        "name": "🟢 Fácil",
        "description": "Tests básicos con pocas iteraciones",
        "stress_iterations": 10,
        "concurrent_tests": 2,
        "timeout": 5.0,
        "edge_cases": False,
        "performance_threshold": 60.0
    },
    "medium": {
        "name": "🟡 Medio",
        "description": "Tests completos con carga moderada",
        "stress_iterations": 50,
        "concurrent_tests": 5,
        "timeout": 3.0,
        "edge_cases": True,
        "performance_threshold": 70.0
    },
    "hard": {
        "name": "🔴 Difícil",
        "description": "Tests intensivos con alta carga",
        "stress_iterations": 100,
        "concurrent_tests": 10,
        "timeout": 1.0,
        "edge_cases": True,
        "performance_threshold": 80.0
    },
    "nightmare": {
        "name": "💀 Pesadilla",
        "description": "Tests extremos para evaluar límites",
        "stress_iterations": 500,
        "concurrent_tests": 20,
        "timeout": 0.5,
        "edge_cases": True,
        "performance_threshold": 90.0
    }
}

# Tests que se deben ejecutar siempre
BASIC_TESTS = [
    ("Saludo básico", "hola", ["bienvenido", "hotel"]),
    ("Saludo formal", "Buenos días", ["buenos días", "bienvenido"]),
    ("Habitación económica", "cuál es la habitación más barata", ["económica", "precio"]),
    ("Habitación lujosa", "habitación más cara", ["lujosa", "exclusiva"]),
    ("Restaurantes", "información sobre restaurantes", ["restaurante", "menú"]),
    ("Menús", "precios de los menús", ["precio", "menú"]),
    ("Amenidades", "qué actividades tienen", ["amenidades", "actividades"]),
    ("Contacto", "información de contacto", ["contacto", "teléfono"]),
    ("Reservas", "cómo hacer una reserva", ["reserva", "contacto"]),
    ("Ayuda", "ayuda", ["ayuda", "información"])
]

# Tests de dificultad media
MEDIUM_TESTS = [
    ("Consulta con errores tipográficos", "abl me gustari saver de las avitasiones", None),
    ("Consulta mezclada", "Hola, necesito saber precios de habitaciones y restaurantes", None),
    ("Consulta en inglés", "What are your room prices?", None),
    ("Consulta con caracteres especiales", "¿Cuál es la habitación más económica? 💰🏠", None),
    ("Consulta muy larga", "Me gustaría obtener información detallada sobre todas las habitaciones disponibles en el hotel, incluyendo precios, servicios incluidos, amenidades, políticas de cancelación y disponibilidad para las próximas fechas", None),
    ("Consulta ambigua", "precio", None),
    ("Consulta sin contexto", "¿cuánto cuesta?", None),
    ("Múltiples preguntas", "¿Cuáles son los precios de las habitaciones y qué restaurantes tienen?", None)
]

# Tests extremos para casos edge
EXTREME_TESTS = [
    ("Texto vacío", "", None),
    ("Solo espacios", "   ", None),
    ("Solo símbolos", "!@#$%^&*()", None),
    ("Texto muy largo", "a" * 1000, None),
    ("Caracteres unicode", "🏨🍽️🏊‍♂️💰🌟", None),
    ("HTML/Scripts", "<script>alert('test')</script>", None),
    ("SQL injection", "'; DROP TABLE users; --", None),
    ("Path traversal", "../../../etc/passwd", None),
    ("Números aleatorios", "123456789", None),
    ("Caracteres especiales", "çñáéíóúü", None),
    ("Texto en otros idiomas", "Здравствуйте, где ресторан?", None),
    ("JSON malformado", '{"test": incomplete', None),
    ("XML malformado", "<xml><unclosed>", None),
    ("URLs", "https://malicious-site.com/hack", None),
    ("Comandos shell", "rm -rf /", None)
]

# Funciones a testear individualmente
FUNCTIONS_TO_TEST = [
    ("get_hotel_name_from_documents", "get_hotel_name_from_documents", []),
    ("get_time_based_greeting", "get_time_based_greeting", []),
    ("normalize_text", "normalize_text", ["¡Hola! ¿Cómo está?"]),
    ("get_room_info_from_documents", "get_room_info_from_documents", []),
    ("get_cheapest_room_info", "get_cheapest_room_info", []),
    ("get_most_expensive_room_info", "get_most_expensive_room_info", []),
    ("get_restaurant_info_from_documents", "get_restaurant_info_from_documents", []),
    ("get_amenities_info_from_documents", "get_amenities_info_from_documents", []),
    ("get_contact_info_from_documents", "get_contact_info_from_documents", [])
]

# Documentos que deben existir
REQUIRED_DOCUMENTS = [
    "hotel_info.txt",
    "habitaciones_precios.txt",
    "restaurantes_menus.txt",
    "amenidades_actividades.txt"
]

# Umbrales de rendimiento
PERFORMANCE_THRESHOLDS = {
    "response_time_max": 2.0,  # Segundos
    "success_rate_min": 85.0,  # Porcentaje
    "concurrent_success_min": 80.0,  # Porcentaje
    "stress_success_min": 90.0  # Porcentaje
}

# Configuración de colores
COLORS = {
    "header": "\033[96m",
    "success": "\033[92m",
    "warning": "\033[93m",
    "error": "\033[91m",
    "info": "\033[94m",
    "reset": "\033[0m"
}
