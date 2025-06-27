"""
Bot principal modularizado
"""
import time
from datetime import datetime
from typing import Dict

from ai.cache import response_cache
from ai.intent_detector import detect_intent
from ai.vectorstore import vectorstore_manager
from analytics.manager import analytics_manager
from config.settings import settings
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from utils.logger import logger
from utils.text_processor import sanitize_text, validate_message

from bot.callbacks import (
    handle_callback_query,
    handle_error,
    handle_help,
    handle_message,
    handle_start,
)


class HoteleriaBot:
    """Bot de hotelería modularizado con funcionalidades avanzadas"""

    def __init__(self):
        """Inicializa el bot de hotelería"""
        settings.validate()

        self.token = settings.TELEGRAM_TOKEN
        self.app = ApplicationBuilder().token(self.token).build()

        # Persistencia de contexto de usuario
        self.user_contexts: Dict[int, Dict] = {}

        # Configuración de validaciones
        self.user_message_counts = {}

        self._configurar_handlers()

    def _configurar_handlers(self):
        """Configura todos los handlers del bot"""
        # Comandos básicos
        self.app.add_handler(CommandHandler("start", handle_start))
        self.app.add_handler(CommandHandler("help", handle_help))
        self.app.add_handler(CommandHandler("stats", self._handle_stats))
        self.app.add_handler(CommandHandler(
            "clear_cache", self._handle_clear_cache))

        # Comandos que redirigen a callbacks (usan documentos reales)
        self.app.add_handler(CommandHandler(
            "rooms", self._rooms_command_redirect))
        self.app.add_handler(CommandHandler(
            "restaurants", self._restaurants_command_redirect))
        self.app.add_handler(CommandHandler(
            "amenities", self._amenities_command_redirect))
        self.app.add_handler(CommandHandler(
            "contact", self._contact_command_redirect))

        # Callback queries para botones
        self.app.add_handler(CallbackQueryHandler(handle_callback_query))

        # Handler para mensajes de texto
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, handle_message
        ))

        # Handler de errores
        self.app.add_error_handler(handle_error)

    async def _handle_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja el comando /stats para mostrar estadísticas del sistema"""
        try:
            from ai.cache import response_cache
            from ai.models import ai_models
            from ai.vectorstore import vectorstore_manager

            # Obtener estadísticas
            cache_stats = response_cache.get_stats()
            model_stats = ai_models.get_stats()
            vectorstore_stats = vectorstore_manager.get_stats()

            # Formatear mensaje
            stats_message = f"""📊 **Estadísticas del Sistema**

🗂️ **Cache de Respuestas:**
• Hits: {cache_stats['hits']} ({cache_stats['hit_rate']}%)
• Misses: {cache_stats['misses']}
• Tamaño: {cache_stats['cache_size']}/{cache_stats['max_size']} ({cache_stats['usage_percent']}%)
• Evictions: {cache_stats['evictions']}

🤖 **Modelos de IA:**
• Modo: {"Lazy Loading" if settings.LAZY_LOAD_MODELS else "Carga Inmediata"}
• Cache habilitado: {"✅" if settings.ENABLE_MODEL_CACHING else "❌"}
• Max concurrencia: {settings.MAX_CONCURRENT_REQUESTS}

📚 **Base de Conocimiento:**
• Documentos: {vectorstore_stats['document_count']}
• Vectorstore: {"✅ Creado" if vectorstore_stats['vectorstore_created'] else "❌ No disponible"}
• Modelo embeddings: {vectorstore_stats['embedding_model']}

⚙️ **Configuración:**
• Analytics: {"✅" if settings.ENABLE_ANALYTICS else "❌"}
• Respuestas enriquecidas: {"✅" if settings.ENABLE_RICH_RESPONSES else "❌"}
• Formato con emojis: {"✅" if settings.ENABLE_EMOJI_FORMATTING else "❌"}"""

            # Añadir estadísticas de resource manager si está disponible
            if settings.LAZY_LOAD_MODELS and 'concurrency' in model_stats:
                concurrency_stats = model_stats['concurrency']
                stats_message += f"""

