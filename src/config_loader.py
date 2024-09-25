""" src/config_loader.py """

import configparser
import os
import logging
from src.logger_setup import setup_logger
logger = setup_logger()

class ConfigLoader:
    def __init__(self, config_file='config/config.ini'):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """
        Wczytuje plik konfiguracyjny.
        """
        config = configparser.ConfigParser(interpolation=None)  # Wyłączenie interpolacji
        config.read(self.config_file)
        return config
    
    def validate_config(self):
        """Waliduje, czy plik konfiguracyjny zawiera wymagane sekcje i opcje."""
        required_sections = ['DEFAULT', 'DATABASE', 'OUTPUT']
        for section in required_sections:
            if section not in self.config:
                logger.error(f"Brakuje sekcji {section} w pliku konfiguracyjnym.")
                return False
        return True

    def get(self, section, option, fallback=None):
        """
        Pobiera wartość z pliku konfiguracyjnego dla danego sekcji i opcji.
        """
        return self.config.get(section, option, fallback=fallback)

    def get_log_level_console(self):
        """
        Pobiera poziom logowania dla konsoli z pliku konfiguracyjnego lub zmiennej środowiskowej.
        """
        log_level_env = os.getenv('LOG_LEVEL_CONSOLE')
        if log_level_env:
            return log_level_env.upper()

        level = self.get('DEFAULT', 'LOG_LEVEL_CONSOLE', fallback='INFO').upper()
        return self._map_log_level(level)

    def get_log_level_file(self):
        """
        Pobiera poziom logowania dla plików z pliku konfiguracyjnego lub zmiennej środowiskowej.
        """
        log_level_env = os.getenv('LOG_LEVEL_FILE')
        if log_level_env:
            return log_level_env.upper()

        level = self.get('DEFAULT', 'LOG_LEVEL_FILE', fallback='INFO').upper()
        return self._map_log_level(level)

    def get_log_file(self):
        """
        Pobiera ścieżkę do pliku logów z pliku konfiguracyjnego.
        """
        return self.get('DEFAULT', 'LOG', fallback='logs/app.log')

    def get_database_url(self):
        """
        Pobiera URL bazy danych z pliku konfiguracyjnego.
        """
        return self.get('DATABASE', 'URL', fallback=None)

    def get_date_format(self):
        """
        Pobiera format daty z pliku konfiguracyjnego.
        """
        return self.get('DEFAULT', 'DATE_FORMAT', fallback='%d.%m.%Y')

    def get_ssl_verification_setting(self):
        """
        Pobiera ustawienie weryfikacji SSL z pliku konfiguracyjnego.
        """
        return self.config.getboolean('DATABASE', 'VERIFY_SSL', fallback=True)

    def get_output_lists_dir(self):
        """
        Pobiera ścieżkę do katalogu na listy HTML z pliku konfiguracyjnego.
        """
        return self.get('OUTPUT', 'HTML_LISTS', fallback='output/lists/')

    def get_output_reports_dir(self):
        """
        Pobiera ścieżkę do katalogu na raporty HTML z pliku konfiguracyjnego.
        """
        return self.get('OUTPUT', 'HTML_REPORTS', fallback='output/reports/')

    def _map_log_level(self, level):
        """
        Mapuje poziom logowania z tekstu na poziomy logowania z modułu logging.
        """
        log_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return log_levels.get(level, logging.INFO)
    
    def get_company_name(self):
        """
        Pobiera nazwę firmy z pliku konfiguracyjnego.
        """
        return self.get('DEFAULT', 'COMPANY_NAME', fallback='Example Company')
