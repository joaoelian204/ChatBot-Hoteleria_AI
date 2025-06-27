#!/usr/bin/env python3
"""
🧪 SISTEMA DE TESTING UNIVERSAL PROFESIONAL PARA CHATBOT
=========================================================

Sistema de testing avanzado que evalúa todas las funciones del chatbot
con diferentes niveles de dificultad y casos edge complejos.

Características:
- Tests unitarios y de integración
- Benchmarking de rendimiento
- Tests de estrés y robustez
- Validación de respuestas
- Métricas de calidad
- Tests de casos extremos

Uso:
    python -m src.testing.test_suite
    python -m src.testing.test_suite --mode stress
    python -m src.testing.test_suite --difficulty hard
"""

import json
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import colorama
from colorama import Fore

# Configurar path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from ai.fallback_handler import (
        generate_fallback_response,
        get_amenities_info_from_documents,
        get_cheapest_room_info,
        get_contact_info_from_documents,
        get_hotel_name_from_documents,
        get_most_expensive_room_info,
        get_restaurant_info_from_documents,
        get_room_info_from_documents,
        get_time_based_greeting,
        normalize_text,
        read_document_safely,
    )
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("Asegúrate de ejecutar desde el directorio raíz del proyecto")
    sys.exit(1)

# Inicializar colorama
colorama.init(autoreset=True)


@dataclass
class TestResult:
    """Resultado de un test individual"""
    name: str
    passed: bool
    duration: float
    expected: Optional[str] = None
    actual: Optional[str] = None
    error: Optional[str] = None
    performance_score: Optional[float] = None


@dataclass
class TestSuiteResult:
    """Resultado completo de la suite de tests"""
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    total_duration: float = 0.0
    coverage_score: float = 0.0
    performance_score: float = 0.0
    results: List[TestResult] = None

    def __post_init__(self):
        if self.results is None:
            self.results = []


