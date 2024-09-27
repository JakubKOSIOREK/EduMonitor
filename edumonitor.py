""" edumonitor.py """

from src.logger_setup import setup_logger
from src.arg_parser import get_arguments, process_csv_argument
from src.json_loader import JSONLoader
from src.table_display import TableDisplay
from src.employee_management import EmployeeManager
from src.db_fetcher import DBFetcher
from src.html_list_generator import HTMLListGenerator
from src.html_report_generator import HTMLReportGenerator

def main():
    logger = setup_logger()
    logger.info("Program EduMonitor został uruchomiony.")

    # Wczytanie argumentów z linii komend
    args = get_arguments()

    # Inicjalizacja loaderów
    json_loader = JSONLoader()
    db_fetcher = DBFetcher()
    table_display = TableDisplay()
    list_generator = HTMLListGenerator()
    report_generator = HTMLReportGenerator()

    employees_json = None
    employees_db = []

    # Przetwarzanie pliku CSV, jeśli podano
    if args.csv:
        logger.info(f"Przetwarzanie pliku CSV: {args.csv}")
        filtered_data = process_csv_argument(args.csv)
        if filtered_data:
            employees_json = json_loader.convert_to_json_structure(filtered_data)
            json_loader.save_to_json(employees_json)
        else:
            logger.error("Nie udało się przetworzyć pliku CSV.")
            return

    # Jeśli podano --shell, --generate-training-lists lub --generate-training-report, ładujemy najnowszy plik JSON
    if args.shell or args.generate_training_lists or args.generate_training_report:
        logger.info("Ładowanie danych z najnowszego pliku JSON.")
        employees_json = json_loader.load_employees_from_json()

    # Wyświetlanie danych w konsoli
    if args.shell and employees_json:
        logger.info("Wyświetlanie danych w trybie interaktywnym.")
        logger.debug(f"Wyświetlanie danych w trybie interaktywnym. Liczba pracowników: {len(employees_json)}")
        employees_db = db_fetcher.fetch_employee_data_from_url()
        manager = EmployeeManager(employees_json, employees_db)
        employees_json = manager.check_employee_in_db()
        kadra_zarzadcza, kadra_kierownicza, pracownicy = manager.filter_by_position()
        table_display.display_all_groups(kadra_zarzadcza, kadra_kierownicza, pracownicy)

    # Generowanie list w formacie HTML
    if args.generate_training_lists and employees_json:
        logger.info("Generowanie list pracowników w formacie HTML.")
        logger.debug(f"Generowanie list pracowników. Liczba pracowników: {len(employees_json)}")
        employees_db = db_fetcher.fetch_employee_data_from_url()
        manager = EmployeeManager(employees_json, employees_db)
        employees_json = manager.check_employee_in_db()
        kadra_zarzadcza, kadra_kierownicza, pracownicy = manager.filter_by_position()
        list_generator.generate_lists_for_all_groups(kadra_zarzadcza, kadra_kierownicza, pracownicy)

    # Generowanie raportu o stanie szkoleń
    if args.generate_training_report and employees_json:
        logger.info("Generowanie raportu o stanie wyszkolenia pracowników.")
        logger.debug(f"Generowanie list pracowników. Liczba pracowników: {len(employees_json)}")
        employees_db = db_fetcher.fetch_employee_data_from_url()
        manager = EmployeeManager(employees_json, employees_db)
        employees_json = manager.check_employee_in_db()
        report_generator.generate_training_report(employees_json)

    logger.info("Program EduMonitor zakończył działanie.")

if __name__ == '__main__':
    main()