🚦 **Gestión de Recursos:**
• Requests activos: {concurrency_stats['active_requests']}/{concurrency_stats['max_concurrent']}
• Total requests: {concurrency_stats['total_requests']}
• Uso concurrencia: {concurrency_stats['usage_percent']:.1f}%"""

            await update.message.reply_text(
                stats_message,
                parse_mode=ParseMode.MARKDOWN
            )

            logger.info(
                f"📊 Estadísticas mostradas a usuario {update.effective_user.id}")

        except Exception as e:
            logger.error(f"❌ Error al mostrar estadísticas: {e}")
            await update.message.reply_text(
                "❌ Error al obtener las estadísticas del sistema."
            )

    def _get_user_context(self, user_id: int) -> Dict:
        """Obtiene el contexto del usuario"""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {
                'conversation_history': [],
                'last_interaction': datetime.now(),
                'preferences': {},
                'current_topic': None
            }
        return self.user_contexts[user_id]

    def _update_user_context(self, user_id: int, message: str, response: str):
        """Actualiza el contexto del usuario"""
        context = self._get_user_context(user_id)
        context['conversation_history'].append({
            'user_message': message,
            'bot_response': response,
            'timestamp': datetime.now()
        })

        # Mantener solo las últimas 10 interacciones
        if len(context['conversation_history']) > 10:
            context['conversation_history'] = context['conversation_history'][-10:]

        context['last_interaction'] = datetime.now()

    def _create_rich_response(self, text: str, intent: str = None) -> tuple:
        """Crea una respuesta enriquecida con botones y formato"""
        if not settings.ENABLE_RICH_RESPONSES:
            return text, None

        # Formatear texto con Markdown
        formatted_text = self._format_text_with_emojis(text, intent)

        # Crear botones contextuales
        keyboard = self._create_contextual_keyboard(intent)

        return formatted_text, InlineKeyboardMarkup(keyboard) if keyboard else None

    def _format_text_with_emojis(self, text: str, intent: str = None) -> str:
        """Formatea el texto con emojis y Markdown"""
        # Agregar emojis según el contexto
        if intent == "habitaciones":
            text = "🏨 " + text
        elif intent == "restaurantes":
            text = "🍽️ " + text
        elif intent == "amenidades":
            text = "🏊 " + text
        elif intent == "precios":
            text = "💰 " + text
        elif intent == "contacto":
            text = "📞 " + text

        # Convertir a Markdown si no lo está
        if not text.startswith('*') and not text.startswith('**'):
            # Agregar formato básico
            lines = text.split('\n')
            formatted_lines = []
            for line in lines:
                if line.strip().startswith('🏨') or line.strip().startswith('🍽️') or line.strip().startswith('🏊'):
                    formatted_lines.append(f"**{line}**")
                elif line.strip().startswith('💡'):
                    formatted_lines.append(f"*{line}*")
                else:
                    formatted_lines.append(line)
            text = '\n'.join(formatted_lines)

        return text

    def _create_contextual_keyboard(self, intent: str = None) -> list:
        """Crea botones contextuales según la intención"""
        if intent == "habitaciones":
            return [
                [
                    InlineKeyboardButton(
                        "💰 Ver Precios", callback_data="precios_habitaciones"),
                    InlineKeyboardButton(
                        "📞 Reservar", callback_data="reservar_habitacion")
                ],
                [
                    InlineKeyboardButton(
                        "🏊 Amenidades", callback_data="amenidades"),
                    InlineKeyboardButton(
                        "🍽️ Restaurantes", callback_data="restaurantes")
                ]
            ]
        elif intent == "restaurantes":
            return [
                [
                    InlineKeyboardButton("📋 Ver Menús", callback_data="menus"),
                    InlineKeyboardButton(
                        "📞 Reservar Mesa", callback_data="reservar_mesa")
                ],
                [
                    InlineKeyboardButton(
                        "🏨 Habitaciones", callback_data="habitaciones"),
                    InlineKeyboardButton(
                        "🏊 Amenidades", callback_data="amenidades")
                ]
            ]
        elif intent == "amenidades":
            return [
                [
                    InlineKeyboardButton(
                        "🏨 Habitaciones", callback_data="habitaciones"),
                    InlineKeyboardButton(
                        "🍽️ Restaurantes", callback_data="restaurantes")
                ],
                [
                    InlineKeyboardButton(
                        "📞 Contacto", callback_data="contacto"),
                    InlineKeyboardButton("💰 Precios", callback_data="precios")
                ]
            ]
        else:
            return [
                [
                    InlineKeyboardButton(
                        "🏨 Habitaciones", callback_data="habitaciones"),
                    InlineKeyboardButton(
                        "🍽️ Restaurantes", callback_data="restaurantes")
                ],
                [
                    InlineKeyboardButton(
                        "🏊 Amenidades", callback_data="amenidades"),
                    InlineKeyboardButton(
                        "📞 Contacto", callback_data="contacto")
                ],
                [
                    InlineKeyboardButton(
                        "❓ Pregunta Libre", callback_data="pregunta_libre")
                ]
            ]

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja mensajes de texto del usuario"""
        user_id = update.effective_user.id
        message = update.message.text

        # Validar mensaje
        is_valid, error_msg = validate_message(message, user_id)
        if not is_valid:
            await update.message.reply_text(f"❌ {error_msg}")
            return

        # Sanitizar mensaje
        sanitized_message = sanitize_text(message)

        # Validar límite de mensajes por minuto
        if not self._validate_message_rate_limit(user_id):
            await update.message.reply_text(
                "⚠️ Estás enviando demasiados mensajes. Espera un momento."
            )
            return

        # Mostrar indicador de escritura
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        start_time = time.time()

        try:
            # Obtener respuesta de IA
            response = await self._get_ai_response(sanitized_message)

            # Calcular tiempo de respuesta
            response_time = time.time() - start_time

            # Detectar intención para botones contextuales
            intent, confidence = detect_intent(sanitized_message)
            logger.info(
                f"Intención detectada: {intent} (confianza: {confidence})")

            # Crear respuesta enriquecida
            formatted_response, keyboard = self._create_rich_response(
                response, intent)

            # Enviar respuesta
            await update.message.reply_text(
                formatted_response,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )

            # Actualizar contexto del usuario
            self._update_user_context(user_id, sanitized_message, response)

            # Registrar métricas
            self._record_metrics(sanitized_message, response_time, user_id)

        except Exception as e:
            logger.error(f"Error al procesar mensaje: {e}")
            await update.message.reply_text(
                "❌ Lo siento, tuve un problema procesando tu mensaje. Intenta de nuevo."
            )

    async def _get_ai_response(self, message: str) -> str:
        """Obtiene respuesta de IA"""
        from ai.models import ai_models
        
        # Verificar cache primero
        cached_response = response_cache.get(message)
        if cached_response:
            return cached_response

        # Buscar contexto relevante según el modo de carga
        if ai_models.use_lazy_loading:
            context_docs = await vectorstore_manager.search_context_async(message)
        else:
            context_docs = vectorstore_manager.search_context(message)

        # Generar respuesta usando IA
        from ai.text_generator import generate_response_async
        response = await generate_response_async(message, context_docs)

        # Guardar en cache
        response_cache.set(message, response)

        return response

    def _validate_message_rate_limit(self, user_id: int) -> bool:
        """Valida el límite de mensajes por minuto"""
        current_time = time.time()
        minute_ago = current_time - 60

        if user_id not in self.user_message_counts:
            self.user_message_counts[user_id] = []

        # Limpiar mensajes antiguos
        self.user_message_counts[user_id] = [
            timestamp for timestamp in self.user_message_counts[user_id]
            if timestamp > minute_ago
        ]

        # Verificar límite
        if len(self.user_message_counts[user_id]) >= settings.MAX_MESSAGES_PER_MINUTE:
            return False

        # Agregar mensaje actual
        self.user_message_counts[user_id].append(current_time)
        return True

    def _record_metrics(self, message: str, response_time: float, user_id: int):
        """Registra métricas de la interacción"""
        try:
            from analytics.manager import analytics_manager
            analytics_manager.record_question(
                message, response_time, str(user_id))
        except Exception as e:
            logger.error(f"Error al registrar métricas: {e}")

    # Métodos de redirección para comandos (usan datos reales de documentos)
    async def _rooms_command_redirect(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Redirige /rooms al sistema de callbacks que usa documentos"""
        from ai.fallback_handler import get_room_info_from_documents
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        try:
            logger.info(
                f"Usuario {update.effective_user.id} usó comando /rooms")
            analytics_manager.track_event(
                "command_rooms", {"user_id": update.effective_user.id})

            # Usar el sistema que ya funciona con documentos reales
            response = get_room_info_from_documents()
            keyboard = [
                [InlineKeyboardButton(
                    "💰 Habitación más económica", callback_data="cheapest_room")],
                [InlineKeyboardButton(
                    "💎 Habitación más lujosa", callback_data="most_expensive_room")],
                [InlineKeyboardButton("📞 Reservar", callback_data="reservar")],
                [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error en comando /rooms: {e}")
            await update.message.reply_text("❌ Lo siento, hubo un error. Intenta de nuevo.")

    async def _restaurants_command_redirect(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Redirige /restaurants al sistema de callbacks que usa documentos"""
        from ai.fallback_handler import get_restaurant_info_from_documents
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        try:
            logger.info(
                f"Usuario {update.effective_user.id} usó comando /restaurants")
            analytics_manager.track_event("command_restaurants", {
                                          "user_id": update.effective_user.id})

            # Usar el sistema que ya funciona con documentos reales
            response = get_restaurant_info_from_documents()
            keyboard = [
                [InlineKeyboardButton(
                    "📞 Reservar mesa", callback_data="reservar_mesa")],
                [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error en comando /restaurants: {e}")
            await update.message.reply_text("❌ Lo siento, hubo un error. Intenta de nuevo.")

    async def _amenities_command_redirect(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Redirige /amenities al sistema de callbacks que usa documentos"""
        from ai.fallback_handler import get_amenities_info_from_documents
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        try:
            logger.info(
                f"Usuario {update.effective_user.id} usó comando /amenities")
            analytics_manager.track_event(
                "command_amenities", {"user_id": update.effective_user.id})

            # Usar el sistema que ya funciona con documentos reales
            response = get_amenities_info_from_documents()
            keyboard = [
                [InlineKeyboardButton(
                    "📞 Más información", callback_data="reservar")],
                [InlineKeyboardButton("🔙 Volver", callback_data="volver")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error en comando /amenities: {e}")
            await update.message.reply_text("❌ Lo siento, hubo un error. Intenta de nuevo.")

    async def _contact_command_redirect(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Redirige /contact al sistema de callbacks que usa documentos"""
        from ai.fallback_handler import get_contact_info_from_documents
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        try:
            logger.info(
                f"Usuario {update.effective_user.id} usó comando /contact")
            analytics_manager.track_event(
                "command_contact", {"user_id": update.effective_user.id})

            # Usar el sistema que ya funciona con documentos reales
            response = get_contact_info_from_documents()
            keyboard = [
                [InlineKeyboardButton(" Volver", callback_data="volver")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error en comando /contact: {e}")
            await update.message.reply_text("❌ Lo siento, hubo un error. Intenta de nuevo.")

    def run(self):
        """Ejecuta el bot con gestión de recursos"""
        logger.info("🤖 Iniciando ChatBot de Hotelería...")
        logger.info(f"🏨 Empresa: {settings.EMPRESA_NOMBRE}")

        # Mostrar configuración activa
        self._log_configuration()

        # Inicializar modelos de IA antes de empezar
        logger.info("🧠 Pre-cargando modelos de IA...")
        ai_ready = self._initialize_ai_models()
        if ai_ready:
            logger.info("🎯 Bot listo con IA completa")
        else:
            logger.info("📋 Bot listo con respuestas básicas")

        logger.info("🚀 Bot ejecutándose... (Ctrl+C para detener)")

        try:
            self.app.run_polling()
        except KeyboardInterrupt:
            logger.info("⏹️ Bot detenido por el usuario")
        except Exception as e:
            logger.error(f"❌ Error al ejecutar el bot: {e}")
            raise
        finally:
            self._cleanup_resources()

    def _log_configuration(self):
        """Log de la configuración activa"""
        logger.info("⚙️ Configuración activa:")
        logger.info(
            f"  - Lazy loading: {'✅' if settings.LAZY_LOAD_MODELS else '❌'}")
        logger.info(
            f"  - Model caching: {'✅' if settings.ENABLE_MODEL_CACHING else '❌'}")
        logger.info(
            f"  - Analytics: {'✅' if settings.ENABLE_ANALYTICS else '❌'}")
        logger.info(
            f"  - Rich responses: {'✅' if settings.ENABLE_RICH_RESPONSES else '❌'}")
        logger.info(f"  - Max cache size: {settings.MAX_CACHE_SIZE}")
        logger.info(
            f"  - Max concurrent requests: {settings.MAX_CONCURRENT_REQUESTS}")

    def _cleanup_resources(self):
        """Limpia recursos al cerrar el bot"""
        try:
            logger.info("🧹 Limpiando recursos...")

            # Limpiar cache expirado
            try:
                from ai.cache import response_cache
                expired_count = response_cache.cleanup_expired()
                logger.info(
                    f"🗑️ {expired_count} entradas de cache expiradas limpiadas")
            except ImportError:
                pass

            # Estadísticas finales
            self._log_final_stats()

            logger.info("✅ Recursos limpiados correctamente")

        except Exception as e:
            logger.error(f"❌ Error al limpiar recursos: {e}")

    def _log_final_stats(self):
        """Log estadísticas finales"""
        try:
            from ai.cache import response_cache
            from ai.models import ai_models

            cache_stats = response_cache.get_stats()
            logger.info("📊 Estadísticas finales:")
            logger.info(
                f"  - Cache hits: {cache_stats['hits']} ({cache_stats['hit_rate']}%)")
            logger.info(
                f"  - Cache size: {cache_stats['cache_size']}/{cache_stats['max_size']}")

            if settings.LAZY_LOAD_MODELS:
                model_stats = ai_models.get_stats()
                if 'concurrency' in model_stats:
                    concurrency_stats = model_stats['concurrency']
                    logger.info(
                        f"  - Total requests: {concurrency_stats['total_requests']}")

        except Exception as e:
            logger.debug(f"Error al obtener estadísticas finales: {e}")

    async def _handle_clear_cache(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando para limpiar el cache (solo para administradores)"""
        try:
            # Aquí podrías añadir verificación de permisos de admin
            user_id = update.effective_user.id

            from ai.cache import response_cache

            # Obtener estadísticas antes de limpiar
            old_stats = response_cache.get_stats()

            # Limpiar cache
            response_cache.clear()

            # Confirmar limpieza
            await update.message.reply_text(
                f"🧹 Cache limpiado exitosamente!\n\n"
                f"📊 Estadísticas anteriores:\n"
                f"• Entradas eliminadas: {old_stats['cache_size']}\n"
                f"• Hit rate anterior: {old_stats['hit_rate']}%\n"
                f"• Total requests: {old_stats['total_requests']}"
            )

            logger.info(f"🧹 Cache limpiado por usuario {user_id}")

        except Exception as e:
            logger.error(f"❌ Error al limpiar cache: {e}")
            await update.message.reply_text("❌ Error al limpiar el cache.")

    def _initialize_ai_models(self):
        """Inicializa los modelos de IA para uso inmediato"""
        try:
            logger.info("🧠 Inicializando modelos de IA...")
            from ai.models import ai_models
            
            # Forzar carga del vectorstore
            logger.info("🔄 Cargando vectorstore...")
            
            # Realizar una búsqueda de prueba para activar los modelos
            if ai_models.use_lazy_loading:
                logger.info("⚠️ Modo lazy loading - los modelos se cargarán cuando sean necesarios")
                return True
            else:
                test_results = vectorstore_manager.search_context("hotel", k=1)
                
                if test_results:
                    logger.info("✅ Modelos de IA cargados y funcionando")
                    return True
                else:
                    logger.warning("⚠️ Modelos inicializados pero sin resultados de prueba")
                    return False
                
        except Exception as e:
            logger.error(f"❌ Error inicializando modelos de IA: {e}")
            return False
