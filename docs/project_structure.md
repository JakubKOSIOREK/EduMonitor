<!--edumonitor/docs/project_structure.md-->

```
edumonitor/
├── config/
|   ├── config.ini              # Główny plik konfiguracyjny
│   └── config_example.ini      # Przykładowy plik konfiguracyjny
├── docs/
|   ├── data_flow.md
|   ├── data_flow.pdf
|   ├── project_structure.md    # Struktura projektu
|   └── project_structure.pdf
├── logs/
├── src/
|   ├── config_loader.py        # Funkcje ładowania konfiguracji
|   ├── csv_loader.py           # Funkcje wczytywania i filtrowania plików CSV
|   ├── db_fetcher.py           # Pobieranie danych o pracownikach z URL
|   ├── employee_class.py       # Klasa Employee i metody do zarządzania pracownikami
|   ├── logger_setup.py         # Konfiguracja loggera
|   └── table_display.py        # Generowanie i wyświetlanie tabel na konsoli
├── tests/
│   ├── test_csv_loader.py        # Testy dla csv_loader
│   ├── test_employee_checker.py  # Testy dla employee_checker
│   └── test_db_fetcher.py        # Testy dla db_fetcher
├── tmp/
├── edumonitor.py
├── CHANGELOG.md
├── CHANGELOG.pdf
├── edumonitor.py
├── LICENCE.md
├── LICENCE.pdf
├── README.md
└── README.pdf
```
