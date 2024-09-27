""" src/arg_parser.py """

import argparse
import os
from src.csv_loader import CSVLoader
from src.logger_setup import setup_logger
from src.utility.validation import validate_csv_row_data

logger = setup_logger()
def get_arguments():
    parser = argparse.ArgumentParser(description='EduMonitor - wczytaj plik CSV i wyświetl dane.')
    parser.add_argument('--csv', type=str, help='Ścieżka do pliku CSV, który zostanie zapisany jako JSON')
    parser.add_argument('--shell', action='store_true', help='Wyświetlenie wyników w konsoli (tabele)')
    parser.add_argument('--generate-training-lists', action='store_true', help='Generowanie listy pracowników na szkolenia w formacie HTML')
    parser.add_argument('--generate-training-report', action='store_true', help='Generowanie raportu o stanie wyszkolenia pracowników')

    return parser.parse_args()

def process_csv_argument(csv_path):
    """
    Przetwarza i waliduje plik CSV podany przez użytkownika.
    Zwraca listę przefiltrowanych danych lub None w przypadku błędów.
    """
    if not os.path.exists(csv_path):
        logger.error(f"Błąd: Plik CSV {csv_path} nie istnieje.")
        return None

    # Wczytanie i filtrowanie pliku CSV
    loader = CSVLoader(csv_path, expected_columns=13)
    filtered_data = loader.load_and_filter_data()

    # Walidacja danych
    if filtered_data and validate_csv_row_data(filtered_data):
        return filtered_data
    else:
        logger.error("Błąd walidacji danych. Plik nie został zapisany.")
        return None