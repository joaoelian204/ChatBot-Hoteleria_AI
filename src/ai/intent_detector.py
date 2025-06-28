"""
Detector de intenciones del usuario
"""
from typing import Dict, Tuple

from utils.logger import logger
from utils.text_processor import normalize_text


def get_intent_patterns() -> Dict[str, list]:
    """Retorna los patrones de intención mapeados"""
    return {
        'economic_room': [
            'economica', 'barata', 'mas barata', 'menos cara', 'precio bajo',
            'mas economica', 'la mas barata', 'la mas economica', 'mas barato',
            'menos costosa', 'mas accesible', 'precio economico', 'tarifa baja',
            'cual es la economica', 'cual es la barata', 'habitacion economica',
            'habitacion barata', 'suite economica', 'alojamiento economico',
            'mas barato', 'menos caro', 'precio minimo', 'tarifa economica',
            'habitacion simple', 'habitacion basica', 'opcion economica'
        ],
        'expensive_room': [
            'cara', 'costosa', 'mas cara', 'mas costosa', 'precio alto',
            'mas caro', 'la mas cara', 'la mas costosa', 'mas costoso',
            'precio maximo', 'mas lujosa', 'lujosa', 'presidencial', 'suite presidencial',
            'habitacion cara', 'habitacion costosa', 'suite cara', 'suite costosa',
            'habitacion lujosa', 'suite lujosa', 'alojamiento lujoso', 'opcion lujosa',
            'la mejor habitacion', 'habitacion premium', 'suite premium'
        ],
        'rooms_with_prices': [
            'habitacion', 'suite', 'cama', 'dormitorio', 'cuarto', 'alojamiento',
            'precio', 'costo', 'valor', 'cuanto', 'tarifa', 'pagar', 'coste',
            'habitaciones', 'suites', 'dormitorios', 'cuartos', 'precios',
            'costos', 'valores', 'tarifas', 'costes', 'habitacion precio',
            'suite precio', 'cama precio', 'dormitorio precio', 'cuarto precio'
        ],
        'restaurants': [
            'restaurante', 'menu', 'comida', 'gastronomia', 'cena', 'almuerzo',
            'desayuno', 'bar', 'cafeteria', 'cafe', 'buffet', 'grill', 'pizzeria',
            'sushi', 'italiano', 'mexicano', 'internacional', 'fusion', 'snack',
            'pub', 'wine', 'cocktail', 'restaurantes', 'menus', 'comidas',
            'gastronomias', 'cenas', 'almuerzos', 'desayunos', 'bares'
        ],
        'amenities': [
            'piscina', 'gimnasio', 'spa', 'amenidad', 'actividad', 'servicio',
            'sauna', 'jacuzzi', 'tenis', 'golf', 'wifi', 'parking', 'estacionamiento',
            'concierge', 'room service', 'facilidad', 'instalacion', 'deporte',
            'recreacion', 'entretenimiento', 'piscinas', 'gimnasios', 'spas',
            'amenidades', 'actividades', 'servicios', 'saunas', 'jacuzzis'
        ],
        'pricing': [
            'precio', 'tarifa', 'costo', 'valor', 'cuanto', 'pagar', 'coste',
            'precios', 'tarifas', 'costos', 'valores', 'costes', 'cuanto cuesta',
            'cuanto vale', 'cuanto pago', 'precio por noche', 'tarifa por noche',
            'costo por noche', 'valor por noche', 'precio habitacion', 'tarifa habitacion'
        ],
        'contact': [
            'contacto', 'telefono', 'email', 'reservar', 'reserva', 'llamar',
            'correo', 'mail', 'direccion', 'ubicacion', 'location', 'address',
            'contactos', 'telefonos', 'emails', 'reservas', 'llamadas', 'correos',
            'mails', 'direcciones', 'ubicaciones', 'reservar habitacion',
            'hacer reserva', 'contactar', 'comunicar', 'informacion contacto'
        ]
    }


def detect_intent(question: str) -> Tuple[str, int]:
    """
    Detecta la intención del usuario basada en la pregunta
    Usa normalización centralizada para consistencia
    Returns:
        Tuple[str, int]: (intención, puntuación)
    """
    question_normalized = normalize_text(question)
    logger.info(f"[DEBUG] Pregunta normalizada: '{question_normalized}'")
    intent_patterns = get_intent_patterns()
    intent_scores = {}
    for intent, patterns in intent_patterns.items():
        score = 0
        for pattern in patterns:
            if pattern in question_normalized:
                score += 1
        intent_scores[intent] = score
    best_intent = max(intent_scores.items(), key=lambda x: x[1])
    logger.info(f"[DEBUG] Intenciones detectadas: {intent_scores}")
    logger.info(f"[DEBUG] Mejor intención: {best_intent[0]} (score: {best_intent[1]})")
    return best_intent[0], best_intent[1]


def get_intent_function_name(intent: str) -> str:
    """Mapea la intención a la función correspondiente"""
    intent_function_map = {
        'economic_room': 'get_cheapest_room_info',
        'expensive_room': 'get_most_expensive_room_info',
        'rooms_with_prices': 'get_room_info_from_documents',
        'restaurants': 'get_restaurant_info_from_documents',
        'amenities': 'get_amenities_info_from_documents',
        'pricing': 'get_room_info_from_documents',
        'contact': 'get_contact_info_from_documents'
    }
    return intent_function_map.get(intent, 'get_general_info') 