""" src/db_fetcher.py"""

from src.config_loader import ConfigLoader
from src.logger_setup import setup_logger
from src.utility.logging_decorator import log_exceptions
import urllib3
import json

logger = setup_logger()

class DBFetcher:
    """
    Klasa odpowiedzialna za pobieranie danych o pracownikach z zewnętrznego URL.
    """

    def __init__(self):
        self.config_loader = ConfigLoader()
        self.verify_ssl = self.config_loader.get_ssl_verification_setting()
        self.url = self.config_loader.get_database_url()
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED' if self.verify_ssl else 'CERT_NONE')
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @log_exceptions(logger)
    def fetch_employee_data_from_url(self):
        """
        Pobiera dane o pracownikach z zewnętrznego URL pobranego z pliku konfiguracyjnego.
        
        Returns:
            list: Lista pracowników pobrana z zewnętrznego API lub pusta lista w przypadku błędu.
        """
        timeout = 10  # 10 sekund na odpowiedź z serwera
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            logger.info(f"Rozpoczęto pobieranie danych z URL: {self.url}")
            response = self.http.request('GET', self.url, headers=headers, timeout=timeout)
            
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
        except urllib3.exceptions.TimeoutError:
            logger.error("Żądanie przekroczyło limit czasu.")
        except urllib3.exceptions.ConnectionError as e:
            logger.error(f"Błąd połączenia: {e}")
        except urllib3.exceptions.HTTPError as e:
            logger.error(f"Błąd HTTP: {e}")
        except Exception as e:
            logger.error(f"Nieoczekiwany błąd: {e}")
        
        return []