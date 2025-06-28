"""
Servicio especializado en información de restaurantes y amenidades
"""
import json
from typing import Any, Dict

from database.repository import contenido_repository
from utils.logger import logger


def get_restaurant_info_from_documents() -> str:
    """Obtiene información de restaurantes desde la base de datos"""
    try:
        restaurantes = contenido_repository.obtener_por_categoria('restaurantes')

        if not restaurantes:
            return "🍽️ **Restaurantes**\n\nInformación de restaurantes no disponible en este momento."

        response = "🍽️ **NUESTROS RESTAURANTES**\n"
        response += "═" * 40 + "\n\n"

        for i, restaurante in enumerate(restaurantes, 1):
            # Título del restaurante con numeración
            response += f"**{i}. {restaurante['titulo']}**\n"
            response += "─" * (len(restaurante['titulo']) + 4) + "\n"

            # Limpiar y formatear contenido
            contenido = _format_restaurant_content(restaurante['contenido'])
            response += f"📋 {contenido}\n"

            # Intentar obtener información adicional de metadatos
            metadatos = _get_restaurant_metadata(restaurante)

            # Agregar información de metadatos
            response += _add_restaurant_metadata_info(metadatos)
            response += "\n"

        # Footer mejorado
        response += "═" * 40 + "\n"
        response += "📞 **RESERVAS:** Contacta con recepción\n"
        response += "🕐 **Horarios:** Consulta disponibilidad al momento de tu reserva"

        return response

    except Exception as e:
        logger.error(f"❌ Error obteniendo restaurantes desde BD: {e}")
        return "🍽️ Información de restaurantes no disponible."


def get_amenities_info_from_documents() -> str:
    """Obtiene información de amenidades desde la base de datos"""
    try:
        amenidades = contenido_repository.obtener_por_categoria('amenidades')

        # Verificar si la consulta devolvió datos
        if not amenidades:
            logger.warning("⚠️ No se encontraron amenidades en la base de datos")
            return "🏊 **AMENIDADES**\n\nInformación de amenidades no disponible en este momento.\n\n💡 **Sugerencia:** Contacta con recepción para conocer nuestros servicios y amenidades disponibles."

        # Verificar que amenidades sea una lista válida
        if not isinstance(amenidades, list):
            logger.error(f"❌ Formato de datos incorrecto para amenidades: {type(amenidades)}")
            return "🏊 **AMENIDADES**\n\nError en el formato de datos de amenidades."

        response = "🏊‍♂️ **AMENIDADES Y SERVICIOS**\n"
        response += "═" * 40 + "\n\n"

        valid_amenidades = 0
        for i, amenidad in enumerate(amenidades, 1):
            try:
                # Verificar que amenidad sea un diccionario válido
                if not isinstance(amenidad, dict):
                    logger.warning(f"⚠️ Amenidad {i} no es un diccionario válido: {type(amenidad)}")
                    continue

                # Verificar que tenga los campos requeridos
                if 'titulo' not in amenidad:
                    logger.warning(f"⚠️ Amenidad {i} no tiene título")
                    continue

                titulo = amenidad.get('titulo', 'Servicio sin nombre')
                contenido = amenidad.get('contenido', 'Información no disponible')

                # Asegurar que titulo y contenido sean strings
                if not isinstance(titulo, str):
                    titulo = str(titulo) if titulo else 'Servicio sin nombre'
                if not isinstance(contenido, str):
                    contenido = str(contenido) if contenido else 'Información no disponible'

                # Título con numeración y emoji apropiado
                emoji = _get_amenity_emoji(titulo)

                response += f"**{valid_amenidades + 1}. {emoji} {titulo}**\n"
                response += "─" * (len(titulo) + 8) + "\n"

                # Limpiar y formatear contenido
                contenido = '\n'.join(line.strip() for line in contenido.split('\n') if line.strip())

                if len(contenido) > 200:
                    sentences = contenido.split('. ')
                    if len(sentences) >= 2:
                        truncated = '. '.join(sentences[:2])
                        if not truncated.endswith('.'):
                            truncated += "."
                        contenido = truncated
                    else:
                        # Si no hay oraciones, truncar por caracteres
                        contenido = contenido[:200] + "..." if len(contenido) > 200 else contenido

                response += f"📋 {contenido}\n"

                # Obtener metadatos adicionales de forma segura
                metadatos = amenidad.get('metadatos', {})
                if isinstance(metadatos, str):
                    try:
                        metadatos = json.loads(metadatos)
                    except (json.JSONDecodeError, Exception):
                        logger.warning(f"⚠️ Error parseando metadatos para amenidad {titulo}")
                        metadatos = {}

                # Información adicional de metadatos
                if isinstance(metadatos, dict) and metadatos.get('categoria_amenidad'):
                    response += f"🏷️ **Categoría:** {metadatos['categoria_amenidad']}\n"

                response += "\n"
                valid_amenidades += 1

            except Exception as e:
                logger.warning(f"⚠️ Error procesando amenidad {i}: {e}")
                continue

        # Verificar si se procesó al menos una amenidad válida
        if valid_amenidades == 0:
            logger.warning("⚠️ No se pudo procesar ninguna amenidad válida")
            return "🏊 **AMENIDADES**\n\nNo se pudieron cargar las amenidades en este momento.\n\n💡 **Sugerencia:** Contacta con recepción para información sobre servicios disponibles."

        # Footer mejorado
        response += "═" * 40 + "\n"
        response += "ℹ️ **INFO:** Todas las amenidades están incluidas\n"
        response += "📞 **CONSULTAS:** Contacta con recepción para horarios específicos"

        logger.info(f"✅ Se procesaron {valid_amenidades} amenidades correctamente")
        return response

    except Exception as e:
        logger.error(f"❌ Error obteniendo amenidades desde BD: {e}")
        return "🏊 **AMENIDADES**\n\nError temporal al cargar información de amenidades.\n\n📞 **Contacto:** Por favor contacta con recepción para información sobre nuestros servicios."


