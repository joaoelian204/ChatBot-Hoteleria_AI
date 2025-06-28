"""
Servicio especializado en búsqueda de habitaciones por precio
"""
import re
from typing import Any, Dict, List

from database.services.room_service import get_rooms_with_prices
from utils.logger import logger


def get_room_by_price(target_price: float, tolerance: float = 50.0) -> str:
    """
    Busca habitaciones por precio específico o aproximado

    Args:
        target_price: Precio objetivo en USD
        tolerance: Tolerancia para búsqueda aproximada (default: 50 USD)
    """
    try:
        rooms_with_prices = get_rooms_with_prices()

        if not rooms_with_prices:
            return "🏠 **BÚSQUEDA POR PRECIO**\n\nNo se pudieron obtener precios de las habitaciones."

        # Buscar coincidencia exacta primero
        exact_match = _find_exact_price_match(rooms_with_prices, target_price)

        if exact_match:
            return _format_exact_match_response(exact_match, target_price)

        # Si no hay coincidencia exacta, buscar aproximadas
        approximate_rooms = _find_approximate_price_matches(rooms_with_prices, target_price, tolerance)

        if approximate_rooms:
            return _format_approximate_matches_response(approximate_rooms, target_price)
        else:
            return _format_no_matches_response(rooms_with_prices, target_price)

    except Exception as e:
        logger.error(f"❌ Error buscando habitación por precio {target_price}: {e}")
        return f"🏠 Error buscando habitaciones por ${target_price:.0f} USD."


def extract_price_from_query(query: str) -> float:
    """
    Extrae el precio de una consulta del usuario

    Args:
        query: Consulta del usuario

    Returns:
        float: Precio extraído o 0.0 si no se encuentra
    """
    # Normalizar query
    query = query.lower()

    # Patrones para extraer precios (ordenados por prioridad)
    patterns = [
        r'\$\s*(\d+)',                    # $150, $ 150
        r'(\d+)\s*dolares?',              # 150 dolares, 150 dolar
        r'(\d+)\s*usd',                   # 150 usd, 150USD
        r'(\d+)\s*pesos?',                # 150 pesos, 150 peso
        r'precio\s+de\s+(\d+)',           # precio de 150
        r'cuesta\s+(\d+)',                # cuesta 150
        r'vale\s+(\d+)',                  # vale 150
        r'(\d+)\s*euros?',                # 150 euros, 150 euro
        r'de\s+(\d+)\s*dolares?',         # de 150 dolares
        r'de\s+(\d+)\s*usd',              # de 150 usd
        r'de\s+(\d+)(?:\s|$)',            # de 150 (al final o seguido de espacio)
        r'habitacion\s+de\s+(\d+)',       # habitacion de 150
        r'cuarto\s+de\s+(\d+)',           # cuarto de 150
        r'room\s+de\s+(\d+)',             # room de 150
        r'por\s+(\d+)',                   # por 150
        r'a\s+(\d+)',                     # a 150
        r'(\d+)\s*$',                     # solo número al final: "150"
        r'y\s+de\s+(\d+)',                # y de 150
        r'(\d{2,4})(?!\d)',               # cualquier número de 2-4 dígitos (100-9999)
    ]

    for pattern in patterns:
        matches = re.findall(pattern, query)
        for match in matches:
            try:
                price = float(match)
                # Filtrar precios que parecen razonables para habitaciones de hotel
                if 50 <= price <= 5000:  # Rango razonable para precios de hotel
                    return price
            except (ValueError, TypeError):
                continue

    return 0.0


# ===== FUNCIONES AUXILIARES PRIVADAS =====

def _find_exact_price_match(rooms_with_prices: List[Dict[str, Any]], target_price: float) -> Dict[str, Any]:
    """Busca una coincidencia exacta de precio"""
    for room_data in rooms_with_prices:
        if room_data['precio'] == target_price:
            return room_data
    return None


def _find_approximate_price_matches(rooms_with_prices: List[Dict[str, Any]],
                                    target_price: float,
                                    tolerance: float) -> List[Dict[str, Any]]:
    """Busca coincidencias aproximadas de precio"""
    approximate_rooms = []

    for room_data in rooms_with_prices:
        price_diff = abs(room_data['precio'] - target_price)
        if price_diff <= tolerance:
            approximate_rooms.append({
                'habitacion': room_data['habitacion'],
                'precio': room_data['precio'],
                'diferencia': price_diff
            })

    # Ordenar por diferencia de precio
    approximate_rooms.sort(key=lambda x: x['diferencia'])
    return approximate_rooms


