"""
Gestión de analytics y métricas del bot
"""
import json
import sqlite3
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from utils.logger import logger


class AnalyticsManager:
    """Gestión de analytics y métricas del bot"""

    def __init__(self):
        self.db_path = "src/data/analytics.db"
        self.events = []
        self.metrics = defaultdict(int)
        self.session_data = {}
        self._init_database()

    def _init_database(self):
        """Inicializa la base de datos de analytics"""
        try:
            # Crear directorio data si no existe
            db_path = Path(self.db_path)
            db_path.parent.mkdir(parents=True, exist_ok=True)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    user_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    data TEXT,
                    session_id TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value INTEGER DEFAULT 0,
                    date DATE DEFAULT CURRENT_DATE,
                    UNIQUE(metric_name, date)
                )
            ''')
            conn.commit()
            conn.close()
            logger.info("Base de datos de analytics inicializada")
        except Exception as e:
            logger.error(f"Error al inicializar base de datos de analytics: {e}")

    def track_event(self, event_type: str, data: Dict[str, Any] = None, user_id: int = None):
        """Registra un evento"""
        try:
            event = {
                'event_type': event_type,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'data': json.dumps(data) if data else None,
                'session_id': self._get_session_id(user_id)
            }
            self.events.append(event)
            self._save_event_to_db(event)
            self._update_metrics(event_type)
            logger.debug(f"Evento registrado: {event_type}")
        except Exception as e:
            logger.error(f"Error al registrar evento: {e}")

    def _get_session_id(self, user_id: int) -> str:
        """Genera o recupera el ID de sesión del usuario"""
        if user_id not in self.session_data:
            self.session_data[user_id] = f"session_{user_id}_{int(time.time())}"
        return self.session_data[user_id]

    def _save_event_to_db(self, event: Dict[str, Any]):
        """Guarda el evento en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (event_type, user_id, timestamp, data, session_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                event['event_type'],
                event['user_id'],
                event['timestamp'],
                event['data'],
                event['session_id']
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error al guardar evento en DB: {e}")

    def _update_metrics(self, event_type: str):
        """Actualiza las métricas basadas en el tipo de evento"""
        today = datetime.now().date().isoformat()
        metric_key = f"{event_type}_{today}"
        self.metrics[metric_key] += 1
        self._save_metric_to_db(event_type, self.metrics[metric_key], today)

    def _save_metric_to_db(self, metric_name: str, value: int, date: str):
        """Guarda la métrica en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO metrics (metric_name, metric_value, date)
                VALUES (?, ?, ?)
            ''', (metric_name, value, date))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error al guardar métrica en DB: {e}")

    def get_metrics(self, days: int = 7) -> Dict[str, Any]:
        """Obtiene métricas de los últimos días"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            cursor.execute('''
                SELECT metric_name, SUM(metric_value) as total
                FROM metrics
                WHERE date >= ?
                GROUP BY metric_name
                ORDER BY total DESC
            ''', (start_date,))
            results = cursor.fetchall()
            conn.close()
            return {row[0]: row[1] for row in results}
        except Exception as e:
            logger.error(f"Error al obtener métricas: {e}")
            return {}

    def get_user_activity(self, user_id: int, days: int = 7) -> List[Dict[str, Any]]:
        """Obtiene la actividad de un usuario específico"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            cursor.execute('''
                SELECT event_type, timestamp, data
                FROM events
                WHERE user_id = ? AND timestamp >= ?
                ORDER BY timestamp DESC
            ''', (user_id, start_date))
            results = cursor.fetchall()
            conn.close()
            return [
                {
                    'event_type': row[0],
                    'timestamp': row[1],
                    'data': json.loads(row[2]) if row[2] else None
                }
                for row in results
            ]
        except Exception as e:
            logger.error(f"Error al obtener actividad del usuario: {e}")
            return []

    def get_popular_events(self, days: int = 7, limit: int = 10) -> List[tuple]:
        """Obtiene los eventos más populares"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).isoformat()
            cursor.execute('''
                SELECT event_type, COUNT(*) as count
                FROM events
                WHERE timestamp >= ?
                GROUP BY event_type
                ORDER BY count DESC
                LIMIT ?
            ''', (start_date, limit))
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            logger.error(f"Error al obtener eventos populares: {e}")
            return []

    def get_daily_stats(self, days: int = 7) -> Dict[str, List[int]]:
        """Obtiene estadísticas diarias"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            start_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            cursor.execute('''
                SELECT date, COUNT(*) as count
                FROM events
                WHERE date >= ?
                GROUP BY date
                ORDER BY date
            ''', (start_date,))
            results = cursor.fetchall()
            conn.close()
            dates = []
            counts = []
            for row in results:
                dates.append(row[0])
                counts.append(row[1])
            return {'dates': dates, 'counts': counts}
        except Exception as e:
            logger.error(f"Error al obtener estadísticas diarias: {e}")
            return {'dates': [], 'counts': []}

    def cleanup_old_data(self, days: int = 30):
        """Limpia datos antiguos de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            cursor.execute('DELETE FROM events WHERE timestamp < ?', (cutoff_date,))
            cursor.execute('DELETE FROM metrics WHERE date < ?', (cutoff_date,))
            conn.commit()
            conn.close()
            logger.info(f"Datos de más de {days} días eliminados")
        except Exception as e:
            logger.error(f"Error al limpiar datos antiguos: {e}")


analytics_manager = AnalyticsManager()
