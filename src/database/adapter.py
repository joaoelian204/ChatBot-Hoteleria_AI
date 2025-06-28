"""
Adaptador de vectorstore para usar base de datos SQLite
"""
from typing import List

from database.repository import contenido_repository
from utils.logger import logger


class DatabaseVectorStoreAdapter:
    """Adaptador para usar contenido de base de datos en el vectorstore"""

    def __init__(self):
        self.repository = contenido_repository

    def get_all_documents_for_vectorstore(self) -> List[dict]:
        """Obtiene todos los documentos de la base de datos formateados para vectorstore"""
        try:
            contenido = self.repository.obtener_todo_contenido()
            documentos_vectorstore = []

            for item in contenido:
                # Crear un documento formateado para el vectorstore
                documento = {
                    'page_content': self._formatear_contenido_para_vectorstore(item),
                    'metadata': {
                        'id': item['id'],
                        'categoria': item['categoria'],
                        'titulo': item['titulo'],
                        'precio': item.get('precio'),
                        'source': f"db_{item['categoria']}_{item['id']}",
                        **item.get('metadatos', {})
                    }
                }
                documentos_vectorstore.append(documento)

            logger.info(
                f"✅ Preparados {len(documentos_vectorstore)} documentos de la base de datos para vectorstore")
            return documentos_vectorstore

        except Exception as e:
            logger.error(
                f"❌ Error al obtener documentos de la base de datos: {e}")
            return []

    def get_documents_by_category(self, categoria: str) -> List[dict]:
        """Obtiene documentos por categoría específica"""
        try:
            contenido = self.repository.obtener_por_categoria(categoria)
            documentos_vectorstore = []

            for item in contenido:
                documento = {
                    'page_content': self._formatear_contenido_para_vectorstore(item),
                    'metadata': {
                        'id': item['id'],
                        'categoria': item['categoria'],
                        'titulo': item['titulo'],
                        'precio': item.get('precio'),
                        'source': f"db_{item['categoria']}_{item['id']}",
                        **item.get('metadatos', {})
                    }
                }
                documentos_vectorstore.append(documento)

            logger.info(
                f"✅ Preparados {len(documentos_vectorstore)} documentos de categoría '{categoria}'")
            return documentos_vectorstore

        except Exception as e:
            logger.error(
                f"❌ Error al obtener documentos de categoría '{categoria}': {e}")
            return []

    def _formatear_contenido_para_vectorstore(self, item: dict) -> str:
        """Formatea el contenido de la base de datos para el vectorstore"""
        # Combinar título y contenido para mejor búsqueda semántica
        contenido_formateado = f"TÍTULO: {item['titulo']}\n\n"
        contenido_formateado += f"CATEGORÍA: {item['categoria']}\n\n"
        contenido_formateado += f"CONTENIDO: {item['contenido']}"

        # Añadir precio si existe
        if item.get('precio'):
            contenido_formateado += f"\n\nPRECIO: ${item['precio']}"

        # Añadir metadatos relevantes
        metadatos = item.get('metadatos', {})
        if metadatos:
            for key, value in metadatos.items():
                if value and key not in ['tipo']:  # Evitar metadatos internos
                    contenido_formateado += f"\n{key.upper()}: {value}"

        return contenido_formateado

    def search_in_database(self, termino: str) -> List[dict]:
        """Busca directamente en la base de datos"""
        try:
            resultados = self.repository.buscar_contenido(termino)
            logger.info(
                f"🔍 Búsqueda en BD para '{termino}': {len(resultados)} resultados")
            return resultados

        except Exception as e:
            logger.error(f"❌ Error en búsqueda de base de datos: {e}")
            return []

    def get_content_summary(self) -> dict:
        """Obtiene resumen del contenido disponible"""
        try:
            estadisticas = self.repository.obtener_estadisticas()
            return estadisticas

        except Exception as e:
            logger.error(f"❌ Error al obtener resumen de contenido: {e}")
            return {}


# Instancia global del adaptador
db_vectorstore_adapter = DatabaseVectorStoreAdapter()
