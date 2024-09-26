""" edumonitor.py """

import os
from src.logger_setup import setup_logger
from src.arg_parser import get_arguments
from src.csv_loader import CSVLoader
from src.json_loader import JSONLoader
from src.table_display import TableDisplay
from src.employee_management import EmployeeManager
from src.utility.validation import validate_csv_row_data
from src.db_fetcher import DBFetcher

def main():
    logger = setup_logger()
    logger.info("Program EduMonitor został uruchomiony.")

    # Wczytanie argumentów z linii komend
    args = get_arguments()

    # Inicjalizacja loaderów
    json_loader = JSONLoader()
    db_fetcher = DBFetcher()  # Inicjalizacja DBFetcher
    table_display = TableDisplay()

    employees_json = None
    employees_db = []  # Domyślna pusta lista dla danych z URL

    if args.csv:
        csv_path = args.csv
        if not os.path.exists(csv_path):
            logger.error(f"Błąd: Plik CSV {csv_path} nie istnieje.")
            return

        # Wczytanie i filtrowanie pliku CSV
        loader = CSVLoader(csv_path, expected_columns=13)
        filtered_data = loader.load_and_filter_data()

        # Walidacja danych
        if filtered_data and validate_csv_row_data(filtered_data):
            # Pobranie danych z bazy URL
            employees_db = db_fetcher.fetch_employee_data_from_url()

            # Konwersja przefiltrowanych danych na obiekty Employee
            employees_json = json_loader.convert_to_json_structure(filtered_data)

            # Porównanie z danymi z bazy URL
            if employees_json and employees_db:
                # Przekazujemy listy pracowników z JSON oraz z URL
                manager = EmployeeManager(employees_json, employees_db)
                employees_json = manager.check_employee_in_db()

            # Zapis zaktualizowanych danych do JSON
            json_loader.save_to_json(employees_json)

        else:
            logger.error("Błąd walidacji danych. Plik nie został zapisany.")
            return

    elif args.shell:
        # Jeśli podano tylko --shell, ładowanie pracowników z najnowszego JSON
        employees_json = json_loader.load_employees_from_json()

    # Wyświetlanie wyników w tabeli, jeśli są dane do wyświetlenia
    if args.shell and employees_json:
        manager = EmployeeManager(employees_json, employees_db)
        kadra_zarzadcza, kadra_kierownicza, pracownicy = manager.filter_by_position()
        table_display.display_all_groups(kadra_zarzadcza, kadra_kierownicza, pracownicy)

    logger.info("Program EduMonitor zakończył działanie.")

if __name__ == '__main__':
    main()
