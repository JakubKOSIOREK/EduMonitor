""" tests/test_fetch_employee_data_from_url.py """

import unittest
from unittest import mock
from src.db_fetcher import fetch_employee_data_from_url
import urllib3
import json

class TestFetchEmployeeDataFromUrl(unittest.TestCase):

    @mock.patch('src.db_fetcher.urllib3.PoolManager.request')
    def test_fetch_employee_data_success(self, mock_request):
        """Test udanego pobrania danych (200 OK)"""
        # Symulowane dane zwracane przez API
        mock_response_data = json.dumps({
            "users": [
                {"nazwisko": "Nowak", "imie": "Jan", "stanowisko": "Dyrektor", "email": "jan.nowak@example.com"},
                {"nazwisko": "Kowalski", "imie": "Adam", "stanowisko": "Kierownik", "email": "adam.kowalski@example.com"}
            ]
        })
        
        # Mockujemy odpowiedź 200 OK
        mock_request.return_value.status = 200
        mock_request.return_value.data = mock_response_data.encode('utf-8')

        # Wywołujemy funkcję
        url = 'https://example.com/data'
        result = fetch_employee_data_from_url(url)

        # Sprawdzamy, czy funkcja zwraca prawidłowe dane
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['nazwisko'], 'Nowak')
        self.assertEqual(result[1]['imie'], 'Adam')

    @mock.patch('src.db_fetcher.urllib3.PoolManager.request')
    def test_fetch_employee_data_404(self, mock_request):
        """Test błędu 404 Not Found"""
        # Mockujemy odpowiedź 404
        mock_request.return_value.status = 404
        
        # Wywołujemy funkcję
        url = 'https://example.com/data'
        result = fetch_employee_data_from_url(url)

        # Sprawdzamy, czy zwraca pustą listę
        self.assertEqual(result, [])

    @mock.patch('src.db_fetcher.urllib3.PoolManager.request')
    def test_fetch_employee_data_connection_error(self, mock_request):
        """Test błędu połączenia (np. brak internetu)"""
        # Mockujemy wyjątek ConnectionError
        mock_request.side_effect = urllib3.exceptions.ConnectionError

        # Wywołujemy funkcję
        url = 'https://example.com/data'
        result = fetch_employee_data_from_url(url)

        # Sprawdzamy, czy zwraca pustą listę
        self.assertEqual(result, [])

    @mock.patch('src.db_fetcher.ConfigLoader.get_ssl_verification_setting', return_value=False)
    @mock.patch('src.db_fetcher.urllib3.PoolManager.request')
    def test_fetch_employee_data_no_ssl_verification(self, mock_request, mock_ssl_verification):
        """Test braku weryfikacji SSL"""
        # Symulowane dane zwracane przez API
        mock_response_data = json.dumps({
            "users": [
                {"nazwisko": "Nowak", "imie": "Jan", "stanowisko": "Dyrektor", "email": "jan.nowak@example.com"}
            ]
        })
        
        # Mockujemy odpowiedź 200 OK
        mock_request.return_value.status = 200
        mock_request.return_value.data = mock_response_data.encode('utf-8')

        # Wywołujemy funkcję z wyłączoną weryfikacją SSL
        url = 'https://example.com/data'
        result = fetch_employee_data_from_url(url)

        # Sprawdzamy, czy funkcja zwraca prawidłowe dane
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['nazwisko'], 'Nowak')
        mock_ssl_verification.assert_called_once()

if __name__ == '__main__':
    unittest.main()
