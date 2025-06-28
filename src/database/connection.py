"""
Gestión de conexión a la base de datos SQLite
"""
import sqlite3
import threading
from pathlib import Path

from utils.logger import logger


class DatabaseConnection:
    """Gestión de conexión a la base de datos SQLite"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return

        self.db_path = Path("src/data/hotel_content.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = None
        self.initialized = True
        self._init_database()

    def get_connection(self) -> sqlite3.Connection:
        """Obtiene la conexión a la base de datos"""
        if self._connection is None:
            try:
                self._connection = sqlite3.connect(
                    str(self.db_path),
                    check_same_thread=False,
                    timeout=30.0
                )
                self._connection.row_factory = sqlite3.Row
                # Habilitar foreign keys
                self._connection.execute("PRAGMA foreign_keys = ON")
                logger.info("✅ Conexión a base de datos establecida")
            except Exception as e:
                logger.error(f"❌ Error al conectar a la base de datos: {e}")
                raise

        return self._connection

    def close_connection(self):
        """Cierra la conexión a la base de datos"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("🔒 Conexión a base de datos cerrada")

    def _init_database(self):
        """Inicializa la estructura de la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Tabla principal de contenido del hotel
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contenido_hotel (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categoria TEXT NOT NULL CHECK (categoria IN (
                        'habitaciones', 'restaurantes', 'amenidades', 
                        'politicas', 'informacion', 'contacto'
                    )),
                    titulo TEXT NOT NULL,
                    contenido TEXT NOT NULL,
                    precio DECIMAL(10,2) DEFAULT NULL,
                    metadatos TEXT DEFAULT NULL,
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabla para habitaciones con detalles específicos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habitaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contenido_id INTEGER NOT NULL,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    precio_noche DECIMAL(10,2) NOT NULL,
                    capacidad_personas INTEGER DEFAULT 2,
                    tipo_cama TEXT,
                    servicios TEXT,
                    disponible BOOLEAN DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contenido_id) REFERENCES contenido_hotel(id) ON DELETE CASCADE
                )
            ''')

            # Tabla para restaurantes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS restaurantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contenido_id INTEGER NOT NULL,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    tipo_cocina TEXT,
                    horario_apertura TEXT,
                    horario_cierre TEXT,
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contenido_id) REFERENCES contenido_hotel(id) ON DELETE CASCADE
                )
            ''')

            # Tabla para amenidades/servicios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS amenidades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contenido_id INTEGER NOT NULL,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    categoria_amenidad TEXT,
                    horario TEXT,
                    costo DECIMAL(10,2) DEFAULT NULL,
                    disponible BOOLEAN DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contenido_id) REFERENCES contenido_hotel(id) ON DELETE CASCADE
                )
            ''')

            # Tabla para versiones de contenido
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS versiones_contenido (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contenido_id INTEGER NOT NULL,
                    version INTEGER NOT NULL,
                    contenido_anterior TEXT,
                    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    motivo_cambio TEXT,
                    FOREIGN KEY (contenido_id) REFERENCES contenido_hotel(id) ON DELETE CASCADE
                )
            ''')

            # Índices para optimización
            cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_contenido_categoria ON contenido_hotel(categoria)')
            cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_contenido_activo ON contenido_hotel(activo)')
            cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_habitaciones_precio ON habitaciones(precio_noche)')
            cursor.execute(
                'CREATE INDEX IF NOT EXISTS idx_habitaciones_disponible ON habitaciones(disponible)')

            conn.commit()
            logger.info(
                "✅ Estructura de base de datos inicializada correctamente")

        except Exception as e:
            logger.error(f"❌ Error al inicializar la base de datos: {e}")
            raise


# Instancia global de la conexión
db_connection = DatabaseConnection()