class ChatbotTestSuite:
    """Suite de testing profesional para el chatbot"""

    def __init__(self, difficulty: str = "medium", verbose: bool = True):
        self.difficulty = difficulty
        self.verbose = verbose
        self.test_results = TestSuiteResult()
        self.start_time = time.time()

        # Configuración de dificultad
        self.difficulty_configs = {
            "easy": {
                "stress_iterations": 10,
                "concurrent_tests": 2,
                "timeout": 5.0,
                "edge_cases": False
            },
            "medium": {
                "stress_iterations": 50,
                "concurrent_tests": 5,
                "timeout": 3.0,
                "edge_cases": True
            },
            "hard": {
                "stress_iterations": 100,
                "concurrent_tests": 10,
                "timeout": 1.0,
                "edge_cases": True
            },
            "nightmare": {
                "stress_iterations": 500,
                "concurrent_tests": 20,
                "timeout": 0.5,
                "edge_cases": True
            }
        }

        self.config = self.difficulty_configs.get(difficulty, self.difficulty_configs["medium"])

        # Tests básicos
        self.basic_tests = [
            ("Saludo básico", "hola"),
            ("Saludo formal", "Buenos días"),
            ("Habitación económica", "cuál es la habitación más barata"),
            ("Habitación lujosa", "habitación más cara"),
            ("Restaurantes", "información sobre restaurantes"),
            ("Menús", "precios de los menús"),
            ("Amenidades", "qué actividades tienen"),
            ("Contacto", "información de contacto"),
            ("Reservas", "cómo hacer una reserva"),
            ("Ayuda", "ayuda")
        ]

        # Tests de dificultad media
        self.medium_tests = [
            ("Consulta con errores tipográficos", "abl me gustari saver de las avitasiones"),
            ("Consulta mezclada", "Hola, necesito saber precios de habitaciones y restaurantes"),
            ("Consulta en inglés", "What are your room prices?"),
            ("Consulta con caracteres especiales", "¿Cuál es la habitación más económica? 💰🏠"),
            ("Consulta muy larga", "Me gustaría obtener información detallada sobre todas las habitaciones disponibles en el hotel, incluyendo precios, servicios incluidos, amenidades, políticas de cancelación y disponibilidad para las próximas fechas"),
            ("Consulta ambigua", "precio"),
            ("Consulta sin contexto", "¿cuánto cuesta?"),
            ("Múltiples preguntas", "¿Cuáles son los precios de las habitaciones y qué restaurantes tienen?")
        ]

        # Tests extremos (hard/nightmare)
        self.extreme_tests = [
            ("Texto vacío", ""),
            ("Solo espacios", "   "),
            ("Solo símbolos", "!@#$%^&*()"),
            ("Texto muy largo", "a" * 1000),
            ("Caracteres unicode", "🏨🍽️🏊‍♂️💰🌟"),
            ("HTML/Scripts", "<script>alert('test')</script>"),
            ("SQL injection", "'; DROP TABLE users; --"),
            ("Path traversal", "../../../etc/passwd"),
            ("Números aleatorios", "123456789"),
            ("Caracteres especiales", "çñáéíóúü"),
            ("Texto en otros idiomas", "Здравствуйте, где ресторан?"),
            ("JSON malformado", '{"test": incomplete'),
            ("XML malformado", "<xml><unclosed>"),
            ("URLs", "https://malicious-site.com/hack"),
            ("Comandos shell", "rm -rf /")
        ]

    def print_header(self):
        """Imprime el header del sistema de testing"""
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}🧪 SISTEMA DE TESTING UNIVERSAL - CHATBOT DE HOTELERÍA 🤖")
        print(f"{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.YELLOW}📊 Dificultad: {self.difficulty.upper()}")
        print(f"{Fore.YELLOW}⚙️  Configuración:")
        print(f"{Fore.WHITE}   - Tests de estrés: {self.config['stress_iterations']}")
        print(f"{Fore.WHITE}   - Tests concurrentes: {self.config['concurrent_tests']}")
        print(f"{Fore.WHITE}   - Timeout: {self.config['timeout']}s")
        print(f"{Fore.WHITE}   - Casos extremos: {'Sí' if self.config['edge_cases'] else 'No'}")
        print(f"{Fore.CYAN}{'=' * 80}\n")

    def run_test(self, test_name: str, test_input: str, expected_keywords: List[str] = None) -> TestResult:
        """Ejecuta un test individual y mide el rendimiento"""
        start_time = time.time()

        try:
            # Ejecutar el test con timeout
            result = self._execute_with_timeout(
                lambda: generate_fallback_response(test_input),
                self.config['timeout']
            )

            duration = time.time() - start_time

            # Validar el resultado
            if result is None or not isinstance(result, str):
                return TestResult(
                    name=test_name,
                    passed=False,
                    duration=duration,
                    actual=str(result),
                    error="Respuesta inválida o None"
                )

            # Verificar keywords esperadas
            passed = True
            if expected_keywords:
                result_lower = result.lower()
                for keyword in expected_keywords:
                    if keyword.lower() not in result_lower:
                        passed = False
                        break

            # Calcular score de rendimiento
            performance_score = min(100.0, (1.0 / max(duration, 0.001)) * 10)

            return TestResult(
                name=test_name,
                passed=passed,
                duration=duration,
                actual=result[:200] + "..." if len(result) > 200 else result,
                performance_score=performance_score
            )

        except Exception as e:
            duration = time.time() - start_time
            return TestResult(
                name=test_name,
                passed=False,
                duration=duration,
                error=str(e),
                performance_score=0.0
            )

    def _execute_with_timeout(self, func, timeout):
        """Ejecuta una función con timeout"""
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError("Test excedió el tiempo límite")

        # Configurar timeout (solo en sistemas Unix)
        if hasattr(signal, 'SIGALRM'):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(timeout))

        try:
            result = func()
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)  # Cancelar timeout
            return result
        except TimeoutError:
            raise
        except Exception as e:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            raise e

    def test_basic_functionality(self):
        """Tests básicos de funcionalidad"""
        print(f"{Fore.GREEN}📋 EJECUTANDO TESTS BÁSICOS...")

        for test_name, test_input in self.basic_tests:
            result = self.run_test(test_name, test_input)
            self._add_result(result)

            if self.verbose:
                status = f"{Fore.GREEN}✅ PASS" if result.passed else f"{Fore.RED}❌ FAIL"
                print(f"  {status} {test_name} ({result.duration:.3f}s)")
                if not result.passed and result.error:
                    print(f"    {Fore.RED}Error: {result.error}")

    def test_medium_difficulty(self):
        """Tests de dificultad media"""
        print(f"\n{Fore.YELLOW}📊 EJECUTANDO TESTS DE DIFICULTAD MEDIA...")

        for test_name, test_input in self.medium_tests:
            result = self.run_test(test_name, test_input)
            self._add_result(result)

            if self.verbose:
                status = f"{Fore.GREEN}✅ PASS" if result.passed else f"{Fore.RED}❌ FAIL"
                print(f"  {status} {test_name} ({result.duration:.3f}s)")

    def test_extreme_cases(self):
        """Tests de casos extremos"""
        if not self.config['edge_cases']:
            return

        print(f"\n{Fore.RED}🔥 EJECUTANDO TESTS EXTREMOS...")

        for test_name, test_input in self.extreme_tests:
            result = self.run_test(test_name, test_input)
            self._add_result(result)

            if self.verbose:
                status = f"{Fore.GREEN}✅ PASS" if result.passed else f"{Fore.RED}❌ FAIL"
                print(f"  {status} {test_name} ({result.duration:.3f}s)")

    def test_performance_stress(self):
        """Tests de estrés y rendimiento"""
        print(f"\n{Fore.MAGENTA}⚡ EJECUTANDO TESTS DE ESTRÉS...")

        stress_queries = [
            "hola",
            "habitación más barata",
            "restaurantes",
            "contacto"
        ]

        total_time = 0
        successful_requests = 0

        for i in range(self.config['stress_iterations']):
            query = stress_queries[i % len(stress_queries)]
            start_time = time.time()

            try:
                result = generate_fallback_response(query)
                duration = time.time() - start_time
                total_time += duration

                if result and isinstance(result, str) and len(result) > 0:
                    successful_requests += 1

            except Exception:
                duration = time.time() - start_time
                total_time += duration

            if self.verbose and i % 10 == 0:
                print(f"  Progreso: {i}/{self.config['stress_iterations']} ({(i / self.config['stress_iterations'] * 100):.1f}%)")

        avg_response_time = total_time / self.config['stress_iterations']
        success_rate = successful_requests / self.config['stress_iterations'] * 100

        # Crear resultado del test de estrés
        stress_result = TestResult(
            name="Test de Estrés",
            passed=success_rate >= 90 and avg_response_time <= 1.0,
            duration=total_time,
            performance_score=success_rate
        )

        self._add_result(stress_result)

        print(f"  {Fore.CYAN}📈 Tiempo promedio de respuesta: {avg_response_time:.3f}s")
        print(f"  {Fore.CYAN}📊 Tasa de éxito: {success_rate:.1f}%")

    def test_concurrent_access(self):
        """Tests de acceso concurrente"""
        print(f"\n{Fore.BLUE}🔄 EJECUTANDO TESTS CONCURRENTES...")

        def worker_task(worker_id):
            results = []
            queries = ["hola", "habitaciones", "restaurantes", "contacto"]

            for i in range(5):  # Cada worker hace 5 requests
                query = f"{queries[i % len(queries)]} worker-{worker_id}"
                start_time = time.time()

                try:
                    result = generate_fallback_response(query)
                    duration = time.time() - start_time

                    success = result and isinstance(result, str) and len(result) > 0
                    results.append((success, duration))

                except Exception:
                    results.append((False, time.time() - start_time))

            return results

        # Ejecutar workers concurrentes
        with ThreadPoolExecutor(max_workers=self.config['concurrent_tests']) as executor:
            futures = [executor.submit(worker_task, i) for i in range(self.config['concurrent_tests'])]
            all_results = []

            for future in futures:
                try:
                    worker_results = future.result(timeout=10)
                    all_results.extend(worker_results)
                except Exception as e:
                    print(f"  {Fore.RED}❌ Worker falló: {e}")

        # Analizar resultados
        successful = sum(1 for success, _ in all_results if success)
        total = len(all_results)
        avg_time = sum(duration for _, duration in all_results) / total if total > 0 else 0

        concurrent_result = TestResult(
            name="Test Concurrente",
            passed=successful / total >= 0.9 if total > 0 else False,
            duration=avg_time,
            performance_score=successful / total * 100 if total > 0 else 0
        )

        self._add_result(concurrent_result)

        print(f"  {Fore.CYAN}🔢 Requests exitosos: {successful}/{total}")
        print(f"  {Fore.CYAN}⏱️  Tiempo promedio: {avg_time:.3f}s")

    def test_document_integration(self):
        """Tests de integración con documentos"""
        print(f"\n{Fore.CYAN}📄 EJECUTANDO TESTS DE INTEGRACIÓN...")

        # Test de lectura de documentos
        docs_to_test = [
            "hotel_info.txt",
            "habitaciones_precios.txt",
            "restaurantes_menus.txt",
            "amenidades_actividades.txt"
        ]

        for doc in docs_to_test:
            start_time = time.time()
            try:
                content = read_document_safely(doc)
                duration = time.time() - start_time

                doc_result = TestResult(
                    name=f"Lectura {doc}",
                    passed=len(content) > 0,
                    duration=duration,
                    actual=f"Contenido: {len(content)} caracteres"
                )

            except Exception as e:
                duration = time.time() - start_time
                doc_result = TestResult(
                    name=f"Lectura {doc}",
                    passed=False,
                    duration=duration,
                    error=str(e)
                )

            self._add_result(doc_result)

            if self.verbose:
                status = f"{Fore.GREEN}✅ PASS" if doc_result.passed else f"{Fore.RED}❌ FAIL"
                print(f"  {status} {doc_result.name} ({doc_result.duration:.3f}s)")

    def test_functions_individually(self):
        """Tests de funciones individuales"""
        print(f"\n{Fore.MAGENTA}🔧 EJECUTANDO TESTS DE FUNCIONES INDIVIDUALES...")

        functions_to_test = [
            ("get_hotel_name_from_documents", get_hotel_name_from_documents, []),
            ("get_time_based_greeting", get_time_based_greeting, []),
            ("normalize_text", normalize_text, ["¡Hola! ¿Cómo está?"]),
            ("get_room_info_from_documents", get_room_info_from_documents, []),
            ("get_cheapest_room_info", get_cheapest_room_info, []),
            ("get_most_expensive_room_info", get_most_expensive_room_info, []),
            ("get_restaurant_info_from_documents", get_restaurant_info_from_documents, []),
            ("get_amenities_info_from_documents", get_amenities_info_from_documents, []),
            ("get_contact_info_from_documents", get_contact_info_from_documents, [])
        ]

        for func_name, func, args in functions_to_test:
            start_time = time.time()
            try:
                result = func(*args)
                duration = time.time() - start_time

                func_result = TestResult(
                    name=f"Función {func_name}",
                    passed=result is not None,
                    duration=duration,
                    actual=str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
                )

            except Exception as e:
                duration = time.time() - start_time
                func_result = TestResult(
                    name=f"Función {func_name}",
                    passed=False,
                    duration=duration,
                    error=str(e)
                )

            self._add_result(func_result)

            if self.verbose:
                status = f"{Fore.GREEN}✅ PASS" if func_result.passed else f"{Fore.RED}❌ FAIL"
                print(f"  {status} {func_result.name} ({func_result.duration:.3f}s)")

    def _add_result(self, result: TestResult):
        """Añade un resultado a la suite"""
        self.test_results.results.append(result)
        self.test_results.total_tests += 1

        if result.passed:
            self.test_results.passed += 1
        else:
            self.test_results.failed += 1

    def generate_report(self):
        """Genera un reporte completo de los tests"""
        end_time = time.time()
        self.test_results.total_duration = end_time - self.start_time

        # Calcular métricas
        pass_rate = (self.test_results.passed / self.test_results.total_tests * 100) if self.test_results.total_tests > 0 else 0
        avg_duration = sum(r.duration for r in self.test_results.results) / len(self.test_results.results) if self.test_results.results else 0
        avg_performance = sum(r.performance_score for r in self.test_results.results if r.performance_score) / len([r for r in self.test_results.results if r.performance_score]) if any(r.performance_score for r in self.test_results.results) else 0

        # Header del reporte
        print(f"\n{Fore.CYAN}{'=' * 80}")
        print(f"{Fore.CYAN}📊 REPORTE FINAL DE TESTING")
        print(f"{Fore.CYAN}{'=' * 80}")

        # Resumen general
        print(f"\n{Fore.YELLOW}📈 RESUMEN GENERAL:")
        print(f"{Fore.WHITE}   Total de tests: {self.test_results.total_tests}")
        print(f"{Fore.GREEN}   ✅ Pasados: {self.test_results.passed}")
        print(f"{Fore.RED}   ❌ Fallidos: {self.test_results.failed}")
        print(f"{Fore.CYAN}   📊 Tasa de éxito: {pass_rate:.1f}%")
        print(f"{Fore.CYAN}   ⏱️  Tiempo total: {self.test_results.total_duration:.2f}s")
        print(f"{Fore.CYAN}   📊 Tiempo promedio: {avg_duration:.3f}s")
        print(f"{Fore.CYAN}   🚀 Score de rendimiento: {avg_performance:.1f}/100")

        # Clasificación de calidad
        if pass_rate >= 95:
            quality = f"{Fore.GREEN}🌟 EXCELENTE"
        elif pass_rate >= 85:
            quality = f"{Fore.YELLOW}✅ BUENO"
        elif pass_rate >= 70:
            quality = f"{Fore.YELLOW}⚠️  ACEPTABLE"
        else:
            quality = f"{Fore.RED}❌ NECESITA MEJORAS"

        print(f"\n{Fore.CYAN}🏆 CALIDAD DEL CHATBOT: {quality}")

        # Tests fallidos
        failed_tests = [r for r in self.test_results.results if not r.passed]
        if failed_tests:
            print(f"\n{Fore.RED}❌ TESTS FALLIDOS:")
            for test in failed_tests[:10]:  # Mostrar máximo 10
                print(f"{Fore.RED}   • {test.name}")
                if test.error:
                    print(f"{Fore.RED}     Error: {test.error[:100]}...")

        # Tests más lentos
        slowest_tests = sorted(self.test_results.results, key=lambda x: x.duration, reverse=True)[:5]
        if slowest_tests:
            print(f"\n{Fore.YELLOW}🐌 TESTS MÁS LENTOS:")
            for test in slowest_tests:
                print(f"{Fore.YELLOW}   • {test.name}: {test.duration:.3f}s")

        # Recomendaciones
        print(f"\n{Fore.CYAN}💡 RECOMENDACIONES:")
        if pass_rate < 90:
            print(f"{Fore.YELLOW}   • Revisar y corregir los tests fallidos")
        if avg_duration > 1.0:
            print(f"{Fore.YELLOW}   • Optimizar el rendimiento del chatbot")
        if avg_performance < 70:
            print(f"{Fore.YELLOW}   • Mejorar la velocidad de respuesta")

        print(f"{Fore.GREEN}   • El chatbot está funcionando correctamente" if pass_rate >= 90 else f"{Fore.RED}   • El chatbot necesita atención")

        # Guardar reporte en JSON
        self._save_report_json()

        print(f"\n{Fore.CYAN}💾 Reporte guardado en: reports/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        print(f"{Fore.CYAN}{'=' * 80}\n")

    def _save_report_json(self):
        """Guarda el reporte en formato JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Crear directorio de reportes si no existe
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        report_data = {
            "timestamp": timestamp,
            "difficulty": self.difficulty,
            "summary": {
                "total_tests": self.test_results.total_tests,
                "passed": self.test_results.passed,
                "failed": self.test_results.failed,
                "pass_rate": (self.test_results.passed / self.test_results.total_tests * 100) if self.test_results.total_tests > 0 else 0,
                "total_duration": self.test_results.total_duration,
                "avg_performance": sum(r.performance_score for r in self.test_results.results if r.performance_score) / len([r for r in self.test_results.results if r.performance_score]) if any(r.performance_score for r in self.test_results.results) else 0
            },
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "duration": r.duration,
                    "error": r.error,
                    "performance_score": r.performance_score
                }
                for r in self.test_results.results
            ]
        }

        report_file = reports_dir / f"test_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # Limpiar reportes antiguos (mantener solo los últimos 10)
        self._cleanup_old_reports(reports_dir)

    def _cleanup_old_reports(self, reports_dir: Path):
        """Limpia reportes antiguos manteniendo solo los últimos 10"""
        try:
            import glob
            pattern = str(reports_dir / "test_report_*.json")
            reports = glob.glob(pattern)

            if len(reports) > 10:
                # Ordenar por fecha de modificación y eliminar los más antiguos
                reports.sort(key=lambda x: Path(x).stat().st_mtime)
                old_reports = reports[:-10]  # Mantener solo los últimos 10

                for old_report in old_reports:
                    try:
                        Path(old_report).unlink()
                    except Exception:
                        pass  # Ignorar errores al eliminar
        except Exception:
            pass  # Ignorar errores en la limpieza

    def run_all_tests(self):
        """Ejecuta toda la suite de tests"""
        self.print_header()

        try:
            # Tests básicos
            self.test_basic_functionality()

            # Tests de dificultad media
            if self.difficulty in ["medium", "hard", "nightmare"]:
                self.test_medium_difficulty()

            # Tests extremos
            if self.difficulty in ["hard", "nightmare"]:
                self.test_extreme_cases()

            # Tests de rendimiento
            self.test_performance_stress()

            # Tests concurrentes
            if self.difficulty in ["medium", "hard", "nightmare"]:
                self.test_concurrent_access()

            # Tests de integración
            self.test_document_integration()

            # Tests de funciones individuales
            self.test_functions_individually()

            # Generar reporte final
            self.generate_report()

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Tests interrumpidos por el usuario")
            self.generate_report()
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error fatal en los tests: {e}")
            traceback.print_exc()


def show_menu():
    """Muestra el menú interactivo"""
    print(f"\n{Fore.CYAN}🧪 SISTEMA DE TESTING UNIVERSAL - CHATBOT")
    print(f"{Fore.CYAN}{'=' * 50}")
    print(f"{Fore.YELLOW}Selecciona el nivel de dificultad:")
    print(f"{Fore.GREEN}1. 🟢 Fácil      - Tests básicos (10 iteraciones)")
    print(f"{Fore.YELLOW}2. 🟡 Medio     - Tests completos (50 iteraciones)")
    print(f"{Fore.RED}3. 🔴 Difícil    - Tests intensivos (100 iteraciones)")
    print(f"{Fore.MAGENTA}4. 💀 Pesadilla - Tests extremos (500 iteraciones)")
    print(f"{Fore.BLUE}5. 📊 Ver último reporte")
    print(f"{Fore.CYAN}6. ❌ Salir")
    print(f"{Fore.CYAN}{'=' * 50}")


def main():
    """Función principal con menú interactivo"""
    if len(sys.argv) > 1:
        # Modo comando directo
        difficulty = sys.argv[1] if sys.argv[1] in ["easy", "medium", "hard", "nightmare"] else "medium"
        suite = ChatbotTestSuite(difficulty=difficulty, verbose=True)
        suite.run_all_tests()
        return

    # Modo interactivo
    while True:
        show_menu()

        try:
            choice = input(f"\n{Fore.WHITE}Ingresa tu opción (1-6): ").strip()

            if choice == "1":
                suite = ChatbotTestSuite(difficulty="easy", verbose=True)
                suite.run_all_tests()
            elif choice == "2":
                suite = ChatbotTestSuite(difficulty="medium", verbose=True)
                suite.run_all_tests()
            elif choice == "3":
                suite = ChatbotTestSuite(difficulty="hard", verbose=True)
                suite.run_all_tests()
            elif choice == "4":
                confirm = input(f"{Fore.RED}⚠️  Modo pesadilla puede tardar varios minutos. ¿Continuar? (s/N): ")
                if confirm.lower() in ['s', 'si', 'y', 'yes']:
                    suite = ChatbotTestSuite(difficulty="nightmare", verbose=True)
                    suite.run_all_tests()
            elif choice == "5":
                # Buscar último reporte
                import glob
                reports = glob.glob("reports/test_report_*.json")
                if reports:
                    latest_report = max(reports)
                    with open(latest_report, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    print(f"\n{Fore.CYAN}📊 ÚLTIMO REPORTE ({data['timestamp']}):")
                    print(f"{Fore.WHITE}Archivo: {latest_report}")
                    print(f"{Fore.WHITE}Dificultad: {data['difficulty']}")
                    print(f"{Fore.WHITE}Tests: {data['summary']['total_tests']}")
                    print(f"{Fore.GREEN}Pasados: {data['summary']['passed']}")
                    print(f"{Fore.RED}Fallidos: {data['summary']['failed']}")
                    print(f"{Fore.CYAN}Tasa de éxito: {data['summary']['pass_rate']:.1f}%")
                else:
                    print(f"{Fore.YELLOW}No se encontraron reportes previos")
            elif choice == "6":
                print(f"{Fore.GREEN}¡Hasta luego! 👋")
                break
            else:
                print(f"{Fore.RED}Opción inválida. Por favor, selecciona 1-6.")

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Saliendo...")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")


if __name__ == "__main__":
    main()