# ===== FUNCIONES AUXILIARES PRIVADAS =====

def _format_restaurant_content(contenido: str) -> str:
    """Formatea el contenido de un restaurante"""
    # Remover espacios en blanco excesivos al inicio de líneas
    contenido = '\n'.join(line.strip() for line in contenido.split('\n') if line.strip())

    # Truncar contenido si es muy largo pero mantener párrafos completos
    if len(contenido) > 250:
        sentences = contenido.split('. ')
        truncated = '. '.join(sentences[:2])
        if not truncated.endswith('.'):
            truncated += "."
        contenido = truncated

    return contenido


def _format_amenity_content(contenido: str) -> str:
    """Formatea el contenido de una amenidad"""
    contenido = '\n'.join(line.strip() for line in contenido.split('\n') if line.strip())

    if len(contenido) > 200:
        sentences = contenido.split('. ')
        truncated = '. '.join(sentences[:2])
        if not truncated.endswith('.'):
            truncated += "."
        contenido = truncated

    return contenido


def _get_restaurant_metadata(restaurante: Dict[str, Any]) -> Dict[str, Any]:
    """Obtiene y parsea los metadatos de un restaurante"""
    metadatos = restaurante.get('metadatos', {})
    if isinstance(metadatos, str):
        try:
            metadatos = json.loads(metadatos)
        except Exception:
            metadatos = {}
    return metadatos


def _get_amenity_metadata(amenidad: Dict[str, Any]) -> Dict[str, Any]:
    """Obtiene y parsea los metadatos de una amenidad"""
    metadatos = amenidad.get('metadatos', {})
    if isinstance(metadatos, str):
        try:
            metadatos = json.loads(metadatos)
        except Exception:
            metadatos = {}
    return metadatos


def _add_restaurant_metadata_info(metadatos: Dict[str, Any]) -> str:
    """Agrega información de metadatos del restaurante al response"""
    info = ""

    # Agregar tipo de cocina si está disponible
    if metadatos.get('tipo_cocina'):
        info += f"🍳 **Tipo:** {metadatos['tipo_cocina']}\n"

    # Agregar ambiente si está disponible
    if metadatos.get('ambiente'):
        info += f"✨ **Ambiente:** {metadatos['ambiente']}\n"

    # Agregar especialidad si está disponible
    if metadatos.get('especialidad'):
        info += f"⭐ **Especialidad:** {metadatos['especialidad']}\n"

    return info


def _get_amenity_emoji(titulo: str) -> str:
    """Obtiene el emoji apropiado para una amenidad según su título"""
    titulo_lower = titulo.lower()

    if "piscina" in titulo_lower:
        return "🏊‍♂️"
    elif "spa" in titulo_lower:
        return "🧘‍♀️"
    elif "fitness" in titulo_lower or "gimnasio" in titulo_lower:
        return "💪"
    elif "acuático" in titulo_lower or "deporte" in titulo_lower:
        return "🏄‍♂️"
    elif "kid" in titulo_lower or "niño" in titulo_lower or "infantil" in titulo_lower:
        return "👶"
    elif "restaurante" in titulo_lower or "bar" in titulo_lower:
        return "🍽️"
    elif "wifi" in titulo_lower or "internet" in titulo_lower:
        return "🌐"
    elif "parking" in titulo_lower or "estacionamiento" in titulo_lower:
        return "🚗"
    elif "entretenimiento" in titulo_lower or "juego" in titulo_lower:
        return "🎮"
    else:
        return "✨"
