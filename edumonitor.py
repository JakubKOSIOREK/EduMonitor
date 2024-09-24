""" edumonitor.py """

import os
import argparse
from src.csv_loader import CSVLoader
from src.db_fetcher import fetch_employee_data_from_url
from src.config_loader import ConfigLoader
from src.logger_setup import setup_logger
from src.table_display import TableDisplay
from src.html_generator import HTMLReportGenerator
from src.employee_management import EmployeeManager


def main():
    logger = setup_logger()
    logger.info("Program EduMonitor został uruchomiony.")

    parser = argparse.ArgumentParser(description='EduMonitor - wczytaj plik CSV i wyświetl dane.')
    parser.add_argument('--csv', type=str, help='Ścieżka do pliku CSV')
    parser.add_argument('--test-csv', action='store_true', help='Użycie testowego pliku CSV z katalogu tests/test_files/')
    parser.add_argument('--shell', action='store_true', help='Wyświetlenie wyników w konsoli (tabele)')
    parser.add_argument('--lists-html', action='store_true', help='Generowanie list pracowników w formacie HTML')
    parser.add_argument('--report-html', action='store_true', help='Generowanie raportu o stanie wyszkolenia w formacie HTML')
    args = parser.parse_args()

    if args.test_csv:
        test_csv_path = os.path.join('tests', 'test_files', 'dane_testowe.csv')
        if not os.path.exists(test_csv_path):
            logger.error(f"Błąd: Plik testowy {test_csv_path} nie istnieje.")
            return
        csv_path = test_csv_path
        logger.info(f"Użycie testowego pliku CSV: {csv_path}")
    elif args.csv:
        csv_path = args.csv
    else:
        logger.error("Błąd: Musisz podać ścieżkę do pliku CSV lub użyć flagi --test-csv.")
        return

    # Użycie ConfigLoader do wczytania konfiguracji
    config_loader = ConfigLoader()
    url = config_loader.get_database_url()
    if not url:
        logger.error("Błąd: Nie znaleziono URL w pliku konfiguracyjnym.")
        return

    # Wczytanie i przetworzenie pliku CSV
    csv_loader = CSVLoader()
    raw_data = csv_loader.load_file_stream(csv_path)
    employees_csv = csv_loader.filter_file(raw_data)
    employees_db = fetch_employee_data_from_url(url)

    # Użycie klasy EmployeeManager do zarządzania pracownikami
    manager = EmployeeManager(employees_csv, employees_db)
    updated_employees = manager.check_employee_in_db()

    # Filtracja pracowników według stanowiska
    kadra_zarzadcza, kadra_kierownicza, pracownicy = manager.filter_by_position()

    # Wyświetlanie wyników w konsoli
    table_display = TableDisplay()
    if args.shell:
        table_display.display_all_groups(kadra_zarzadcza, kadra_kierownicza, pracownicy)

    # Generowanie HTML
    html_generator = HTMLReportGenerator()

    if args.lists_html:
        html_generator.generate_employee_list("Kadra Zarządzająca", kadra_zarzadcza)
        html_generator.generate_employee_list("Kadra Kierownicza", kadra_kierownicza)
        html_generator.generate_employee_list("Pracownicy", pracownicy)

    if args.report_html:
        html_generator.generate_training_report(employees_csv)

    logger.info("Program EduMonitor został zakończony.")


if __name__ == '__main__':
    main()