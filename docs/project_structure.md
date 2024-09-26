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
├── input/
├── logs/
├── outputs/
|   ├── lists/
|   └── reports/
├── src/
|   ├── utility/
|   |   ├── exceptioon_handling.py
|   |   ├── formatting.py
|   |   ├── logging_decorator.py
|   |   └── validation.py
|   ├── config_loader.py
|   ├── csv_loader.py
|   ├── db_fetcher.py
|   ├── employee_management.py
|   ├── employee.py
|   ├── logger_setup.py
|   └── table_display.py
├── templates/
│   └── employee_list_template.html
│   └── employee_report_template.html
├── tests/
|   ├── test_files/
|   |   └── dane_testowe.csv
|   ├── test_CSVLoader.py
|   ├── test_EmployeeManager.py
|   ├── test_fetch_employee_data_from_url.py
|   ├── test_HTMLReportGenerator.py
|   ├── test_TestEduMonitor.py
|   └── test_TestTableDisplay.py
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
