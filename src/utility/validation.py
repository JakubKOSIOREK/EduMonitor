""" src/utility/validation.py """

from datetime import datetime

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