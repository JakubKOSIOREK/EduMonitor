""" edumonitor.py """

import argparse
from src.csv_loader import load_file, filter_file
from src.employee_class import Employee
from src.db_fetcher import fetch_employee_data_from_url
from src.config_loader import get_database_url
from src.logger_setup import setup_logger
from src.table_display import display_all_groups

# Inicjalizacja loggera
logger = setup_logger()

def main():
    logger.info("Program EduMonitor został uruchomiony.")
    
    parser = argparse.ArgumentParser(description='EduMonitor - wczytaj plik CSV i wyświetl dane.')
    parser.add_argument('--csv', type=str, help='Ścieżka do pliku CSV')
    parser.add_argument('--shell', action='store_true', help='Wyświetlenie wyników w konsoli (tabele)')  # Flaga do wyświetlania wyników w konsoli
    args = parser.parse_args()

    if not args.csv:
        logger.error("Błąd: Musisz podać ścieżkę do pliku CSV lub użyć trybu testowego.")
        return
    csv_path = args.csv
    url = get_database_url()  # Pobieramy URL z config.ini
    if not url:
        logger.error("Błąd: Nie znaleziono URL w pliku konfiguracyjnym.")
        return

    # Wczytanie i przetworzenie pliku CSV
    raw_data = load_file(csv_path)
    employees_csv = filter_file(raw_data)

    employees_db = fetch_employee_data_from_url(url)

    # Sprawdzenie pracowników z CSV w bazie danych URL
    updated_employees = Employee.check_employee_in_db(employees_csv, employees_db)

    # Podział na trzy kategorie: kadra zarządzająca, kadra kierownicza, pracownicy
    kadra_zarzadcza, kadra_kierownicza, pracownicy = Employee.filter_by_position(updated_employees)

    # Wyświetlanie wyników na konsoli tylko, jeśli podano flagę --shell
    if args.shell:
        display_all_groups(kadra_zarzadcza, kadra_kierownicza, pracownicy)

    logger.info("Program EduMonitor został zakończony.")

if __name__ == '__main__':
    main()
