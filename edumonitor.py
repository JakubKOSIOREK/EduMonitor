""" edumonitor.py """

import os
from src.logger_setup import setup_logger
from src.arg_parser import get_arguments, process_csv_argument
from src.json_loader import JSONLoader
from src.table_display import TableDisplay
from src.employee_management import EmployeeManager
from src.db_fetcher import DBFetcher

def main():
    logger = setup_logger()
    logger.info("Program EduMonitor został uruchomiony.")

    # Wczytanie argumentów z linii komend
    args = get_arguments()

    # Inicjalizacja loaderów
    json_loader = JSONLoader()
    db_fetcher = DBFetcher()
    table_display = TableDisplay()

    employees_json = None
    employees_db = []  # Domyślna pusta lista dla danych z URL

    if args.csv:
        # Przetwarzanie pliku CSV
        filtered_data = process_csv_argument(args.csv)
        if filtered_data:
            # Pobranie danych z bazy URL
            employees_db = db_fetcher.fetch_employee_data_from_url()

            # Konwersja przefiltrowanych danych na obiekty Employee
            employees_json = json_loader.convert_to_json_structure(filtered_data)

            # Porównanie z danymi z bazy URL
            if employees_json and employees_db:
                manager = EmployeeManager(employees_json, employees_db)
                employees_json = manager.check_employee_in_db()

            # Zapis zaktualizowanych danych do JSON
            json_loader.save_to_json(employees_json)
        else:
            return

    elif args.shell:
        # Ładowanie pracowników z najnowszego JSON
        employees_json = json_loader.load_employees_from_json()

    # Wyświetlanie wyników w tabeli, jeśli są dane do wyświetlenia
    if args.shell and employees_json:
        manager = EmployeeManager(employees_json, employees_db)
        kadra_zarzadcza, kadra_kierownicza, pracownicy = manager.filter_by_position()
        table_display.display_all_groups(kadra_zarzadcza, kadra_kierownicza, pracownicy)

    logger.info("Program EduMonitor zakończył działanie.")

if __name__ == '__main__':
    main()