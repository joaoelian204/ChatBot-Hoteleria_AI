"""
Repositorio para gestión de contenido del hotel
"""
import json
from typing import Dict, List, Optional

from database.connection import db_connection
from utils.logger import logger


class ContenidoHotelRepository:
    """Repositorio para operaciones CRUD del contenido del hotel"""

    def __init__(self):
        self.conn = db_connection.get_connection()

    def obtener_todo_contenido(self) -> List[Dict]:
        """Obtiene todo el contenido activo del hotel"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, categoria, titulo, contenido, precio, metadatos, 
                       fecha_creacion, fecha_actualizacion
                FROM contenido_hotel 
                WHERE activo = 1 
                ORDER BY categoria, titulo
            ''')

            contenido = []
            for row in cursor.fetchall():
                item = {
                    'id': row['id'],
                    'categoria': row['categoria'],
                    'titulo': row['titulo'],
                    'contenido': row['contenido'],
                    'precio': row['precio'],
                    'metadatos': json.loads(row['metadatos']) if row['metadatos'] else {},
                    'fecha_creacion': row['fecha_creacion'],
                    'fecha_actualizacion': row['fecha_actualizacion']
                }
                contenido.append(item)

            logger.info(f"✅ Obtenidos {len(contenido)} elementos de contenido")
            return contenido

        except Exception as e:
            logger.error(f"❌ Error al obtener contenido: {e}")
            return []

    def obtener_por_categoria(self, categoria: str) -> List[Dict]:
        """Obtiene contenido por categoría específica"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, categoria, titulo, contenido, precio, metadatos,
                       fecha_creacion, fecha_actualizacion
                FROM contenido_hotel 
                WHERE categoria = ? AND activo = 1 
                ORDER BY titulo
            ''', (categoria,))

            contenido = []
            for row in cursor.fetchall():
                item = {
                    'id': row['id'],
                    'categoria': row['categoria'],
                    'titulo': row['titulo'],
                    'contenido': row['contenido'],
                    'precio': row['precio'],
                    'metadatos': json.loads(row['metadatos']) if row['metadatos'] else {},
                    'fecha_creacion': row['fecha_creacion'],
                    'fecha_actualizacion': row['fecha_actualizacion']
                }
                contenido.append(item)

            logger.info(
                f"✅ Obtenidos {len(contenido)} elementos para categoría '{categoria}'")
            return contenido

        except Exception as e:
            logger.error(
                f"❌ Error al obtener contenido por categoría '{categoria}': {e}")
            return []

    def buscar_contenido(self, termino: str) -> List[Dict]:
        """Busca contenido por término en título y contenido"""
        try:
            cursor = self.conn.cursor()
            termino = f"%{termino}%"
            cursor.execute('''
                SELECT id, categoria, titulo, contenido, precio, metadatos,
                       fecha_creacion, fecha_actualizacion
                FROM contenido_hotel 
                WHERE (titulo LIKE ? OR contenido LIKE ?) AND activo = 1
                ORDER BY categoria, titulo
            ''', (termino, termino))

            contenido = []
            for row in cursor.fetchall():
                item = {
                    'id': row['id'],
                    'categoria': row['categoria'],
                    'titulo': row['titulo'],
                    'contenido': row['contenido'],
                    'precio': row['precio'],
                    'metadatos': json.loads(row['metadatos']) if row['metadatos'] else {},
                    'fecha_creacion': row['fecha_creacion'],
                    'fecha_actualizacion': row['fecha_actualizacion']
                }
                contenido.append(item)

            logger.info(
                f"✅ Búsqueda '{termino}' encontró {len(contenido)} resultados")
            return contenido

        except Exception as e:
            logger.error(f"❌ Error en búsqueda de contenido: {e}")
            return []

    def agregar_contenido(self, categoria: str, titulo: str, contenido: str,
                          precio: float = None, metadatos: Dict = None) -> int:
        """Agrega nuevo contenido al hotel"""
        try:
            cursor = self.conn.cursor()
            metadatos_json = json.dumps(metadatos) if metadatos else None

            cursor.execute('''
                INSERT INTO contenido_hotel 
                (categoria, titulo, contenido, precio, metadatos) 
                VALUES (?, ?, ?, ?, ?)
            ''', (categoria, titulo, contenido, precio, metadatos_json))

            contenido_id = cursor.lastrowid
            self.conn.commit()

            logger.info(
                f"✅ Contenido agregado con ID {contenido_id}: '{titulo}'")
            return contenido_id

        except Exception as e:
            logger.error(f"❌ Error al agregar contenido: {e}")
            return 0

    def actualizar_contenido(self, contenido_id: int, titulo: str = None,
                             contenido: str = None, precio: float = None,
                             metadatos: Dict = None) -> bool:
        """Actualiza contenido existente"""
        try:
            # Obtener contenido actual para versionado
            contenido_actual = self.obtener_por_id(contenido_id)
            if not contenido_actual:
                logger.warning(
                    f"⚠️ No se encontró contenido con ID {contenido_id}")
                return False

            # Crear versión del contenido anterior
            self._crear_version(contenido_id, contenido_actual['contenido'])

            # Preparar campos de actualización
            campos_actualizar = []
            valores = []

            if titulo is not None:
                campos_actualizar.append("titulo = ?")
                valores.append(titulo)

            if contenido is not None:
                campos_actualizar.append("contenido = ?")
                valores.append(contenido)

            if precio is not None:
                campos_actualizar.append("precio = ?")
                valores.append(precio)

            if metadatos is not None:
                campos_actualizar.append("metadatos = ?")
                valores.append(json.dumps(metadatos))

            # Siempre actualizar fecha de modificación
            campos_actualizar.append("fecha_actualizacion = CURRENT_TIMESTAMP")
            valores.append(contenido_id)

            # Si no hay campos para actualizar (excepto fecha)
            if not campos_actualizar[:-1]:
                logger.warning("⚠️ No se especificaron campos para actualizar")
                return False

            # Ejecutar actualización
            cursor = self.conn.cursor()
            query = f'''
                UPDATE contenido_hotel 
                SET {', '.join(campos_actualizar)}
                WHERE id = ?
            '''
            cursor.execute(query, valores)
            self.conn.commit()

            logger.info(f"✅ Contenido actualizado: ID {contenido_id}")
            return True

        except Exception as e:
            logger.error(
                f"❌ Error al actualizar contenido ID {contenido_id}: {e}")
            return False

    def eliminar_contenido(self, contenido_id: int) -> bool:
        """Elimina contenido (marca como inactivo)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE contenido_hotel 
                SET activo = 0, fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (contenido_id,))

            if cursor.rowcount > 0:
                self.conn.commit()
                logger.info(
                    f"✅ Contenido marcado como inactivo: ID {contenido_id}")
                return True
            else:
                logger.warning(
                    f"⚠️ No se encontró contenido con ID {contenido_id}")
                return False

        except Exception as e:
            logger.error(
                f"❌ Error al eliminar contenido ID {contenido_id}: {e}")
            return False

    def obtener_por_id(self, contenido_id: int) -> Optional[Dict]:
        """Obtiene contenido por ID específico"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, categoria, titulo, contenido, precio, metadatos,
                       fecha_creacion, fecha_actualizacion
                FROM contenido_hotel 
                WHERE id = ? AND activo = 1
            ''', (contenido_id,))

            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'categoria': row['categoria'],
                    'titulo': row['titulo'],
                    'contenido': row['contenido'],
                    'precio': row['precio'],
                    'metadatos': json.loads(row['metadatos']) if row['metadatos'] else {},
                    'fecha_creacion': row['fecha_creacion'],
                    'fecha_actualizacion': row['fecha_actualizacion']
                }
            return None

        except Exception as e:
            logger.error(
                f"❌ Error al obtener contenido por ID {contenido_id}: {e}")
            return None

    def _crear_version(self, contenido_id: int, contenido_anterior: str, motivo: str = None):
        """Crea una versión del contenido anterior"""
        try:
            cursor = self.conn.cursor()

            # Obtener número de versión siguiente
            cursor.execute('''
                SELECT COALESCE(MAX(version), 0) + 1 
                FROM versiones_contenido 
                WHERE contenido_id = ?
            ''', (contenido_id,))

            version = cursor.fetchone()[0]

            # Insertar versión
            cursor.execute('''
                INSERT INTO versiones_contenido 
                (contenido_id, version, contenido_anterior, motivo_cambio)
                VALUES (?, ?, ?, ?)
            ''', (contenido_id, version, contenido_anterior, motivo))

            logger.debug(
                f"📚 Versión {version} creada para contenido ID {contenido_id}")

        except Exception as e:
            logger.error(f"❌ Error al crear versión: {e}")

    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas del contenido"""
        try:
            cursor = self.conn.cursor()

            # Contar por categoría
            cursor.execute('''
                SELECT categoria, COUNT(*) as total
                FROM contenido_hotel 
                WHERE activo = 1
                GROUP BY categoria
            ''')
            por_categoria = dict(cursor.fetchall())

            # Total general
            cursor.execute(
                'SELECT COUNT(*) FROM contenido_hotel WHERE activo = 1')
            total = cursor.fetchone()[0]

            # Última actualización
            cursor.execute('''
                SELECT MAX(fecha_actualizacion) 
                FROM contenido_hotel 
                WHERE activo = 1
            ''')
            ultima_actualizacion = cursor.fetchone()[0]

            estadisticas = {
                'total_contenido': total,
                'por_categoria': por_categoria,
                'ultima_actualizacion': ultima_actualizacion,
                'categorias_disponibles': list(por_categoria.keys())
            }

            logger.info("✅ Estadísticas de contenido obtenidas")
            return estadisticas

        except Exception as e:
            logger.error(f"❌ Error al obtener estadísticas: {e}")
            return {}


# Instancia global del repositorio
contenido_repository = ContenidoHotelRepository()
