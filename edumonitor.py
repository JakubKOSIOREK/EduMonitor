""" edumonitor.py """

import os
from src.logger_setup import setup_logger
from src.arg_parser import get_arguments
from src.csv_loader import CSVLoader
from src.json_loader import JSONLoader
from src.utility.validation import validate_csv_row_data

def main():
    logger = setup_logger()
    logger.info("Program EduMonitor został uruchomiony.")

    # Wczytanie argumentów z linii komend
    args = get_arguments()

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
            # Przetwarzanie i zapis do JSON
            json_loader = JSONLoader()
            json_data = json_loader.convert_to_json_structure(filtered_data)
            json_loader.save_to_json(json_data)
        else:
            logger.error("Błąd walidacji danych. Plik nie został zapisany.")

    logger.info("Program EduMonitor zakończył działanie.")

if __name__ == '__main__':
    main()