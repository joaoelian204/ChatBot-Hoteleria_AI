"""
Callbacks para el bot de Telegram
"""
from ai.fallback_handler import (
    generate_fallback_response,
    get_amenities_info_from_documents,
    get_cheapest_room_info,
    get_contact_info_from_documents,
    get_most_expensive_room_info,
    get_restaurant_info_from_documents,
    get_room_info_from_documents,
    get_smart_welcome_response,
)
from ai.text_generator import generate_response
from ai.vectorstore import vectorstore_manager
from analytics.manager import analytics_manager
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils.logger import logger


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /start"""
    try:
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        logger.info(f"Usuario {user_id} ({user_name}) inició el bot")
        analytics_manager.track_event(
            "bot_start", {"user_id": user_id, "user_name": user_name})

        # Usar el nuevo sistema de saludo inteligente
        welcome_message = get_smart_welcome_response()

        keyboard = [
            [InlineKeyboardButton(
                "🏠 Habitaciones", callback_data="habitaciones")],
            [InlineKeyboardButton(
                "🍽️ Restaurantes", callback_data="restaurantes")],
            [InlineKeyboardButton("🏊 Amenidades", callback_data="amenidades")],
            [InlineKeyboardButton("📞 Contacto", callback_data="contacto")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en handle_start: {e}")
        await update.message.reply_text("❌ Lo siento, hubo un error. Intenta de nuevo.")


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /help"""
    try:
        user_id = update.effective_user.id
        logger.info(f"Usuario {user_id} solicitó ayuda")
        analytics_manager.track_event("bot_help", {"user_id": user_id})
        help_message = """🤖 **Comandos disponibles:**

/start - Iniciar el bot
/help - Mostrar esta ayuda
/rooms - Información de habitaciones
/restaurants - Información de restaurantes
/amenities - Información de amenidades
/contact - Información de contacto

💡 También puedes escribir tu pregunta directamente."""
        await update.message.reply_text(help_message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en handle_help: {e}")
        await update.message.reply_text("❌ Lo siento, hubo un error. Intenta de nuevo.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja mensajes de texto del usuario"""
    try:
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        message_text = update.message.text
        logger.info(f"Usuario {user_id} ({user_name}) envió: {message_text}")
        analytics_manager.track_event("user_message", {
            "user_id": user_id,
            "user_name": user_name,
            "message_length": len(message_text)
        })

        # Usar nuestro sistema mejorado de fallback_handler
        response = generate_fallback_response(message_text)
        await update.message.reply_text(response, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en handle_message: {e}")
        await update.message.reply_text("❌ Lo siento, hubo un error procesando tu mensaje. Intenta de nuevo.")


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja las consultas de callback de los botones inline"""
    try:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        user_name = query.from_user.first_name
        callback_data = query.data
        logger.info(
            f"Usuario {user_id} ({user_name}) presionó botón: {callback_data}")
        analytics_manager.track_event("button_click", {
            "user_id": user_id,
            "user_name": user_name,
            "button": callback_data
        })
        if callback_data == "habitaciones":
            await _handle_rooms_callback(query)
        elif callback_data == "restaurantes":
            await _handle_restaurants_callback(query)
        elif callback_data == "amenidades":
            await _handle_amenities_callback(query)
        elif callback_data == "contacto":
            await _handle_contact_callback(query)
        elif callback_data == "precios":
            await _handle_pricing_callback(query)
        elif callback_data == "cheapest_room":
            await _handle_cheapest_room_callback(query)
        elif callback_data == "most_expensive_room":
            await _handle_most_expensive_room_callback(query)
        elif callback_data == "reservar":
            await _handle_booking_callback(query)
        elif callback_data == "reservar_mesa":
            await _handle_booking_callback(query)  # Usar la misma función para ambos tipos de reserva
        elif callback_data == "volver":
            # Volver al menú principal con saludo inteligente
            welcome_message = get_smart_welcome_response()
            keyboard = [
                [InlineKeyboardButton(
                    "🏠 Habitaciones", callback_data="habitaciones")],
                [InlineKeyboardButton(
                    "🍽️ Restaurantes", callback_data="restaurantes")],
                [InlineKeyboardButton(
                    "🏊 Amenidades", callback_data="amenidades")],
                [InlineKeyboardButton("📞 Contacto", callback_data="contacto")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            logger.warning(f"Callback no reconocido: {callback_data}")
            await query.edit_message_text("❌ Opción no reconocida. Usa /start para ver las opciones disponibles.")
    except Exception as e:
        logger.error(f"Error en handle_callback_query: {e}")
        await query.edit_message_text("❌ Lo siento, hubo un error. Intenta de nuevo.")


async def _handle_rooms_callback(query) -> None:
    """Maneja el callback de habitaciones"""
    try:
        # Usar nuestro sistema mejorado
        response = get_room_info_from_documents()
        keyboard = [
            [InlineKeyboardButton(
                "💰 Habitación más económica", callback_data="cheapest_room")],
            [InlineKeyboardButton("� Habitación más lujosa",
                                callback_data="most_expensive_room")],
            [InlineKeyboardButton("�📞 Reservar", callback_data="reservar")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en _handle_rooms_callback: {e}")
        await query.edit_message_text("❌ Error al obtener información de habitaciones.")


async def _handle_restaurants_callback(query) -> None:
    """Maneja el callback de restaurantes"""
    try:
        # Usar nuestro sistema mejorado
        response = get_restaurant_info_from_documents()
        keyboard = [
            [InlineKeyboardButton(
                "📞 Reservar mesa", callback_data="reservar_mesa")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en _handle_restaurants_callback: {e}")
        await query.edit_message_text("❌ Error al obtener información de restaurantes.")


async def _handle_amenities_callback(query) -> None:
    """Maneja el callback de amenidades"""
    try:
        # Usar nuestro sistema mejorado
        response = get_amenities_info_from_documents()
        keyboard = [
            [InlineKeyboardButton("📞 Más información",
                                  callback_data="reservar")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en _handle_amenities_callback: {e}")
        await query.edit_message_text("❌ Error al obtener información de amenidades.")


async def _handle_contact_callback(query) -> None:
    """Maneja el callback de contacto"""
    try:
        # Usar nuestro sistema mejorado
        response = get_contact_info_from_documents()
        keyboard = [
            [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en _handle_contact_callback: {e}")
        await query.edit_message_text("❌ Error al obtener información de contacto.")


async def _handle_cheapest_room_callback(query) -> None:
    """Maneja el callback de habitación más económica"""
    try:
        # Usar nuestro sistema de habitación más económica
        response = get_cheapest_room_info()
        keyboard = [
            [InlineKeyboardButton(
                "📞 Reservar esta habitación", callback_data="reservar")],
            [InlineKeyboardButton(
                "🏠 Ver todas las habitaciones", callback_data="habitaciones")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en _handle_cheapest_room_callback: {e}")
        await query.edit_message_text("❌ Error al obtener información de la habitación más económica.")


async def _handle_most_expensive_room_callback(query) -> None:
    """Maneja el callback de habitación más cara"""
    try:
        # Usar nuestro sistema de habitación más cara
        response = get_most_expensive_room_info()
        keyboard = [
            [InlineKeyboardButton(
                "📞 Reservar esta habitación", callback_data="reservar")],
            [InlineKeyboardButton(
                "🏠 Ver todas las habitaciones", callback_data="habitaciones")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en _handle_most_expensive_room_callback: {e}")
        await query.edit_message_text("❌ Error al obtener información de la habitación más cara.")


async def _handle_pricing_callback(query) -> None:
    """Maneja el callback de precios"""
    try:
        from ai.models import ai_models
        
        search_query = "precio tarifa costo habitación suite" 
        
        # Usar el método correcto según el modo de carga
        if ai_models.use_lazy_loading:
            context_docs = await vectorstore_manager.search_context_async(search_query, k=3)
        else:
            context_docs = vectorstore_manager.search_context(search_query, k=3)
            
        from ai.text_generator import generate_response_async
        response = await generate_response_async("¿Cuáles son los precios?", context_docs)
        keyboard = [
            [InlineKeyboardButton(
                "📞 Consultar", callback_data="consultar_precio")],
            [InlineKeyboardButton("🔙 Volver", callback_data="habitaciones")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en _handle_pricing_callback: {e}")
        await query.edit_message_text("❌ Error al obtener información de precios.")


async def _handle_booking_callback(query) -> None:
    """Maneja el callback de reservas"""
    try:
        # Obtener información de contacto real desde los documentos
        contact_info = get_contact_info_from_documents()
        
        # Agregar contexto específico para reservas
        response = f"📞 **Reservas**\n\n{contact_info}\n\n� **Para reservas, por favor menciona:**\n• Fechas de entrada y salida\n• Número de huéspedes\n• Tipo de habitación preferida\n\n¿Te gustaría que te ayude con algo más?"
        keyboard = [
            [InlineKeyboardButton("📞 Llamar ahora", callback_data="llamar")],
            [InlineKeyboardButton("📧 Enviar email", callback_data="email")],
            [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error en _handle_booking_callback: {e}")
        await query.edit_message_text("❌ Error al procesar la solicitud de reserva.")


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja errores del bot"""
    try:
        logger.error(f"Error en el bot: {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Lo siento, ocurrió un error inesperado. Por favor, intenta de nuevo."
            )
    except Exception as e:
        logger.error(f"Error en handle_error: {e}")
