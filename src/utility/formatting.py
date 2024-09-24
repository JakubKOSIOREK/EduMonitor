""" src/utility/formatting.py """

from datetime import datetime

def format_date(date=None, format_str="%d.%m.%Y"):
    """
    Formatuje obiekt datetime na ciąg tekstowy w podanym formacie.
    
    Args:
        date (datetime or None): Obiekt daty do sformatowania. Jeśli None, używa bieżącej daty.
        format_str (str): Format daty (domyślnie "%d.%m.%Y").
    
    Returns:
        str: Sformatowana data w formie tekstowej.
    
    Raises:
        ValueError: Jeśli obiekt date nie jest typu datetime.
    """
    if date is None:
        date = datetime.now()  # Ustawienie bieżącej daty, jeśli brak daty wejściowej

    if not isinstance(date, datetime):
        raise ValueError(f"Expected a datetime object, got {type(date).__name__}")

    try:
        return date.strftime(format_str)
    except Exception as e:
        raise ValueError(f"Error formatting date: {e}")
