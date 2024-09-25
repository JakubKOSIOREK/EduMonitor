""" src/utility/logging_decorator.py """

from functools import wraps
import logging

def log_exceptions(logger=None):
    """
    Dekorator do logowania wyjątków.
    
    Args:
        logger (logging.Logger): Instancja loggera do logowania wyjątków.
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Wyjątek w funkcji {func.__name__}: {e}", exc_info=True)
                raise
        return wrapper
    return decorator