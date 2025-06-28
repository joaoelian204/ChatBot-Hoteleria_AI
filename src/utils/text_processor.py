"""
Utilidades para procesamiento de texto
"""
import re
from typing import Tuple


def sanitize_text(text: str) -> str:
    """Sanitiza el texto de entrada"""
    if not text:
        return ""
    
    # Remover caracteres especiales peligrosos
    text = re.sub(r'[<>"\']', '', text)
    
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text)
    
    # Limitar longitud
    return text.strip()[:1000]

def validate_message(message: str, user_id: int = None) -> Tuple[bool, str]:
    """Valida un mensaje de entrada"""
    if not message or not message.strip():
        return False, "El mensaje no puede estar vacío"
    
    if len(message) > 1000:
        return False, "El mensaje es demasiado largo (máximo 1000 caracteres)"
    
    # Verificar contenido inapropiado
    inappropriate_words = ['spam', 'bot', 'automated']
    message_lower = message.lower()
    for word in inappropriate_words:
        if word in message_lower:
            return False, f"El mensaje contiene contenido inapropiado: {word}"
    
    return True, "OK"

def detect_intent(text: str) -> str:
    """
    Detecta la intención del texto usando normalización
    """
    # Normalizar el texto de entrada
    normalized_text = normalize_text(text)
    
    # Detectar preguntas específicas sobre precios económicos (con texto normalizado)
    economic_keywords = [
        'economica', 'barata', 'mas barata', 'menos cara', 'precio bajo', 
        'mas economica', 'la mas barata', 'la mas economica', 'mas barato',
        'menos costosa', 'mas accesible', 'precio economico', 'tarifa baja',
        'cual es la economica', 'cual es la barata', 'habitacion economica',
        'habitacion barata', 'suite economica', 'alojamiento economico'
    ]
    
    if any(keyword in normalized_text for keyword in economic_keywords):
        return "precios"
    
    # Palabras clave para cada intención (ya normalizadas, sin duplicados)
    intent_keywords = {
        'habitaciones': [
            'habitacion', 'suite', 'cama', 'dormitorio', 'alojamiento', 
            'cuarto', 'room', 'ocupacion'
        ],
        'restaurantes': [
            'restaurante', 'menu', 'comida', 'gastronomia', 'cena', 
            'almuerzo', 'desayuno', 'bar', 'cafe', 'buffet', 'cocina'
        ],
        'amenidades': [
            'piscina', 'gimnasio', 'spa', 'amenidad', 'actividad', 
            'servicio', 'entretenimiento', 'deportes', 'wellness'
        ],
        'precios': [
            'precio', 'tarifa', 'costo', 'valor', 'cuanto', 'pagar',
            'factura', 'cobro', 'descuento', 'promocion'
        ],
        'contacto': [
            'contacto', 'telefono', 'email', 'reservar', 'reserva', 
            'llamar', 'direccion', 'ubicacion', 'como llegar'
        ]
    }
    
    # Buscar coincidencias en texto normalizado
    for intent, keywords in intent_keywords.items():
        if any(keyword in normalized_text for keyword in keywords):
            return intent
    
    return "general"

def normalize_text(text: str) -> str:
    """
    Normaliza el texto para búsqueda y coincidencia de intenciones
    - Convierte a minúsculas
    - Remueve acentos y diacríticos
    - Elimina signos de puntuación y caracteres especiales
    - Normaliza espacios
    """
    if not text:
        return ""
    
    # Convertir a minúsculas
    text = text.lower()
    
    # Remover acentos y diacríticos
    text = text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    text = text.replace('ñ', 'n').replace('ü', 'u')
    text = text.replace('à', 'a').replace('è', 'e').replace('ì', 'i').replace('ò', 'o').replace('ù', 'u')
    text = text.replace('â', 'a').replace('ê', 'e').replace('î', 'i').replace('ô', 'o').replace('û', 'u')
    
    # Remover signos de puntuación y caracteres especiales
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Normalizar espacios múltiples
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def generate_cache_key(text: str) -> str:
    """Genera una clave única para el cache"""
    import hashlib
    normalized = normalize_text(text)
    return hashlib.md5(normalized.encode()).hexdigest() 