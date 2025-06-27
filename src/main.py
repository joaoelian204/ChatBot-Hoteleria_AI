#!/usr/bin/env python3
"""
🏨 ChatBot de Hotelería - Script Principal
==========================================

Script principal modularizado para ejecutar el ChatBot de Hotelería con IA.
Proporciona múltiples modos de operación y gestión completa del sistema.

Autor: Sistema de IA para Hotelería
Versión: 2.0.0
"""

import argparse
import asyncio
import importlib.util
import os
import sys
from pathlib import Path
from typing import Any, Dict

# Configurar path para importaciones
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from utils.logger import logger


class SystemValidator:
    """Validador del sistema y dependencias"""
    
    @staticmethod
    def validate_configuration() -> bool:
        """Verifica que la configuración esté correcta"""
        try:
            settings.validate()
            logger.info("✅ Configuración verificada correctamente")
            return True
        except ValueError as e:
            logger.error(f"❌ Error en configuración: {e}")
            return False
    
    @staticmethod
    def validate_dependencies() -> bool:
        """Verifica que las dependencias estén instaladas"""
        required_packages = {
            'faiss': 'FAISS para búsqueda vectorial',
            'langchain': 'LangChain para procesamiento de IA',
            'telegram': 'python-telegram-bot para el bot',
            'torch': 'PyTorch para modelos de IA',
            'transformers': 'Transformers para modelos de Hugging Face'
        }
        
        missing_packages = []
        
        for package, description in required_packages.items():
            if importlib.util.find_spec(package) is None:
                missing_packages.append(f"{package} ({description})")
        
        if missing_packages:
            logger.error("❌ Dependencias faltantes:")
            for package in missing_packages:
                logger.error(f"   - {package}")
            logger.info("📦 Instala las dependencias con: pip install -r requirements.txt")
            return False
        
        logger.info("✅ Todas las dependencias están instaladas")
        return True
    
    @staticmethod
    def validate_documents() -> bool:
        """Verifica que existan documentos de conocimiento"""
        if not settings.DOCUMENTOS_DIR.exists():
            logger.warning("⚠️ Directorio de documentos no existe")
            logger.info("📄 Ejecuta primero: python src/main.py --mode train")
            return False
        
        documents = list(settings.DOCUMENTOS_DIR.glob("*.txt"))
        if not documents:
            logger.warning("⚠️ No se encontraron documentos en la carpeta 'documentos'")
            logger.info("📄 Ejecuta primero: python src/main.py --mode train")
            return False
        
        logger.info(f"✅ Encontrados {len(documents)} documentos de conocimiento")
        for doc in documents:
            logger.info(f"   - {doc.name}")
        
        return True


