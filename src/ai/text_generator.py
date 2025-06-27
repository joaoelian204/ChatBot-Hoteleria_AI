"""
Generación de texto con IA
"""
from typing import List

from utils.logger import logger

from .fallback_handler import generate_fallback_response
from .models import ai_models  # Reactivado para usar modelos de IA


def generate_response(question: str, context_docs: List[str]) -> str:
    """Genera una respuesta usando IA"""
    try:
        # Si no hay contexto, usar respuesta por defecto
        if not context_docs:
            logger.info("No hay contexto disponible, usando fallback")
            return generate_fallback_response(question)

        # Usar contexto completo sin resumir para respuestas más detalladas
        context_summary = ' '.join(context_docs)

        # Intentar generar respuesta usando IA
        response = _generate_with_context(question, context_summary)

        # Si la respuesta es muy corta o no válida, usar fallback
        if not _validate_response(response) or len(response.strip()) < 30:
            logger.info("Respuesta de IA muy corta o inválida, usando fallback handler")
            return generate_fallback_response(question)

        logger.info("✅ Respuesta generada exitosamente con IA")
        return response

    except Exception as e:
        logger.error(f"Error al generar respuesta: {e}")
        logger.info("🔄 Usando fallback handler debido a error")
        return generate_fallback_response(question)


async def generate_response_async(question: str, context_docs: List[str]) -> str:
    """Genera una respuesta usando IA (versión asíncrona)"""
    try:
        # Si no hay contexto, usar respuesta por defecto
        if not context_docs:
            logger.info("No hay contexto disponible, usando fallback (async)")
            return generate_fallback_response(question)

        # Usar contexto completo sin resumir para respuestas más detalladas
        context_summary = ' '.join(context_docs)

        # Intentar generar respuesta usando IA
        response = await _generate_with_context_async(question, context_summary)

        # Si la respuesta es muy corta o no válida, usar fallback
        if not _validate_response(response) or len(response.strip()) < 30:
            logger.info("Respuesta de IA muy corta o inválida, usando fallback handler (async)")
            return generate_fallback_response(question)

        logger.info("✅ Respuesta generada exitosamente con IA (async)")
        return response

    except Exception as e:
        logger.error(f"Error al generar respuesta async: {e}")
        logger.info("🔄 Usando fallback handler debido a error (async)")
        return generate_fallback_response(question)


def _generate_with_context(question: str, context: str) -> str:
    """Genera respuesta usando contexto con IA como principal y fallback como respaldo"""
    try:
        logger.info("🤖 Intentando generar respuesta con IA...")
        
        # Verificar si lazy loading está habilitado
        if ai_models.use_lazy_loading:
            logger.warning("⚠️ Lazy loading habilitado - usa generate_response_async() en su lugar")
            return generate_fallback_response(question)
        
        # Obtener el modelo generador (solo para modo síncrono)
        generador = ai_models.get_generador_sync()
        
        if generador is None:
            logger.warning("⚠️ Modelo generador no disponible, usando fallback")
            return generate_fallback_response(question)
        
        # Crear prompt más estructurado y contextual
        prompt = f"""Contexto del hotel: {context[:300]}...

Pregunta del cliente: {question}

Responde de manera amigable y profesional, usando la información del contexto. Si no encuentras la información específica, menciona que puedes contactar al personal del hotel.

Respuesta:"""
        
        logger.info(f"📝 Generando respuesta para: '{question[:50]}...'")
        
        # Generar respuesta con parámetros optimizados
        response = generador(
            prompt,
            max_length=300,  # Aumentado para respuestas más completas
            temperature=0.7,  # Balance entre creatividad y consistencia
            do_sample=True,   # Habilitar sampling para respuestas más naturales
            num_return_sequences=1,
            pad_token_id=generador.tokenizer.eos_token_id if hasattr(generador, 'tokenizer') else None,
            truncation=True,
            repetition_penalty=1.2  # Evitar repeticiones
        )
        
        # Extraer la respuesta generada
        if isinstance(response, list) and len(response) > 0:
            generated_text = response[0].get('generated_text', '')
        else:
            generated_text = str(response)
        
        # Limpiar la respuesta (remover el prompt)
        if prompt in generated_text:
            answer = generated_text[len(prompt):].strip()
        else:
            answer = generated_text.strip()
        
        # Limpiar y validar la respuesta
        answer = _clean_response(answer)
        
        logger.info(f"🧠 Respuesta generada: '{answer[:100]}...'")
        
        # Validar respuesta antes de devolverla
        if _validate_response(answer) and not _contains_nonsense(answer):
            logger.info("✅ Respuesta de IA válida")
            return answer
        else:
            logger.warning("❌ Respuesta de IA inválida o contiene nonsense, usando fallback")
            return generate_fallback_response(question)

    except Exception as e:
        logger.error(f"❌ Error al generar con contexto: {e}")
        logger.info("🔄 Usando fallback handler debido a error en generación")
        return generate_fallback_response(question)


