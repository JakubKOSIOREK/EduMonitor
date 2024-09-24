""" src/html_generator.py """

import os
import locale
from jinja2 import Template
from src.logger_setup import setup_logger
from src.config_loader import get_output_lists_dir
from datetime import datetime

# Ustawiamy lokalizację na polską
locale.setlocale(locale.LC_COLLATE, 'pl_PL.UTF-8')

logger = setup_logger()
employee_list_template = "templates/employee_list_template.html"
company_report_template = "templates/employee_report_template.html"

def load_template(template_path):
    """
    Wczytuje szablon HTML z pliku.
    
    Args:
        template_path (str): Ścieżka do pliku szablonu.
    
    Returns:
        Template: Obiekt Jinja2 Template.
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()
        return Template(template_content)
    except FileNotFoundError:
        logger.error(f"Plik szablonu {template_path} nie został znaleziony.")
        return None

def generate_html_file(group_name, employees, config_file='config/config.ini'):
    output_dir = get_output_lists_dir(config_file)
    logger.info(f"Ścieżka katalogu wyjściowego: {output_dir}")
    
    if not employees:
        logger.info(f"Lista pracowników dla grupy '{group_name}' jest pusta. Nie generuję pliku HTML.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Utworzono katalog: {output_dir}")

    file_name = f"{group_name.lower().replace(' ', '_')}_lista_na_szkolenie.html"
    file_path = os.path.join(output_dir, file_name)

    template = load_template(employee_list_template)
    if template is None:
        logger.error(f"Nie załadowano szablonu z {employee_list_template}.")
        return  # Nie generujemy pliku, jeśli nie załadowano szablonu
    
    html_content = template.render(group_name=group_name, employees=employees)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        logger.info(f"Utworzono plik HTML: '{file_path}'")

def generate_training_report_html(employees, config_file):
    # Przykładowy kod do tworzenia raportu o stanie wyszkolenia
    output_dir = get_output_lists_dir(config_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"raport_stanu_wyszkolenia_{timestamp}.html"
    file_path = os.path.join(output_dir, file_name)

    # Przykładowa struktura raportu
    valid_training = [emp for emp in employees if emp.is_valid_training()]
    soon_expiring = [emp for emp in employees if emp.is_soon_expiring()]
    expired = [emp for emp in employees if emp.is_expired()]

    # Wczytanie szablonu
    template = load_template(company_report_template)
    if not template:
        return

    html_content = template.render(
        valid_training=len(valid_training),
        soon_expiring=len(soon_expiring),
        expired=len(expired),
        employees=employees,
        current_date=datetime.now().strftime("%d.%m.%Y")
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        logger.info(f"Raport HTML wygenerowany: {file_path}")