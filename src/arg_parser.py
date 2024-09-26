""" src/arg_parser.py """

import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description='EduMonitor - wczytaj plik CSV i wyświetl dane.')
    parser.add_argument('--csv', type=str, help='Ścieżka do pliku CSV, który zostanie zapisany jako JSON')
    parser.add_argument('--shell', action='store_true', help='Wyświetlenie wyników w konsoli (tabele)')
    parser.add_argument('--lists-html', action='store_true', help='Generowanie list pracowników w formacie HTML')
    parser.add_argument('--report-html', action='store_true', help='Generowanie raportu o stanie wyszkolenia w formacie HTML')

    return parser.parse_args()