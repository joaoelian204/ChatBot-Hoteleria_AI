#!/usr/bin/env python3
"""
🧪 RUNNER PRINCIPAL PARA EL SISTEMA DE TESTING
==============================================

Script principal para ejecutar el sistema de testing del chatbot.

Uso:
    python -m src.testing.run_tests
    python -m src.testing.run_tests --difficulty hard
    python -m src.testing.run_tests --quick
"""

import argparse
import sys
from pathlib import Path

from testing.test_suite import ChatbotTestSuite, show_menu

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    """Función principal del runner de tests"""
    parser = argparse.ArgumentParser(description="Sistema de Testing Universal para Chatbot")
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard", "nightmare"],
        default=None,
        help="Nivel de dificultad de los tests"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Ejecutar solo tests básicos (equivale a --difficulty easy)"
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Modo silencioso (sin output detallado)"
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Solo mostrar el último reporte"
    )

    args = parser.parse_args()

    # Mostrar último reporte si se solicita
    if args.report_only:
        show_last_report()
        return

    # Determinar dificultad
    if args.quick:
        difficulty = "easy"
    elif args.difficulty:
        difficulty = args.difficulty
    else:
        # Modo interactivo
        run_interactive_mode()
        return

    # Ejecutar tests con configuración especificada
    verbose = not args.silent
    suite = ChatbotTestSuite(difficulty=difficulty, verbose=verbose)
    suite.run_all_tests()


def show_last_report():
    """Muestra el último reporte de testing"""
    import glob
    import json

    from colorama import Fore

    reports = glob.glob("reports/test_report_*.json")
    if not reports:
        print(f"{Fore.YELLOW}No se encontraron reportes previos")
        return

    latest_report = max(reports)
    try:
        with open(latest_report, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\n{Fore.CYAN}📊 ÚLTIMO REPORTE ({data['timestamp']}):")
        print(f"{Fore.WHITE}Archivo: {latest_report}")
        print(f"{Fore.WHITE}Dificultad: {data['difficulty']}")
        print(f"{Fore.WHITE}Tests: {data['summary']['total_tests']}")
        print(f"{Fore.GREEN}✅ Pasados: {data['summary']['passed']}")
        print(f"{Fore.RED}❌ Fallidos: {data['summary']['failed']}")
        print(f"{Fore.CYAN}📊 Tasa de éxito: {data['summary']['pass_rate']:.1f}%")
        print(f"{Fore.CYAN}⏱️  Duración total: {data['summary'].get('total_duration', 0):.2f}s")

        # Mostrar tests fallidos si existen
        failed_tests = [r for r in data['results'] if not r['passed']]
        if failed_tests:
            print(f"\n{Fore.RED}❌ Tests fallidos:")
            for test in failed_tests[:5]:  # Mostrar máximo 5
                print(f"{Fore.RED}   • {test['name']}")
                if test.get('error'):
                    print(f"{Fore.RED}     Error: {test['error'][:80]}...")

            if len(failed_tests) > 5:
                print(f"{Fore.RED}   ... y {len(failed_tests) - 5} más")

    except Exception as e:
        print(f"{Fore.RED}Error al leer reporte: {e}")


def run_interactive_mode():
    """Ejecuta el modo interactivo"""
    from colorama import Fore

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
                show_last_report()
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
