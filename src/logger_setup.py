""" src/logger_setup.py """

import logging
import os
from datetime import datetime
from src.config_loader import get_log_file, get_log_level_console, get_log_level_file

def setup_logger(config_file='config/config.ini'):
    logger = logging.getLogger('EduMonitor')

    # Sprawdzenie, czy logger nie ma już dodanych handlerów
    if not logger.hasHandlers():
        # Pobranie ścieżki do pliku logów z pliku konfiguracyjnego
        log_file = get_log_file(config_file)
        
        # Dodanie timestamp do nazwy pliku
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_with_timestamp = f"{os.path.splitext(log_file)[0]}_{timestamp}.log"

        # Tworzenie katalogu na logi, jeśli nie istnieje
        log_dir = os.path.dirname(log_file_with_timestamp)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Pobranie poziomów logowania dla konsoli i pliku
        log_level_console = get_log_level_console(config_file)
        log_level_file = get_log_level_file(config_file)

        # Ustawienie poziomu logowania na loggerze na minimalny (konsola lub plik)
        logger.setLevel(min(log_level_console, log_level_file))

        # Tworzenie formatera
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Tworzenie konsolowego handlera
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level_console)
        console_handler.setFormatter(formatter)

        # Tworzenie plikowego handlera z kodowaniem UTF-8
        file_handler = logging.FileHandler(log_file_with_timestamp, encoding='utf-8')
        file_handler.setLevel(log_level_file)
        file_handler.setFormatter(formatter)

        # Dodanie handlerów do loggera
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
