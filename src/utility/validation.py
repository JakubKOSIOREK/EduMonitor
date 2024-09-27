""" src/utility/validation.py """

from datetime import datetime
from src.logger_setup import setup_logger

def validate_date_format(date_str, date_format="%d.%m.%Y"):
    """
    Sprawdza, czy data jest w poprawnym formacie.
    
    Args:
        date_str (str): Data w formie tekstowej.
        date_format (str): Oczekiwany format daty (domyślnie "%d.%m.%Y").
    
    Returns:
        bool: True, jeśli data jest poprawna, False w przeciwnym razie.
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

def is_past_date(date):
    """
    Sprawdza, czy podana data jest w przeszłości.
    
    Args:
        date (datetime): Obiekt daty do sprawdzenia.
    
    Returns:
        bool: True, jeśli data jest w przeszłości, False w przeciwnym razie.
    """
    return date < datetime.now()

def validate_csv_row_data(data):
    """
    Funkcja waliduje dane wierszy CSV przed zapisem do JSON.
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