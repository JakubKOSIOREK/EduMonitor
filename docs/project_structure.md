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
├── templates/
│   └── employee_list_template.html
├── tests/
│   ├── test_check_employee_in_db.py
│   ├── test_filter_file.py
│   ├── test_is_expired.py
│   ├── test_is_soon_expiring.py
│   └── test_load_file.py
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