class SystemMonitor:
    """Monitor del sistema y recursos"""
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Obtiene información detallada del uso de memoria"""
        try:
            import psutil
            
            # Proceso actual
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            # Memoria del sistema
            system_memory = psutil.virtual_memory()
            
            return {
                'process_rss': memory_info.rss / 1024 / 1024,  # MB
                'process_vms': memory_info.vms / 1024 / 1024,  # MB
                'system_total': system_memory.total / 1024 / 1024 / 1024,  # GB
                'system_available': system_memory.available / 1024 / 1024,  # MB
                'system_percent': system_memory.percent
            }
        except ImportError:
            logger.warning("⚠️ psutil no está instalado. Instala con: pip install psutil")
            return {}
        except Exception as e:
            logger.error(f"❌ Error obteniendo información de memoria: {e}")
            return {}
    
    @staticmethod
    def display_memory_usage():
        """Muestra el uso actual de memoria del sistema"""
        memory_info = SystemMonitor.get_memory_usage()
        
        if not memory_info:
            return False
        
        logger.info("💾 Uso de memoria actual:")
        logger.info(f"   RAM del proceso: {memory_info['process_rss']:.1f} MB")
        logger.info(f"   Memoria virtual: {memory_info['process_vms']:.1f} MB")
        logger.info(f"   RAM total del sistema: {memory_info['system_total']:.1f} GB")
        logger.info(f"   RAM disponible: {memory_info['system_available']:.1f} MB")
        logger.info(f"   Uso del sistema: {memory_info['system_percent']:.1f}%")
        
        return True


class AITester:
    """Tester para modelos de IA"""
    
    @staticmethod
    async def test_ai_models_async() -> bool:
        """Prueba que los modelos de IA se carguen correctamente (versión asíncrona)"""
        logger.info("🧪 Probando carga de modelos de IA (async)...")
        
        try:
            from ai.vectorstore import vectorstore_manager
            
            logger.info("🔄 Forzando carga de vectorstore...")
            
            # Realizar búsquedas de prueba para cargar todos los modelos
            test_queries = [
                "¿Qué habitaciones tienen disponibles?",
                "¿Cuál es el precio?", 
                "¿Hay restaurante?",
                "¿Cómo contactar?"
            ]
            
            success_count = 0
            for query in test_queries:
                logger.info(f"🔍 Probando: {query}")
                
                try:
                    results = await vectorstore_manager.search_context_async(query, k=2)
                    
                    if results:
                        logger.info(f"   ✅ {len(results)} resultados encontrados")
                        success_count += 1
                    else:
                        logger.warning(f"   ⚠️ Sin resultados para: {query}")
                        
                except Exception as e:
                    logger.error(f"   ❌ Error en query '{query}': {e}")
            
            success_rate = (success_count / len(test_queries)) * 100
            logger.info(f"📊 Tasa de éxito: {success_rate:.1f}% ({success_count}/{len(test_queries)})")
            
            return success_rate >= 50  # Al menos 50% de éxito
            
        except Exception as e:
            logger.error(f"❌ Error probando IA (async): {e}")
            return False
    
    @staticmethod
    def test_ai_models_sync() -> bool:
        """Prueba que los modelos de IA se carguen correctamente (versión síncrona)"""
        logger.info("🧪 Probando carga de modelos de IA (sync)...")
        
        try:
            from ai.models import ai_models
            from ai.vectorstore import vectorstore_manager
            
            if ai_models.use_lazy_loading:
                logger.warning("⚠️ Modo lazy loading activado - usa test_ai_models_async()")
                return False
            
            logger.info("🔄 Forzando carga de vectorstore...")
            
            results = vectorstore_manager.search_context("¿Qué habitaciones tienen?", k=2)
            
            if results:
                logger.info(f"✅ IA funcionando - Encontrados {len(results)} resultados")
                for i, result in enumerate(results, 1):
                    logger.info(f"   {i}. {result[:100]}...")
                return True
            else:
                logger.warning("⚠️ IA no está respondiendo adecuadamente")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error probando IA: {e}")
            return False


class ChatbotManager:
    """Gestor principal del chatbot"""
    
    def __init__(self):
        self.validator = SystemValidator()
        self.monitor = SystemMonitor()
        self.ai_tester = AITester()
    
    def run_bot(self) -> bool:
        """Ejecuta el bot principal"""
        logger.info("🤖 Iniciando ChatBot de Hotelería...")
        
        # Validaciones previas
        if not self.validator.validate_configuration():
            return False
        
        if not self.validator.validate_dependencies():
            return False
        
        if not self.validator.validate_documents():
            logger.info("💡 Continuando sin documentos...")
        
        try:
            from bot.bot_main import HoteleriaBot
            bot = HoteleriaBot()
            logger.info("✅ Bot inicializado correctamente")
            logger.info("🚀 Ejecutando bot... (Ctrl+C para detener)")
            bot.run()
            return True
            
        except KeyboardInterrupt:
            logger.info("⏹️ Bot detenido por el usuario")
            return True
        except Exception as e:
            logger.error(f"❌ Error al ejecutar el bot: {e}")
            return False
    
    def run_training(self) -> bool:
        """Ejecuta el entrenamiento del sistema"""
        logger.info("📚 Iniciando entrenamiento...")
        
        try:
            from training.trainer import HoteleriaTrainer
            trainer = HoteleriaTrainer()
            success = trainer.run_full_training()
            
            if success:
                logger.info("✅ Entrenamiento completado exitosamente")
            else:
                logger.error("❌ Error durante el entrenamiento")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error en entrenamiento: {e}")
            return False
    
    def run_analytics(self) -> bool:
        """Ejecuta las analíticas del sistema"""
        logger.info("📊 Mostrando analíticas...")
        
        try:
            from analytics.manager import analytics_manager
            
            # Estadísticas básicas
            daily_stats = analytics_manager.get_daily_stats(7)
            logger.info("\n📈 Últimos 7 días:")
            logger.info(f"   Preguntas totales: {daily_stats['total_questions']}")
            logger.info(f"   Tiempo promedio: {daily_stats['avg_response_time']:.2f}s")
            
            # Preguntas populares
            popular = analytics_manager.get_popular_questions(5)
            if popular:
                logger.info("\n🔥 Preguntas más populares:")
                for i, q in enumerate(popular, 1):
                    logger.info(f"   {i}. {q['question'][:50]}... ({q['count']} veces)")
            
            # Rendimiento del cache
            cache_stats = analytics_manager.get_cache_performance()
            logger.info("\n⚡ Cache:")
            logger.info(f"   Hit rate: {cache_stats['hit_rate']:.1f}%")
            logger.info(f"   Hits: {cache_stats['hits']}, Misses: {cache_stats['misses']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en analíticas: {e}")
            return False
    
    async def run_full_ai_activation(self) -> bool:
        """Activa completamente los modelos de IA"""
        logger.info("🧠 Iniciando activación completa de IA...")
        
        try:
            # Verificar memoria inicial
            initial_memory = SystemMonitor.get_memory_usage().get('process_rss', 0)
            if initial_memory:
                logger.info(f"💾 RAM inicial: {initial_memory:.1f} MB")
            
            # Entrenar normalmente
            if not self.run_training():
                logger.error("❌ Error en entrenamiento básico")
                return False
            
            # Forzar carga de modelos de IA
            logger.info("🚀 Activando modelos de IA...")
            
            if not await self.ai_tester.test_ai_models_async():
                logger.warning("⚠️ Algunos modelos de IA no se cargaron correctamente")
            
            # Verificar memoria final
            final_memory = SystemMonitor.get_memory_usage().get('process_rss', 0)
            if final_memory and initial_memory:
                logger.info(f"💾 RAM final: {final_memory:.1f} MB")
                logger.info(f"📈 Incremento: +{final_memory - initial_memory:.1f} MB")
            
            logger.info("🎉 ¡IA completa activada y lista!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en activación de IA: {e}")
            return False


class InteractiveMenu:
    """Menú interactivo del sistema"""
    
    def __init__(self):
        self.manager = ChatbotManager()
    
    def display_menu(self) -> None:
        """Muestra el menú principal"""
        print("\n" + "="*60)
        print("🏨 CHATBOT DE HOTELERÍA - MENÚ PRINCIPAL")
        print("="*60)
        print("🤖 OPERACIONES DEL BOT:")
        print("   1. Iniciar el chatbot")
        print("   2. Entrenar chatbot con documentos actuales")
        print("   3. Analizar datos y estadísticas")
        print("   4. Solo cargar documentos")
        print()
        print("🧪 TESTING Y DIAGNÓSTICO:")
        print("   5. Verificación rápida del sistema")
        print("   6. Ver uso de memoria")
        print("   7. Probar modelos de IA")
        print("   8. Entrenar + Activar IA completa")
        print()
        print("📋 UTILIDADES:")
        print("   9. Generar plantillas de ejemplo")
        print("   0. Salir")
        print("="*60)
    
    def get_user_choice(self) -> str:
        """Obtiene la elección del usuario"""
        return input("\n🎯 Selecciona una opción [0-9]: ").strip()
    
    def handle_choice(self, choice: str) -> bool:
        """Maneja la elección del usuario"""
        try:
            if choice == '1':
                print("\n🚀 Iniciando el chatbot...")
                return self.manager.run_bot()
                
            elif choice == '2':
                print("\n📚 Entrenando chatbot con documentos actuales...")
                return self.manager.run_training()
                
            elif choice == '3':
                print("\n📊 Analizando datos...")
                return self.manager.run_analytics()
                
            elif choice == '4':
                print("\n📄 Cargando documentos...")
                from ai.vectorstore import vectorstore_manager
                vectorstore_manager.update_knowledge()
                print("✅ Documentos cargados exitosamente")
                return True
                
            elif choice == '5':
                print("\n🔍 Ejecutando verificación rápida...")
                return self._quick_system_check()
                
            elif choice == '6':
                print("\n💾 Mostrando uso de memoria...")
                return self.manager.monitor.display_memory_usage()
                
            elif choice == '7':
                print("\n🧪 Probando modelos de IA...")
                return self._test_ai_models()
                
            elif choice == '8':
                print("\n🧠 Entrenando + Activando IA completa...")
                return asyncio.run(self.manager.run_full_ai_activation())
                
            elif choice == '9':
                print("\n📋 Generando plantillas de ejemplo...")
                return self._generate_example_templates()
                
            elif choice == '0':
                print("\n👋 ¡Hasta luego!")
                return False
                
            else:
                print("❌ Opción no válida. Intenta de nuevo.")
                return True
                
        except KeyboardInterrupt:
            print("\n⏹️ Operación interrumpida por el usuario")
            return True
        except Exception as e:
            logger.error(f"❌ Error en la operación: {e}")
            return True
    
    def _quick_system_check(self) -> bool:
        """Verificación rápida del sistema"""
        logger.info("🔍 Verificación rápida del sistema...")
        
        checks = [
            ("Configuración", self.manager.validator.validate_configuration),
            ("Dependencias", self.manager.validator.validate_dependencies),
            ("Documentos", self.manager.validator.validate_documents),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            logger.info(f"📋 Verificando {check_name}...")
            if not check_func():
                all_passed = False
        
        if all_passed:
            logger.info("✅ Verificación rápida completada exitosamente")
        else:
            logger.warning("⚠️ Algunas verificaciones fallaron")
        
        return all_passed
    
    def _test_ai_models(self) -> bool:
        """Prueba los modelos de IA"""
        from ai.models import ai_models
        
        if ai_models.use_lazy_loading:
            logger.info("🔄 Probando modelos con lazy loading (async)...")
            return asyncio.run(self.manager.ai_tester.test_ai_models_async())
        else:
            logger.info("🔄 Probando modelos sin lazy loading (sync)...")
            return self.manager.ai_tester.test_ai_models_sync()
    
    def _generate_example_templates(self) -> bool:
        """Genera plantillas de ejemplo"""
        logger.info("📋 Generando plantillas de ejemplo...")
        
        try:
            # Aquí podrías generar archivos de ejemplo
            logger.info("✅ Plantillas generadas (funcionalidad en desarrollo)")
            return True
        except Exception as e:
            logger.error(f"❌ Error generando plantillas: {e}")
            return False
    
    def run(self) -> None:
        """Ejecuta el menú interactivo"""
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if not self.handle_choice(choice):
                break


def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(
        description="🏨 ChatBot de Hotelería - Sistema de IA Inteligente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python src/main.py                    # Menú interactivo
  python src/main.py --mode bot         # Iniciar bot directamente
  python src/main.py --mode train       # Entrenar sistema
  python src/main.py --mode analytics   # Ver analíticas
  python src/main.py --check            # Solo verificar configuración
        """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["bot", "train", "analytics"],
        default="bot", 
        help="Modo de ejecución"
    )
    parser.add_argument(
        "--check", 
        action="store_true",
        help="Solo verificar configuración"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="ChatBot de Hotelería v2.0.0"
    )

    args = parser.parse_args()

    # Header del sistema
    logger.info("🏨 ChatBot de Hotelería - Sistema de IA Inteligente")
    logger.info("=" * 60)
    logger.info("📅 Versión: 2.0.0")
    logger.info(f"🐍 Python: {sys.version.split()[0]}")
    logger.info(f"📁 Directorio: {os.getcwd()}")
    logger.info("=" * 60)

    # Verificación de configuración
    if args.check:
        logger.info("🔍 Verificando configuración...")
        validator = SystemValidator()
        validator.validate_configuration()
        validator.validate_dependencies()
        validator.validate_documents()
        return

    # Ejecutar modo específico o menú interactivo
    if len(sys.argv) > 1:
        # Modo comando directo
        manager = ChatbotManager()
        
        if args.mode == "bot":
            success = manager.run_bot()
        elif args.mode == "train":
            success = manager.run_training()
        elif args.mode == "analytics":
            success = manager.run_analytics()
        
        if success:
            logger.info("✅ Operación completada exitosamente")
        else:
            logger.error("❌ Operación falló")
            sys.exit(1)
    else:
        # Menú interactivo
        menu = InteractiveMenu()
        menu.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)