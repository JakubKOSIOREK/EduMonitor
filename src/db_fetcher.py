""" src/db_fetcher.py"""

import urllib3
import json
from src.config_loader import ConfigLoader
from src.logger_setup import setup_logger
from src.utility.logging_decorator import log_exceptions
logger = setup_logger()

@log_exceptions(logger)
def fetch_employee_data_from_url(url):
    """
    Pobiera dane o pracownikach z zewnętrznego URL.
    
    Args:
        url (str): URL do pobrania danych.
    
    Returns:
        list: Lista pracowników pobrana z zewnętrznego API.
    """
    # Pobieramy ustawienie weryfikacji SSL z pliku konfiguracyjnego
    config_loader = ConfigLoader()
    verify_ssl = config_loader.get_ssl_verification_setting()
    timeout = 10  # 10 sekund na odpowiedź z serwera

    # Konfiguracja PoolManager z opcją weryfikacji SSL
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED' if verify_ssl else 'CERT_NONE')

    if not verify_ssl:
        # Wyłączenie ostrzeżeń związanych z brakiem weryfikacji SSL
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        logger.info(f"Rozpoczęto pobieranie danych z URL: {url}")
        response = http.request('GET', url, headers=headers, timeout=timeout)
        
        # Obsługa statusu HTTP
        if response.status == 200:
            raw_data = json.loads(response.data.decode('utf-8'))
            clean_data = raw_data.get("users", [])  # Wyciągamy dane pracowników
            logger.info(f"Pobrano {len(clean_data)} rekordów pracowników z bazy danych.")
            return clean_data
        elif response.status == 404:
            logger.error(f"Błąd: URL nie został znaleziony (404).")
        elif response.status == 500:
            logger.error(f"Błąd: Problem z serwerem (500).")
        else:
            logger.error(f"Błąd: Otrzymano status {response.status}")
            return []
    
    # Obsługa różnych wyjątków
    except urllib3.exceptions.TimeoutError:
        logger.error("Żądanie przekroczyło limit czasu.")
        return []
    except urllib3.exceptions.ConnectionError as e:
        logger.error(f"Błąd połączenia: {e}")
        return []
    except urllib3.exceptions.HTTPError as e:
        logger.error(f"Błąd HTTP: {e}")
        return []
    except Exception as e:
        logger.error(f"Nieoczekiwany błąd: {e}")
        return []
