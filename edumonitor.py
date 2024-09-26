""" edumonitor.py """

import os
import json
from src.logger_setup import setup_logger
from src.arg_parser import get_arguments
from src.csv_loader import CSVLoader
from src.config_loader import ConfigLoader
from src.utility.validation import validate_date_format

def main():
    # Ustawienia loggera
    logger = setup_logger()
    logger.info("Program EduMonitor został uruchomiony.")

    # Wczytanie argumentów z linii komend
    args = get_arguments()

    if args.csv:
        csv_path = args.csv
        if not os.path.exists(csv_path):
            logger.error(f"Błąd: Plik CSV {csv_path} nie istnieje.")
            return

        # Wczytanie i filtrowanie pliku CSV (13 kolumn oczekiwanych)
        loader = CSVLoader(csv_path, expected_columns=13)
        filtered_data = loader.load_and_filter_data()

        # Walidacja danych po przefiltrowaniu, przed zapisem do JSON
        if filtered_data and validate_csv_row_data(filtered_data):
            json_data = convert_to_json_structure(filtered_data)
            json_filename = os.path.basename(csv_path).replace('.csv', '.json')
            save_to_json(json_filename, json_data)
        else:
            logger.error("Błąd walidacji danych. Plik nie został zapisany.")

    logger.info("Program EduMonitor zakończył działanie.")

def convert_to_json_structure(filtered_data):
    """
    Funkcja konwertuje przefiltrowane dane CSV do pożądanej struktury JSON.

    Zwraca listę słowników z odpowiednimi kluczami dla kolumn CSV.
    """
    json_data = []
    for row in filtered_data:
        json_data.append({
            "nazwisko": row[1],                 # Kolumna 2
            "imie": row[2],                     # Kolumna 3
            "kod": row[3],                      # Kolumna 4
            "jednostka_organizacyjna": row[4],  # Kolumna 5
            "nazwa_szkolenia": row[7],          # Kolumna 8
            "okres": row[8],                    # Kolumna 9
            "ocena": row[9],                    # Kolumna 10
            "uwagi": row[10]                    # Kolumna 11
        })
    return json_data

def validate_csv_row_data(data):
    """
    Funkcja waliduje dane wierszy CSV przed zapisem do JSON.
    Sprawdza, czy kluczowe pola są niepuste i mają odpowiednie formaty.
    """
    logger = setup_logger()
    for entry in data:
        # Sprawdzenie, czy pola 'nazwisko' i 'imie' nie są puste
        if not entry[1].strip() or not entry[2].strip():
            logger.error(f"Błąd walidacji: Brak nazwiska lub imienia w danych {entry}")
            return False

        # Sprawdzenie formatu daty w polu 'okres'
        if entry[8]:
            try:
                # Rozdzielenie okresu na dwie daty
                start_date, end_date = entry[8].split("...")
                
                # Sprawdzenie formatu każdej daty
                if not validate_date_format(start_date.strip()) or not validate_date_format(end_date.strip()):
                    logger.error(f"Błąd walidacji: Nieprawidłowy format daty w polu 'okres' dla danych {entry}")
                    return False
            except (ValueError, IndexError):
                logger.error(f"Błąd walidacji: Nieprawidłowy format daty w polu 'okres' dla danych {entry}")
                return False

    logger.info("Dane zostały zwalidowane poprawnie.")
    return True

def save_to_json(json_filename, data):
    """Funkcja zapisuje przefiltrowane dane do pliku JSON w katalogu input/."""
    logger = setup_logger()

    # Tworzenie katalogu input/ jeśli nie istnieje
    input_dir = os.path.join(os.getcwd(), 'input')
    os.makedirs(input_dir, exist_ok=True)

    # Generowanie pełnej ścieżki do pliku JSON w katalogu input/
    json_output_path = os.path.join(input_dir, json_filename)

    try:
        with open(json_output_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Plik CSV został zapisany jako JSON w: {json_output_path}")
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas zapisu do JSON: {e}")

if __name__ == '__main__':
    main()