<!--edumonitor/docs/project_structure.md-->

```
edumonitor/
├── config/
|   └── config.ini              # Główny plik konfiguracyjny
├── docs/
|   ├── data_flow.md
|   └── project_structure.md    # Struktura projektu
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
|   ├── arg_parser.py
|   ├── config_loader.py
|   ├── csv_loader.py
|   ├── db_fetcher.py
|   ├── employee_management.py
|   ├── employee.py
|   ├── html_generator.py
|   ├── json_loader.py
|   ├── logger_setup.py
|   └── table_display.py
├── templates/
│   └── employee_list_template.html
│   └── employee_report_template.html
├── tests/
├── tmp/
├── edumonitor.py
├── CHANGELOG.md
├── edumonitor.py
├── LICENCE.md
└── README.md
```
