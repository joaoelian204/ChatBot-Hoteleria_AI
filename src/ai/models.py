"""
Gestión de modelos de IA con carga perezosa y gestión de recursos
"""
import os

import torch
from config.settings import settings
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from utils.logger import logger

# Import condicional del resource manager
def get_resource_manager():
    """Importa el resource manager solo cuando es necesario"""
    if settings.LAZY_LOAD_MODELS:
        try:
            from ai.resource_manager import resource_manager
            return resource_manager
        except ImportError as e:
            logger.warning(f"No se pudo importar resource_manager: {e}")
            return None
    return None


class ModelFactory:
    """Factory para crear instancias de modelos"""

    @staticmethod
    def create_summarizer():
        """Crea el modelo resumidor"""
        try:
            if os.environ.get("USE_DUMMY_MODELS"):
                return lambda *args, **kwargs: [{"summary_text": "Resumen dummy."}]

            device = "cpu"
            torch_dtype = torch.float32
            model_name = "mrm8488/bert2bert_shared-spanish-finetuned-summarization"

            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                torch_dtype=torch_dtype,
                device_map=None,
                load_in_8bit=False
            )
            return pipeline(
                "summarization",
                model=model,
                tokenizer=tokenizer,
                device=device
            )
        except Exception as e:
            logger.warning(f"No se pudo cargar el modelo de resumen: {e}")
            return lambda *args, **kwargs: [{"summary_text": "Resumen no disponible."}]

    @staticmethod
    def create_generator():
        """Crea el modelo generador"""
        try:
            if os.environ.get("USE_DUMMY_MODELS"):
                return lambda *args, **kwargs: [{"generated_text": "Respuesta dummy."}]

            device = "cpu"
            torch_dtype = torch.float32

            return pipeline(
                "text-generation",
                model="datificate/gpt2-small-spanish",
                device=device,
                torch_dtype=torch_dtype
            )
        except Exception as e:
            logger.warning(f"No se pudo cargar el modelo de generación: {e}")
            return lambda *args, **kwargs: [{"generated_text": "Respuesta no disponible."}]

    @staticmethod
    def create_embeddings():
        """Crea el modelo de embeddings"""
        try:
            if os.environ.get("USE_DUMMY_MODELS"):
                return None

            return HuggingFaceEmbeddings(
                model_name=settings.MODELO_EMBEDDINGS,
                model_kwargs={'device': "cpu"}
            )
        except Exception as e:
            logger.warning(f"No se pudo cargar el modelo de embeddings: {e}")
            return None

    @staticmethod
    def create_intent_classifier():
        """Crea el clasificador de intenciones"""
        try:
            if os.environ.get("USE_DUMMY_MODELS"):
                return lambda *args, **kwargs: [{"label": "general", "score": 1.0}]

            device = "cpu"
            torch_dtype = torch.float32

            return pipeline(
                "text-classification",
                model="facebook/bart-large-mnli",
                device=device,
                torch_dtype=torch_dtype,
                load_in_8bit=False
            )
        except Exception as e:
            logger.warning(
                f"No se pudo cargar el clasificador de intenciones: {e}")
            return lambda *args, **kwargs: [{"label": "general", "score": 1.0}]


