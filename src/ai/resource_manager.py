"""
Gestión de recursos y carga perezosa de modelos de IA
"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Any, Dict, Optional

from config.settings import settings
from utils.logger import logger


class ModelCache:
    """Cache inteligente para modelos de IA con límites de tamaño"""

    def __init__(self, max_size: int = None):
        self.max_size = max_size or settings.MAX_CACHE_SIZE
        self.cache: Dict[str, Any] = {}
        self.access_times: Dict[str, float] = {}
        self.lock = Lock()

    def get(self, key: str) -> Optional[Any]:
        """Obtiene un modelo del cache"""
        with self.lock:
            if key in self.cache:
                self.access_times[key] = time.time()
                logger.debug(f"✅ Modelo {key} obtenido del cache")
                return self.cache[key]
            return None

    def put(self, key: str, model: Any):
        """Almacena un modelo en el cache"""
        with self.lock:
            # Si el cache está lleno, eliminar el menos usado
            if len(self.cache) >= self.max_size:
                self._evict_least_recently_used()

            self.cache[key] = model
            self.access_times[key] = time.time()
            logger.info(
                f"🗂️ Modelo {key} almacenado en cache ({len(self.cache)}/{self.max_size})")

    def _evict_least_recently_used(self):
        """Elimina el modelo menos recientemente usado"""
        if not self.access_times:
            return

        oldest_key = min(self.access_times, key=self.access_times.get)
        del self.cache[oldest_key]
        del self.access_times[oldest_key]
        logger.info(f"🗑️ Modelo {oldest_key} eliminado del cache (LRU)")

    def clear(self):
        """Limpia el cache"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
            logger.info("🧹 Cache de modelos limpiado")

    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del cache"""
        with self.lock:
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'models': list(self.cache.keys()),
                'usage_percent': (len(self.cache) / self.max_size) * 100
            }


class ConcurrencyManager:
    """Gestión de concurrencia para peticiones de IA"""

    def __init__(self, max_concurrent: int = None):
        self.max_concurrent = max_concurrent or settings.MAX_CONCURRENT_REQUESTS
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_concurrent)
        self.active_requests = 0
        self.total_requests = 0
        self.lock = Lock()

        logger.info(
            f"🚦 ConcurrencyManager inicializado: max_concurrent={self.max_concurrent}")

    async def acquire(self):
        """Adquiere un slot de concurrencia"""
        await self.semaphore.acquire()
        with self.lock:
            self.active_requests += 1
            self.total_requests += 1
            logger.debug(
                f"📈 Requests activos: {self.active_requests}/{self.max_concurrent}")

    def release(self):
        """Libera un slot de concurrencia"""
        with self.lock:
            self.active_requests = max(0, self.active_requests - 1)
            logger.debug(
                f"📉 Requests activos: {self.active_requests}/{self.max_concurrent}")
        self.semaphore.release()

    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de concurrencia"""
        with self.lock:
            return {
                'active_requests': self.active_requests,
                'max_concurrent': self.max_concurrent,
                'total_requests': self.total_requests,
                'usage_percent': (self.active_requests / self.max_concurrent) * 100
            }


class LazyModelLoader:
    """Cargador perezoso de modelos de IA"""

    def __init__(self):
        self.cache = ModelCache() if settings.ENABLE_MODEL_CACHING else None
        self.concurrency_manager = ConcurrencyManager()
        self.loading_locks: Dict[str, Lock] = {}
        self.models_registry: Dict[str, Dict[str, Any]] = {}

        logger.info("🚀 LazyModelLoader inicializado:")
        logger.info(f"  - Cache habilitado: {settings.ENABLE_MODEL_CACHING}")
        logger.info(f"  - Carga perezosa: {settings.LAZY_LOAD_MODELS}")
        logger.info(
            f"  - Max concurrencia: {settings.MAX_CONCURRENT_REQUESTS}")

    def register_model(self, model_name: str, model_class: Any, **kwargs):
        """Registra un modelo para carga perezosa"""
        self.models_registry[model_name] = {
            'model_class': model_class,
            'kwargs': kwargs,
            'loaded': False,
            'instance': None
        }
        logger.info(f"📝 Modelo registrado: {model_name}")

    async def get_model(self, model_name: str) -> Any:
        """Obtiene un modelo, cargándolo si es necesario"""
        # Verificar cache primero
        if self.cache:
            cached_model = self.cache.get(model_name)
            if cached_model:
                return cached_model

        # Si no está en cache, cargar
        return await self._load_model(model_name)

    async def _load_model(self, model_name: str) -> Any:
        """Carga un modelo de forma thread-safe"""
        if model_name not in self.models_registry:
            raise ValueError(f"Modelo {model_name} no registrado")

        # Lock por modelo para evitar cargas duplicadas
        if model_name not in self.loading_locks:
            self.loading_locks[model_name] = Lock()

        with self.loading_locks[model_name]:
            model_info = self.models_registry[model_name]

            # Verificar si ya fue cargado por otro hilo
            if model_info['loaded'] and model_info['instance']:
                logger.debug(f"✅ Modelo {model_name} ya cargado por otro hilo")
                return model_info['instance']

            # Controlar concurrencia
            await self.concurrency_manager.acquire()

            try:
                logger.info(f"⏳ Cargando modelo: {model_name}")
                start_time = time.time()

                # Cargar modelo en hilo separado para no bloquear
                loop = asyncio.get_event_loop()
                model_instance = await loop.run_in_executor(
                    self.concurrency_manager.thread_pool,
                    self._instantiate_model,
                    model_name
                )

                load_time = time.time() - start_time
                logger.info(
                    f"✅ Modelo {model_name} cargado en {load_time:.2f}s")

                # Actualizar registro
                model_info['loaded'] = True
                model_info['instance'] = model_instance

                # Almacenar en cache si está habilitado
                if self.cache:
                    self.cache.put(model_name, model_instance)

                return model_instance

            finally:
                self.concurrency_manager.release()

    def _instantiate_model(self, model_name: str) -> Any:
        """Instancia un modelo (ejecutado en hilo separado)"""
        model_info = self.models_registry[model_name]
        model_class = model_info['model_class']
        kwargs = model_info['kwargs']

        try:
            return model_class(**kwargs)
        except Exception as e:
            logger.error(f"❌ Error al cargar modelo {model_name}: {e}")
            raise

    def unload_model(self, model_name: str):
        """Descarga un modelo de la memoria"""
        if model_name in self.models_registry:
            self.models_registry[model_name]['loaded'] = False
            self.models_registry[model_name]['instance'] = None

            if self.cache:
                # El cache maneja la eliminación automáticamente
                pass

            logger.info(f"🗑️ Modelo {model_name} descargado")

    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del loader"""
        stats = {
            'registered_models': len(self.models_registry),
            'loaded_models': sum(1 for m in self.models_registry.values() if m['loaded']),
            'concurrency': self.concurrency_manager.get_stats()
        }

        if self.cache:
            stats['cache'] = self.cache.get_stats()

        return stats


# Instancia global del loader
resource_manager = LazyModelLoader() if settings.LAZY_LOAD_MODELS else None