def _format_exact_match_response(exact_match: Dict[str, Any], target_price: float) -> str:
    """Formatea la respuesta para coincidencia exacta"""
    habitacion = exact_match['habitacion']
    response = f"🎯 **HABITACIÓN ENCONTRADA - ${target_price:.0f} USD**\n"
    response += "═" * 45 + "\n\n"
    response += f"✅ **{habitacion['titulo']}**\n"
    response += "─" * (len(habitacion['titulo']) + 4) + "\n"
    response += f"💰 **Precio exacto:** ${target_price:.0f} USD por noche\n\n"

    # Agregar metadatos si existen
    metadatos = _get_room_metadata_for_price_search(habitacion)

    if metadatos.get('capacidad'):
        response += f"👥 **Capacidad:** {metadatos['capacidad']} personas\n"
    if metadatos.get('tamaño'):
        response += f"📐 **Tamaño:** {metadatos['tamaño']}\n"
    if metadatos.get('vista'):
        response += f"🌅 **Vista:** {metadatos['vista']}\n"

    # Descripción corta
    contenido = habitacion['contenido']
    if len(contenido) > 150:
        sentences = contenido.split('. ')
        contenido = '. '.join(sentences[:2])
        if not contenido.endswith('.'):
            contenido += "."

    response += f"\n📋 {contenido}\n\n"
    response += "═" * 45 + "\n"
    response += "📞 **RESERVAR:** Contacta con recepción"

    return response


def _format_approximate_matches_response(approximate_rooms: List[Dict[str, Any]], target_price: float) -> str:
    """Formatea la respuesta para coincidencias aproximadas"""
    response = f"🔍 **HABITACIONES SIMILARES A ${target_price:.0f} USD**\n"
    response += "═" * 50 + "\n\n"
    response += f"❌ No tenemos habitaciones exactamente a ${target_price:.0f} USD\n"
    response += "✨ **Pero aquí tienes opciones similares:**\n\n"

    for i, room_data in enumerate(approximate_rooms[:3], 1):  # Máximo 3 opciones
        habitacion = room_data['habitacion']
        precio = room_data['precio']
        diferencia = room_data['diferencia']

        if precio > target_price:
            diff_text = f"(+${diferencia:.0f} más)"
            emoji = "📈"
        else:
            diff_text = f"(-${diferencia:.0f} menos)"
            emoji = "📉"

        response += f"{i}. **{habitacion['titulo']}**\n"
        response += f"   {emoji} **${precio:.0f} USD** {diff_text}\n"

        # Descripción muy corta
        contenido = habitacion['contenido']
        if len(contenido) > 80:
            contenido = contenido[:80] + "..."
        response += f"   📋 {contenido}\n\n"

    response += "═" * 50 + "\n"
    response += "💡 **¿Te interesa alguna opción?**\n"
    response += "📞 **Contacto:** +52 984 123-4567"

    return response


def _format_no_matches_response(rooms_with_prices: List[Dict[str, Any]], target_price: float) -> str:
    """Formatea la respuesta cuando no hay coincidencias"""
    # Mostrar la más barata y la más cara como alternativas
    min_price = min(room_data['precio'] for room_data in rooms_with_prices)
    max_price = max(room_data['precio'] for room_data in rooms_with_prices)

    response = f"❌ **NO DISPONIBLE - ${target_price:.0f} USD**\n"
    response += "═" * 40 + "\n\n"
    response += f"Lo sentimos, no tenemos habitaciones en el rango de ${target_price:.0f} USD.\n\n"
    response += "💡 **Nuestras opciones disponibles:**\n\n"
    response += f"💰 **Más económica:** Desde ${min_price:.0f} USD\n"
    response += f"👑 **Más lujosa:** Hasta ${max_price:.0f} USD\n\n"
    response += "🔍 **¿Te gustaría ver estas opciones?**\n"
    response += "Pregunta por 'la habitación más barata' o 'todas las habitaciones'\n\n"
    response += "═" * 40 + "\n"
    response += "📞 **Contacto:** +52 984 123-4567"

    return response


def _get_room_metadata_for_price_search(habitacion: Dict[str, Any]) -> Dict[str, Any]:
    """Obtiene metadatos de habitación para búsqueda por precio"""
    import json

    metadatos = habitacion.get('metadatos', {})
    if isinstance(metadatos, str):
        try:
            metadatos = json.loads(metadatos)
        except Exception:
            metadatos = {}
    return metadatos
