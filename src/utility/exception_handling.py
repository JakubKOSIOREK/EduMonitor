""" src/utility/exception_handling.py """

from functools import wraps
import logging

def handle_exception(logger=None):
    """
    Dekorator, który loguje wyjątki, a następnie je podnosi, aby aplikacja mogła dalej działać.
    Args:
        logger (logging.Logger): Instancja loggera. Jeśli brak, używa domyślnego loggera.
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Błąd w funkcji {func.__name__}: {str(e)}", exc_info=True)
                raise
        return wrapper
    return decorator