async def _generate_with_context_async(question: str, context: str) -> str:
    """Genera respuesta usando contexto (versión asíncrona)"""
    try:
        logger.info("🤖 Intentando generar respuesta con IA (async)...")
        
        # Obtener el modelo generador de forma asíncrona
        generador = await ai_models.get_generador()
        
        if generador is None:
            logger.warning("⚠️ Modelo generador no disponible, usando fallback (async)")
            return generate_fallback_response(question)
        
        # Crear prompt más estructurado y contextual
        prompt = f"""Contexto del hotel: {context[:300]}...

Pregunta del cliente: {question}

Responde de manera amigable y profesional, usando la información del contexto. Si no encuentras la información específica, menciona que puedes contactar al personal del hotel.

Respuesta:"""
        
        logger.info(f"📝 Generando respuesta para: '{question[:50]}...' (async)")
        
        # Generar respuesta con parámetros optimizados
        response = generador(
            prompt,
            max_length=300,
            temperature=0.7,
            do_sample=True,
            num_return_sequences=1,
            pad_token_id=generador.tokenizer.eos_token_id if hasattr(generador, 'tokenizer') else None,
            truncation=True,
            repetition_penalty=1.2
        )
        
        # Extraer la respuesta generada
        if isinstance(response, list) and len(response) > 0:
            generated_text = response[0].get('generated_text', '')
        else:
            generated_text = str(response)
        
        # Limpiar la respuesta (remover el prompt)
        if prompt in generated_text:
            answer = generated_text[len(prompt):].strip()
        else:
            answer = generated_text.strip()
        
        # Limpiar y validar la respuesta
        answer = _clean_response(answer)
        
        logger.info(f"🧠 Respuesta generada (async): '{answer[:100]}...'")
        
        # Validar respuesta antes de devolverla
        if _validate_response(answer) and not _contains_nonsense(answer):
            logger.info("✅ Respuesta de IA válida (async)")
            return answer
        else:
            logger.warning("❌ Respuesta de IA inválida o contiene nonsense, usando fallback (async)")
            return generate_fallback_response(question)

    except Exception as e:
        logger.error(f"❌ Error al generar con contexto async: {e}")
        logger.info("🔄 Usando fallback handler debido a error en generación (async)")
        return generate_fallback_response(question)


def _clean_response(response: str) -> str:
    """Limpia la respuesta generada"""
    if not response:
        return ""
    
    # Remover caracteres extraños y normalizar
    response = response.replace('\n\n\n', '\n\n')
    response = response.replace('  ', ' ')
    response = response.replace('\t', ' ')
    
    # Remover líneas vacías al inicio y final
    response = response.strip()
    
    # Limitar longitud
    if len(response) > 800:
        response = response[:800] + "..."
    
    # Asegurar que la respuesta termine con un punto si no lo tiene
    if response and not response.endswith(('.', '!', '?')):
        response += '.'

    return response.strip()


def _validate_response(response: str) -> bool:
    """Valida que la respuesta sea adecuada"""
    if not response or len(response.strip()) < 10:
        return False

    # Verificar contenido inapropiado o errores
    inappropriate_words = ['error', 'undefined', 'null', 'exception', 'traceback', 'stack']
    response_lower = response.lower()
    for word in inappropriate_words:
        if word in response_lower:
            return False

    # Verificar que no sea solo el prompt repetido
    if response.lower().startswith('contexto del hotel:') or response.lower().startswith('pregunta del cliente:'):
        return False

    return True


def _contains_nonsense(response: str) -> bool:
    """Detecta si la respuesta contiene texto sin sentido"""
    nonsense_patterns = [
        "muebles", "oficina de correos", "suite de correo",
        "enseñanza media", "educación media", "sistema de educación",
        "clasificado de cita", "IQS", "actividades que en una sociedad",
        "12:00 - 27:00",  # Horario imposible
        "undefined", "null", "error", "exception",
        "token", "model", "generator", "pipeline"
    ]

    response_lower = response.lower()
    for pattern in nonsense_patterns:
        if pattern.lower() in response_lower:
            return True

    # Detectar repeticiones excesivas
    words = response.split()
    if len(words) > 10:
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
            if word_count[word] > 5:  # Misma palabra más de 5 veces
                return True

    # Detectar respuestas que son solo el prompt
    if response.lower().count('contexto del hotel:') > 0 and response.lower().count('pregunta del cliente:') > 0:
        return True

    return False
