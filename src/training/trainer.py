"""
Entrenamiento de modelos para hotelería
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from ai.vectorstore import vectorstore_manager
from config.settings import settings
from utils.logger import logger
from utils.text_processor import normalize_text


class HoteleriaTrainer:
    """Entrenador para modelos de hotelería"""

    def __init__(self):
        # Obtener el directorio raíz del proyecto (desde src/ subir dos niveles)
        project_root = Path(__file__).parent.parent.parent
        self.training_data_path = project_root / "documentos"
        self.model_output_path = project_root / "data" / "models"
        self.training_log = []
        self.performance_metrics = {}
        self._ensure_directories()

    def _ensure_directories(self):
        """Asegura que existan los directorios necesarios"""
        self.training_data_path.mkdir(parents=True, exist_ok=True)
        self.model_output_path.mkdir(parents=True, exist_ok=True)

    def load_training_data(self) -> List[Dict[str, Any]]:
        """Carga datos de entrenamiento desde archivos"""
        training_data = []
        try:
            for file_path in self.training_data_path.glob("*.txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    training_data.append({
                        'file': file_path.name,
                        'content': content,
                        'type': self._classify_content(content)
                    })
            logger.info(f"Cargados {len(training_data)} archivos de entrenamiento")
            return training_data
        except Exception as e:
            logger.error(f"Error al cargar datos de entrenamiento: {e}")
            return []

    def _classify_content(self, content: str) -> str:
        """Clasifica el contenido del documento"""
        content_lower = content.lower()
        if any(word in content_lower for word in ['habitacion', 'suite', 'cama', 'dormitorio']):
            return 'rooms'
        elif any(word in content_lower for word in ['restaurante', 'menu', 'comida', 'gastronomia']):
            return 'restaurants'
        elif any(word in content_lower for word in ['piscina', 'gimnasio', 'spa', 'amenidad']):
            return 'amenities'
        elif any(word in content_lower for word in ['precio', 'tarifa', 'costo', 'valor']):
            return 'pricing'
        elif any(word in content_lower for word in ['contacto', 'telefono', 'email', 'reserva']):
            return 'contact'
        else:
            return 'general'

    def preprocess_data(self, training_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Preprocesa los datos de entrenamiento"""
        processed_data = []
        for item in training_data:
            try:
                processed_content = normalize_text(item['content'])
                processed_data.append({
                    'file': item['file'],
                    'original_content': item['content'],
                    'processed_content': processed_content,
                    'type': item['type'],
                    'word_count': len(processed_content.split()),
                    'processed_at': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Error procesando {item['file']}: {e}")
        logger.info(f"Procesados {len(processed_data)} documentos")
        return processed_data

    def train_vectorstore(self, processed_data: List[Dict[str, Any]]) -> bool:
        """Entrena el vectorstore con los datos procesados"""
        try:
            logger.info("🤖 Iniciando entrenamiento del vectorstore...")
            logger.info("⏳ Cargando modelos de IA (esto puede tomar varios minutos la primera vez)...")
            
            # Forzar actualización de conocimiento
            vectorstore_manager.update_knowledge()
            
            # Forzar creación del vectorstore con modelos cargados
            logger.info("🧠 Forzando carga de modelos de embeddings...")
            vectorstore_manager._create_vectorstore()
            
            if vectorstore_manager.vectorstore is not None:
                logger.info("✅ Vectorstore con IA creado exitosamente")
                return True
            else:
                logger.warning("⚠️ Vectorstore creado en modo lazy, se activará en la primera búsqueda")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error entrenando vectorstore: {e}")
            return False

    def validate_training(self, test_queries: List[str]) -> Dict[str, Any]:
        """Valida el entrenamiento con consultas de prueba"""
        logger.info("🔍 Validando entrenamiento...")
        
        # Forzar la inicialización del vectorstore
        try:
            from ai.models import ai_models
            
            # Intentar realizar una búsqueda simple para inicializar el vectorstore
            logger.info("🔍 Probando búsqueda con IA...")
            
            # Usar el método correcto según el modo de carga
            if ai_models.use_lazy_loading:
                logger.warning("⚠️ Modo lazy loading - validación completa requiere modo async")
                # Para validación básica en lazy mode, simplemente confirmar que está listo
                logger.info("✅ Vectorstore preparado para lazy loading")
                test_result = True  # Asumir que está listo para lazy loading
            else:
                test_result = vectorstore_manager.search_context("habitaciones", k=1)
                
            if test_result:
                logger.info("✅ Vectorstore con IA funcionando correctamente")
            else:
                logger.warning("⚠️ Vectorstore inicializado pero sin resultados de prueba")
        except Exception as e:
            logger.warning(f"⚠️ No se pudo inicializar vectorstore para validación: {e}")
            # Retornar resultados por defecto si no se puede validar
            return {
                'total_queries': len(test_queries),
                'successful_queries': 0,
                'failed_queries': len(test_queries),
                'average_response_time': 0,
                'query_results': [],
                'validation_note': 'Validación omitida - vectorstore no disponible'
            }
        
        results = {
            'total_queries': len(test_queries),
            'successful_queries': 0,
            'failed_queries': 0,
            'average_response_time': 0,
            'query_results': []
        }
        total_time = 0
        
        for query in test_queries:
            try:
                start_time = datetime.now()
                
                # Usar el método correcto según el modo de carga
                if ai_models.use_lazy_loading:
                    logger.warning(f"⚠️ Consulta sin resultados: '{query}' (lazy loading - usar async para prueba real)")
                    context_docs = []  # En lazy mode sin async, no podemos hacer búsquedas reales
                else:
                    context_docs = vectorstore_manager.search_context(query, k=3)
                    
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                total_time += response_time
                if context_docs:
                    results['successful_queries'] += 1
                    results['query_results'].append({
                        'query': query,
                        'context_found': True,
                        'context_count': len(context_docs),
                        'response_time': response_time
                    })
                    logger.info(f"✅ Consulta exitosa: '{query}' - {len(context_docs)} documentos encontrados")
                else:
                    results['failed_queries'] += 1
                    results['query_results'].append({
                        'query': query,
                        'context_found': False,
                        'context_count': 0,
                        'response_time': response_time
                    })
                    logger.warning(f"⚠️ Consulta sin resultados: '{query}'")
            except Exception as e:
                logger.error(f"❌ Error validando consulta '{query}': {e}")
                results['failed_queries'] += 1
                results['query_results'].append({
                    'query': query,
                    'context_found': False,
                    'context_count': 0,
                    'response_time': 0,
                    'error': str(e)
                })
        
        if results['total_queries'] > 0:
            results['average_response_time'] = total_time / results['total_queries']
        
        logger.info(f"🎯 Validación completada: {results['successful_queries']}/{results['total_queries']} consultas exitosas")
        return results

    def save_training_log(self, training_data: List[Dict[str, Any]], validation_results: Dict[str, Any]):
        """Guarda el log de entrenamiento"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'training_data_count': len(training_data),
                'validation_results': validation_results,
                'model_version': settings.MODEL_VERSION,
                'vectorstore_stats': vectorstore_manager.get_stats()
            }
            self.training_log.append(log_entry)
            log_file = os.path.join(self.model_output_path, 'training_log.json')
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(self.training_log, f, indent=2, ensure_ascii=False)
            logger.info(f"Log de entrenamiento guardado en {log_file}")
        except Exception as e:
            logger.error(f"Error guardando log de entrenamiento: {e}")

    def get_training_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del entrenamiento"""
        return {
            'total_training_sessions': len(self.training_log),
            'last_training': self.training_log[-1] if self.training_log else None,
            'vectorstore_stats': vectorstore_manager.get_stats(),
            'performance_metrics': self.performance_metrics
        }

    def run_full_training(self) -> bool:
        """Ejecuta el entrenamiento completo"""
        try:
            logger.info("🚀 Iniciando entrenamiento completo...")
            
            # Cargar datos de entrenamiento
            logger.info("📁 Cargando datos de entrenamiento...")
            training_data = self.load_training_data()
            if not training_data:
                logger.error("❌ No se encontraron datos de entrenamiento")
                return False
            
            # Preprocesar datos
            logger.info("🔄 Preprocesando datos...")
            processed_data = self.preprocess_data(training_data)
            if not processed_data:
                logger.error("❌ Error en el preprocesamiento de datos")
                return False
            
            # Entrenar vectorstore
            logger.info("🤖 Entrenando vectorstore...")
            training_success = self.train_vectorstore(processed_data)
            if not training_success:
                logger.error("❌ Error en el entrenamiento del vectorstore")
                return False
            
            # Dar tiempo para que el vectorstore se inicialice completamente
            import time
            logger.info("⏳ Esperando inicialización del vectorstore...")
            time.sleep(2)
            
            # Validar entrenamiento
            logger.info("✅ Validando entrenamiento...")
            test_queries = [
                "¿Qué habitaciones tienen disponibles?",
                "¿Cuál es el precio de la suite?",
                "¿Qué restaurantes tienen?",
                "¿Hay piscina?",
                "¿Cómo los contacto?"
            ]
            validation_results = self.validate_training(test_queries)
            
            # Guardar log de entrenamiento
            self.save_training_log(processed_data, validation_results)
            
            success_rate = (validation_results['successful_queries'] / validation_results['total_queries']) * 100
            logger.info(f"🎉 Entrenamiento completado. Tasa de éxito: {success_rate:.1f}%")
            
            return success_rate > 70
            
        except Exception as e:
            logger.error(f"❌ Error en entrenamiento completo: {e}")
            return False

    def incremental_training(self, new_documents: List[Dict[str, Any]]) -> bool:
        """Entrenamiento incremental con nuevos documentos"""
        try:
            logger.info(f"Iniciando entrenamiento incremental con {len(new_documents)} documentos...")
            processed_docs = self.preprocess_data(new_documents)
            success = self.train_vectorstore(processed_docs)
            if success:
                logger.info("Entrenamiento incremental completado")
            return success
        except Exception as e:
            logger.error(f"Error en entrenamiento incremental: {e}")
            return False

    def export_training_data(self, output_file: str) -> bool:
        """Exporta los datos de entrenamiento"""
        try:
            training_data = self.load_training_data()
            processed_data = self.preprocess_data(training_data)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Datos de entrenamiento exportados a {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error exportando datos de entrenamiento: {e}")
            return False

    def cleanup_old_models(self, keep_last: int = 3):
        """Limpia modelos antiguos, manteniendo solo los últimos"""
        try:
            model_files = list(Path(self.model_output_path).glob("*.pkl"))
            if len(model_files) > keep_last:
                model_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                for old_file in model_files[keep_last:]:
                    old_file.unlink()
                    logger.info(f"Modelo antiguo eliminado: {old_file}")
        except Exception as e:
            logger.error(f"Error limpiando modelos antiguos: {e}")


hoteleria_trainer = HoteleriaTrainer()
