""" src/logger_setup.py """

import logging
import configparser
from datetime import datetime
import os

logger = None

def setup_logger(config_file='config/config.ini', section='DEFAULT'):
    logger = logging.getLogger('EduMonitor')

    if logger.hasHandlers():
        return logger

    # Wczytanie konfiguracji
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_file)

    # Pobranie sekcji (DEFAULT lub TEST)
    log_file = config.get(section, 'LOG', fallback='logs/app.log')

    # Dodanie znacznika czasu do pliku logowania
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_with_timestamp = f"{os.path.splitext(log_file)[0]}_{timestamp}.log"

    log_level_console = config.get(section, 'LOG_LEVEL_CONSOLE', fallback='INFO').upper()
    log_level_file = config.get(section, 'LOG_LEVEL_FILE', fallback='INFO').upper()

    logger.setLevel(min(get_log_level(log_level_console), get_log_level(log_level_file)))

    # Dodanie handlerów (plik i konsola)
    file_handler = logging.FileHandler(log_file_with_timestamp, encoding='utf-8')
    console_handler = logging.StreamHandler()

    file_handler.setLevel(get_log_level(log_level_file))
    console_handler.setLevel(get_log_level(log_level_console))

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_log_level(level_str):
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    return levels.get(level_str, logging.INFO)

def close_log_handlers(logger):
    """Zamyka wszystkie uchwyty loggera, aby uniknąć wycieków plików."""
    handlers = logger.handlers[:]
    for handler in handlers:
        try:
            handler.acquire()  # Upewnijmy się, że blokujemy dostęp do uchwytu
            handler.flush()     # Sprawdzamy, czy dane w buforze są zapisane
            handler.close()     # Zamykamy uchwyt
        except Exception as e:
            print(f"Error while closing handler: {e}")
        finally:
            handler.release()  # Zwalniamy uchwyt
            logger.removeHandler(handler)

def reset_logger(logger):
    """Resetuje logger, usuwając wszystkie uchwyty."""
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()
    logger.handlers = []  # Ustawia pustą listę uchwytów
