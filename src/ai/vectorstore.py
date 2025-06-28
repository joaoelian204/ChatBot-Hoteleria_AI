"""
Gestión de vectorstore y documentos
"""
import os
from typing import List

from config.settings import settings

# Importar adaptador de base de datos - REQUERIDO
from database.adapter import db_vectorstore_adapter
from utils.logger import logger

# Importaciones de langchain - condicionales para evitar errores
try:
    from langchain_community.document_loaders import (
        Docx2txtLoader,
        PyPDFLoader,
        TextLoader,
    )
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
    logger.info("✅ Dependencias de LangChain cargadas correctamente")
except ImportError as e:
    logger.warning(f"⚠️ Dependencias de LangChain no disponibles: {e}")
    logger.info("💡 Instala: pip install langchain langchain-community faiss-cpu")
    LANGCHAIN_AVAILABLE = False

from ai.models import ai_models

DATABASE_AVAILABLE = True
logger.info("🗄️ Sistema configurado para usar base de datos SQLite")


class VectorStoreManager:
    """Gestión del vectorstore y documentos"""

    def __init__(self):
        self.vectorstore = None
        self._documents_processed = False
        self._chunks = []
        # Sistema configurado para usar SIEMPRE base de datos SQLite
        self.use_database = True

        # Inicializar text_splitter solo si langchain está disponible
        if LANGCHAIN_AVAILABLE:
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            logger.info("🗄️ VectorStore inicializado - MODO BASE DE DATOS")
            logger.info("🔄 VectorStore configurado en modo lazy loading")
        else:
            self.text_splitter = None
            logger.warning(
                "⚠️ VectorStore inicializado SIN dependencias de LangChain")
            logger.info(
                "💡 Funcionalidad limitada - instala las dependencias para funcionalidad completa")

    def _load_document(self, file_path: str) -> List:
        """Carga un documento según su extensión"""
        extension = os.path.splitext(file_path)[1].lower()

        try:
            if extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif extension == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
            elif extension in ['.docx', '.doc']:
                loader = Docx2txtLoader(file_path)
            else:
                logger.warning(f"Formato no soportado: {extension}")
                return []

            documents = loader.load()
            logger.info(
                f"Documento cargado: {file_path} ({len(documents)} páginas)")
            return documents

        except Exception as e:
            logger.error(f"Error al cargar {file_path}: {e}")
            return []

    def _prepare_documents(self):
        """Prepara los documentos desde la base de datos SQLite"""
        if self._documents_processed:
            return

        # SIEMPRE usar base de datos como fuente principal
        self._prepare_documents_from_database()

    def _prepare_documents_from_database(self):
        """Prepara documentos desde la base de datos SQLite"""
        try:
            logger.info(
                "🗄️ Cargando documentos desde la base de datos SQLite...")
            documentos_db = db_vectorstore_adapter.get_all_documents_for_vectorstore()

            if not documentos_db:
                logger.warning(
                    "⚠️ No se encontraron documentos en la base de datos")
                logger.info(
                    "💡 Ejecuta: python migrate_to_database.py --migrate")
                return

            # Convertir a formato Document de langchain
            try:
                from langchain_core.documents import Document
            except ImportError:
                try:
                    from langchain.schema import Document
                except ImportError:
                    logger.error(
                        "❌ No se puede importar Document de langchain")
                    return

            all_docs = []

            for doc_data in documentos_db:
                doc = Document(
                    page_content=doc_data['page_content'],
                    metadata=doc_data['metadata']
                )
                all_docs.append(doc)

            logger.info(f"📄 Documentos de BD obtenidos: {len(all_docs)}")

            # Dividir documentos en chunks
            self._chunks = self.text_splitter.split_documents(all_docs)
            logger.info(
                f"📄 Documentos de BD divididos en {len(self._chunks)} chunks")
            self._documents_processed = True

        except Exception as e:
            logger.error(f"❌ Error al preparar documentos desde BD: {e}")
            logger.error(
                "� Asegúrate de ejecutar la migración: python migrate_to_database.py --migrate")
            # No hacer fallback a archivos - requerir base de datos
            raise RuntimeError(
                "Base de datos requerida pero no disponible. Ejecuta la migración primero.")

    def _prepare_documents_from_files(self):
        """Prepara documentos desde archivos (método original)"""
        all_docs = []

        if not settings.DOCUMENTOS_DIR.exists():
            logger.warning(
                f"La carpeta {settings.DOCUMENTOS_DIR} no existe. Creándola...")
            settings.DOCUMENTOS_DIR.mkdir(parents=True, exist_ok=True)
            return

        # Procesar todos los archivos en la carpeta documentos
        for file_name in os.listdir(settings.DOCUMENTOS_DIR):
            file_path = settings.DOCUMENTOS_DIR / file_name
            if file_path.is_file():
                documents = self._load_document(str(file_path))
                if documents:
                    all_docs.extend(documents)

        if all_docs:
            # Dividir documentos en chunks (esto no requiere modelos pesados)
            self._chunks = self.text_splitter.split_documents(all_docs)
            logger.info(f"📄 Documentos divididos en {len(self._chunks)} chunks")
            self._documents_processed = True
        else:
            logger.warning("⚠️ No se encontraron documentos para procesar")

    def _create_vectorstore(self):
        """Crea el vectorstore SOLO cuando sea necesario (modo síncrono - solo para carga inmediata)"""
        if self.vectorstore is not None:
            return  # Ya está creado

        # Preparar documentos si no se ha hecho
        self._prepare_documents()

        if not self._chunks:
            logger.warning("⚠️ No hay chunks disponibles para crear vectorstore")
            return

        # Verificar si lazy loading está habilitado
        if ai_models.use_lazy_loading:
            logger.info("⚠️ Lazy loading habilitado - usa search_context_async() para crear vectorstore")
            return

        # Aquí es donde se cargan los modelos pesados (solo modo inmediato)
        logger.info("⏳ Cargando modelo de embeddings (puede tardar un momento)...")
        try:
            embedding_model = ai_models.get_embedding_model_sync()
            if embedding_model:
                self.vectorstore = FAISS.from_documents(
                    self._chunks, embedding_model)
                logger.info("✅ Vectorstore creado exitosamente")
            else:
                logger.warning("⚠️ Modelo de embeddings no disponible")
        except Exception as e:
            logger.error(f"❌ Error creando vectorstore: {e}")

    def search_context(self, question: str, k: int = 3) -> List[str]:
        """Busca contexto relevante para una pregunta"""
        # Verificar si lazy loading está habilitado
        if ai_models.use_lazy_loading:
            logger.warning("⚠️ Lazy loading habilitado - usa search_context_async() en su lugar")
            return []

        # Si no existe el vectorstore, crearlo ahora (solo modo inmediato)
        if not self.vectorstore:
            logger.info(
                "🔄 Vectorstore no disponible, inicializando desde base de datos...")
            self._create_vectorstore()

        if not self.vectorstore:
            logger.warning("❌ Vectorstore no disponible después de intentar crearlo")
            return []

        try:
            docs = self.vectorstore.similarity_search(question, k=k)
            logger.info(
                f"✅ Encontrados {len(docs)} documentos relevantes desde BD")
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"❌ Error en búsqueda de contexto: {e}")
            return []

    async def search_context_async(self, question: str, k: int = 3) -> List[str]:
        """Busca contexto relevante para una pregunta (método asíncrono para lazy loading)"""
        if not self.vectorstore:
            # Intentar crear el vectorstore con lazy loading
            await self._create_vectorstore_async()

            if not self.vectorstore:
                logger.warning(
                    "❌ Vectorstore no disponible después de intentar crearlo")
                return []

        try:
            docs = self.vectorstore.similarity_search(question, k=k)
            logger.info(f"✅ Encontrados {len(docs)} documentos relevantes (async)")
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"❌ Error en búsqueda de contexto (async): {e}")
            return []

    async def _create_vectorstore_async(self):
        """Crea el vectorstore de forma asíncrona (para lazy loading)"""
        if self.vectorstore is not None:
            return  # Ya está creado

        # Preparar documentos si no se ha hecho
        self._prepare_documents()

        if not self._chunks:
            logger.warning("⚠️ No hay chunks disponibles para crear vectorstore")
            return

        logger.info("⏳ Cargando modelo de embeddings de forma asíncrona...")
        try:
            embedding_model = await ai_models.get_embedding_model()
            if embedding_model:
                self.vectorstore = FAISS.from_documents(
                    self._chunks, embedding_model)
                logger.info("✅ Vectorstore creado exitosamente (async)")
            else:
                logger.warning("⚠️ Modelo de embeddings no disponible")
        except Exception as e:
            logger.error(f"❌ Error al crear vectorstore async: {e}")

    def update_knowledge(self):
        """Actualiza el conocimiento del vectorstore (sin cargar modelos pesados)"""
        logger.info("📚 Actualizando conocimiento...")
        # Solo preparar documentos, no cargar modelos hasta que sea necesario
        self._prepare_documents()
        # Limpiar vectorstore existente para forzar recreación en próxima búsqueda
        self.vectorstore = None
        logger.info("✅ Conocimiento actualizado (lazy loading activado)")

    def reload_document(self, file_path: str):
        """Recarga un documento específico en el vectorstore"""
        try:
            logger.info(f"🔄 Recargando documento: {file_path}")

            # Para simplicidad, reconstruir todo el vectorstore
            # En una implementación más avanzada, se podría actualizar solo el documento específico
            self._create_vectorstore()

            logger.info(f"✅ Documento recargado: {file_path}")

        except Exception as e:
            logger.error(f"❌ Error al recargar documento {file_path}: {e}")

    def add_document(self, file_path: str):
        """Añade un nuevo documento al vectorstore"""
        try:
            logger.info(f"➕ Añadiendo documento: {file_path}")

            documents = self._load_document(file_path)
            if not documents:
                logger.warning(f"No se pudo cargar el documento: {file_path}")
                return

            # Dividir en chunks
            chunks = self.text_splitter.split_documents(documents)

            if self.vectorstore:
                # Añadir al vectorstore existente
                embedding_model = ai_models.get_embedding_model_sync()
                if embedding_model:
                    self.vectorstore.add_documents(chunks)
                    logger.info(
                        f"✅ Documento añadido: {file_path} ({len(chunks)} chunks)")
                else:
                    logger.error("Modelo de embeddings no disponible")
            else:
                # Crear nuevo vectorstore si no existe
                self._create_vectorstore()

        except Exception as e:
            logger.error(f"❌ Error al añadir documento {file_path}: {e}")

    def remove_document(self, file_path: str):
        """Elimina un documento del vectorstore"""
        try:
            logger.info(f"🗑️ Eliminando documento: {file_path}")

            # Para simplicidad, reconstruir todo el vectorstore sin el documento eliminado
            # En una implementación más avanzada, se podría eliminar solo el documento específico
            self._create_vectorstore()

            logger.info(f"✅ Documento eliminado: {file_path}")

        except Exception as e:
            logger.error(f"❌ Error al eliminar documento {file_path}: {e}")

    def get_document_count(self) -> int:
        """Retorna el número de documentos en el vectorstore"""
        if not self.vectorstore:
            return 0
        return len(self.vectorstore.docstore._dict)

    def get_stats(self) -> dict:
        """Retorna estadísticas del vectorstore"""
        if not self.vectorstore:
            return {
                'document_count': 0,
                'vectorstore_created': False,
                'embedding_model': 'N/A'
            }

        return {
            'document_count': self.get_document_count(),
            'vectorstore_created': True,
            'embedding_model': settings.MODELO_EMBEDDINGS
        }


# Instancia global del vectorstore
vectorstore_manager = VectorStoreManager()
