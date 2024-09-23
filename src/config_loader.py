""" src/config_loader.py """

import configparser
import os
import logging

def load_config(config_file='config/config.ini'):
    config = configparser.ConfigParser(interpolation=None)  # Wyłączenie interpolacji
    config.read(config_file)
    return config

def get_log_level_console(config_file='config/config.ini'):
    log_level_env = os.getenv('LOG_LEVEL_CONSOLE')
    if log_level_env:
        return log_level_env.upper()

    config = load_config(config_file)
    try:
        level = config['DEFAULT']['LOG_LEVEL_CONSOLE'].upper()
        log_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return log_levels.get(level, logging.INFO)
    except KeyError:
        return logging.INFO

def get_log_level_file(config_file='config/config.ini'):
    log_level_env = os.getenv('LOG_LEVEL_FILE')
    if log_level_env:
        return log_level_env.upper()

    config = load_config(config_file)
    try:
        level = config['DEFAULT']['LOG_LEVEL_FILE'].upper()
        log_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return log_levels.get(level, logging.INFO)
    except KeyError:
        return logging.INFO

def get_log_file(config_file='config/config.ini'):
    config = load_config(config_file)
    try:
        log_file = config['DEFAULT']['LOG']
        return log_file
    except KeyError:
        return 'logs/app.log'

# Dodajemy brakującą funkcję get_database_url
def get_database_url(config_file='config/config.ini'):
    config = load_config(config_file)
    try:
        url = config['DATABASE']['URL']
        return url
    except KeyError:
        return None

def get_date_format(config_file='config/config.ini'):
    config = load_config(config_file)
    try:
        date_format = config['DEFAULT']['DATE_FORMAT']
        return date_format
    except KeyError:
        return "%d.%m.%Y"  # Domyślny format, jeśli nie znaleziono w konfiguracji
    
def get_ssl_verification_setting(config_file='config/config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    try:
        verify_ssl = config['DATABASE'].getboolean('VERIFY_SSL', True)
        return verify_ssl
    except KeyError:
        return True  # Domyślnie weryfikacja SSL jest włączona

def get_output_lists_dir(config_file='config/config.ini'):
    """
    Pobiera ścieżkę do katalogu na listy HTML z pliku konfiguracyjnego.
    
    Args:
        config_file (str): Ścieżka do pliku konfiguracyjnego.
    
    Returns:
        str: Ścieżka do katalogu na pliki HTML.
    """
    config = load_config(config_file)
    try:
        lists_dir = config['OUTPUT']['LISTS_DIR']
        return lists_dir
    except KeyError:
        return 'output/lists/'  # Domyślna wartość, jeśli brak w pliku config.ini