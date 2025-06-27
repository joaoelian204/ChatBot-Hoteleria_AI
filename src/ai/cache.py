"""
Sistema de cache mejorado para respuestas con límites de tamaño
"""
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from config.settings import settings
from utils.logger import logger
from utils.text_processor import generate_cache_key


class ResponseCache:
    """Sistema de cache mejorado para respuestas de IA con límites de tamaño"""

    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = timedelta(hours=settings.CACHE_DURATION_HOURS)
        self.max_size = settings.MAX_CACHE_SIZE
        self.access_times: Dict[str, float] = {}
        self.stats = {
            'hits': 0,
            'misses': 0,
            'total_requests': 0,
            'evictions': 0
        }

        logger.info(
            f"🗂️ ResponseCache inicializado: max_size={self.max_size}, duration={settings.CACHE_DURATION_HOURS}h")

    def get(self, question: str) -> Optional[str]:
        """Obtiene respuesta del cache si existe y es válida"""
        cache_key = generate_cache_key(question)
        self.stats['total_requests'] += 1

        if cache_key in self.cache:
            cached_data = self.cache[cache_key]

            # Verificar si no ha expirado
            if datetime.now() - cached_data['timestamp'] < self.cache_duration:
                # Actualizar tiempo de acceso para LRU
                self.access_times[cache_key] = time.time()
                self.stats['hits'] += 1
                logger.debug(f"✅ Cache hit para: {question[:50]}...")
                return cached_data['response']
            else:
                # Expirar entrada
                self._remove_entry(cache_key)

        self.stats['misses'] += 1
        logger.debug(f"❌ Cache miss para: {question[:50]}...")
        return None

    def set(self, question: str, response: str):
        """Guarda respuesta en el cache con gestión de tamaño"""
        cache_key = generate_cache_key(question)

        # Si el cache está lleno, eliminar el menos usado
        if len(self.cache) >= self.max_size and cache_key not in self.cache:
            self._evict_least_recently_used()

        # Almacenar en cache
        self.cache[cache_key] = {
            'response': response,
            'timestamp': datetime.now(),
            'question': question,
            'access_count': 1
        }
        self.access_times[cache_key] = time.time()

        logger.debug(
            f"💾 Respuesta cacheada: {question[:50]}... ({len(self.cache)}/{self.max_size})")

    def _evict_least_recently_used(self):
        """Elimina la entrada menos recientemente usada"""
        if not self.access_times:
            return

        # Encontrar la clave con el tiempo de acceso más antiguo
        oldest_key = min(self.access_times, key=self.access_times.get)
        self._remove_entry(oldest_key)
        self.stats['evictions'] += 1

        logger.debug(f"🗑️ Entrada evicted del cache (LRU): {oldest_key}")

    def _remove_entry(self, cache_key: str):
        """Elimina una entrada específica del cache"""
        if cache_key in self.cache:
            del self.cache[cache_key]
        if cache_key in self.access_times:
            del self.access_times[cache_key]

    def clear(self):
        """Limpia todo el cache"""
        self.cache.clear()
        self.access_times.clear()
        self.stats['evictions'] = 0
        logger.info("🧹 Cache limpiado completamente")

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas detalladas del cache"""
        total = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total * 100) if total > 0 else 0

        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'total_requests': self.stats['total_requests'],
            'hit_rate': round(hit_rate, 2),
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'usage_percent': round((len(self.cache) / self.max_size) * 100, 2),
            'evictions': self.stats['evictions'],
            'duration_hours': settings.CACHE_DURATION_HOURS
        }

    def cleanup_expired(self):
        """Limpia entradas expiradas del cache"""
        now = datetime.now()
        expired_keys = [
            key for key, data in self.cache.items()
            if now - data['timestamp'] > self.cache_duration
        ]

        for key in expired_keys:
            self._remove_entry(key)

        if expired_keys:
            logger.info(
                f"🧹 Limpiadas {len(expired_keys)} entradas expiradas del cache")

        return len(expired_keys)

    def get_cache_contents(self) -> Dict[str, Any]:
        """Obtiene el contenido del cache para inspección"""
        return {
            'entries': [
                {
                    'question': data['question'][:100] + '...' if len(data['question']) > 100 else data['question'],
                    'timestamp': data['timestamp'].isoformat(),
                    'response_length': len(data['response'])
                }
                for data in self.cache.values()
            ],
            'total_entries': len(self.cache)
        }


# Instancia global del cache
response_cache = ResponseCache()
