""" tests/test_fetch_employee_data_from_url.py """

import unittest
from unittest import mock
import urllib3
from src.db_fetcher import fetch_employee_data_from_url

class TestFetchEmployeeDataFromUrl(unittest.TestCase):

    @mock.patch('src.db_fetcher.logger')  # Zamockowanie loggera, aby nie wyświetlał komunikatów
    @mock.patch('urllib3.PoolManager.request', return_value=mock.Mock(status=404))  # Symulujemy status 404
    def test_fetch_data_url_not_found(self, mock_request, mock_logger):
        """Test dla sytuacji, gdy URL zwraca 404"""
        url = "http://example.com"
        result = fetch_employee_data_from_url(url)
        
        # Sprawdzamy, czy funkcja zwróciła pustą listę
        self.assertEqual(result, [])
        
        # Upewniamy się, że odpowiedni komunikat został zalogowany, ale nie wyświetlony
        mock_logger.error.assert_called_with("Błąd: URL nie został znaleziony (404).")
    
    @mock.patch('src.db_fetcher.logger')  # Zamockowanie loggera
    @mock.patch('urllib3.PoolManager.request', side_effect=urllib3.exceptions.ConnectionError)  # Symulujemy błąd połączenia
    def test_fetch_data_connection_error(self, mock_request, mock_logger):
        """Test dla sytuacji, gdy połączenie nie może zostać nawiązane"""
        url = "http://example.com"
        result = fetch_employee_data_from_url(url)
        
        # Sprawdzamy, czy funkcja zwróciła pustą listę
        self.assertEqual(result, [])
        
        # Sprawdzamy, czy odpowiedni komunikat został zalogowany
        mock_logger.error.assert_called_with("Błąd połączenia: ")

    @mock.patch('src.db_fetcher.logger')  # Zamockowanie loggera
    @mock.patch('urllib3.PoolManager.request', return_value=mock.Mock(status=200, data=b'{"users": []}'))  # Symulujemy poprawną odpowiedź
    def test_fetch_data_success(self, mock_request, mock_logger):
        """Test dla poprawnej odpowiedzi serwera z pustą listą użytkowników"""
        url = "http://example.com"
        result = fetch_employee_data_from_url(url)
        
        # Sprawdzamy, czy funkcja zwróciła pustą listę
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