class AIModels:
    """Gestión centralizada de modelos de IA con carga perezosa"""

    def __init__(self):
        self.resource_manager = get_resource_manager()
        self.use_lazy_loading = settings.LAZY_LOAD_MODELS and self.resource_manager is not None

        if self.use_lazy_loading:
            self._register_models()
            logger.info("🔄 Modelos registrados para carga perezosa")
        else:
            self._load_models_immediately()
            logger.info("⚡ Modelos cargados inmediatamente")

    def _register_models(self):
        """Registra modelos para carga perezosa"""
        if self.resource_manager:
            self.resource_manager.register_model(
                "summarizer",
                ModelFactory.create_summarizer
            )
            self.resource_manager.register_model(
                "generator",
                ModelFactory.create_generator
            )
            self.resource_manager.register_model(
                "embeddings",
                ModelFactory.create_embeddings
            )
            self.resource_manager.register_model(
                "intent_classifier",
                ModelFactory.create_intent_classifier
            )

    def _load_models_immediately(self):
        """Carga inmediata de todos los modelos (modo tradicional)"""
        try:
            logger.info("Inicializando modelos de IA...")

            self.resumidor = ModelFactory.create_summarizer()
            self.generador = ModelFactory.create_generator()
            self.embedding_model = ModelFactory.create_embeddings()
            self.intent_classifier = ModelFactory.create_intent_classifier()

            logger.info("✅ Modelos inicializados correctamente")

        except Exception as e:
            logger.error(f"❌ Error al inicializar modelos: {e}")
            # Fallback a modelos dummy
            self.generador = lambda *args, **kwargs: [
                {"generated_text": "Respuesta dummy."}]
            self.resumidor = lambda *args, **kwargs: [
                {"summary_text": "Resumen dummy."}]
            self.intent_classifier = lambda *args, **kwargs: [
                {"label": "dummy", "score": 1.0}]
            self.embedding_model = None
            logger.info("🔄 Usando modelos dummy como fallback")

    async def get_resumidor(self):
        """Retorna el modelo resumidor (con carga perezosa si está habilitada)"""
        if self.use_lazy_loading and self.resource_manager:
            return await self.resource_manager.get_model("summarizer")
        return self.resumidor

    async def get_generador(self):
        """Retorna el modelo generador (con carga perezosa si está habilitada)"""
        if self.use_lazy_loading and self.resource_manager:
            return await self.resource_manager.get_model("generator")
        return self.generador

    async def get_embedding_model(self):
        """Retorna el modelo de embeddings (con carga perezosa si está habilitada)"""
        if self.use_lazy_loading and self.resource_manager:
            return await self.resource_manager.get_model("embeddings")
        return self.embedding_model

    async def get_intent_classifier(self):
        """Retorna el clasificador de intenciones (con carga perezosa si está habilitada)"""
        if self.use_lazy_loading and self.resource_manager:
            return await self.resource_manager.get_model("intent_classifier")
        return self.intent_classifier

    # Métodos síncronos para compatibilidad hacia atrás
    def get_resumidor_sync(self):
        """Versión síncrona - solo para carga inmediata"""
        if self.use_lazy_loading:
            raise RuntimeError(
                "Usa get_resumidor() async cuando lazy loading está habilitado")
        return self.resumidor

    def get_generador_sync(self):
        """Versión síncrona - solo para carga inmediata"""
        if self.use_lazy_loading:
            raise RuntimeError(
                "Usa get_generador() async cuando lazy loading está habilitado")
        return self.generador

    def get_embedding_model_sync(self):
        """Versión síncrona - solo para carga inmediata"""
        if self.use_lazy_loading:
            raise RuntimeError(
                "Usa get_embedding_model() async cuando lazy loading está habilitado")
        return self.embedding_model

    def get_intent_classifier_sync(self):
        """Versión síncrona - solo para carga inmediata"""
        if self.use_lazy_loading:
            raise RuntimeError(
                "Usa get_intent_classifier() async cuando lazy loading está habilitado")
        return self.intent_classifier

    def get_stats(self) -> dict:
        """Obtiene estadísticas de los modelos"""
        if self.use_lazy_loading and self.resource_manager:
            return self.resource_manager.get_stats()
        else:
            return {
                'mode': 'immediate_loading',
                'models_loaded': 4,
                'resumidor': self.resumidor is not None,
                'generador': self.generador is not None,
                'embedding_model': self.embedding_model is not None,
                'intent_classifier': self.intent_classifier is not None
            }


# Instancia global de modelos
ai_models = AIModels()
