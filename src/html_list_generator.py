""" src/html_list_generator.py """

import os
from jinja2 import Template
from src.config_loader import ConfigLoader
from src.logger_setup import setup_logger

logger = setup_logger()

class HTMLListGenerator:
    def __init__(self, config_file='config/config.ini'):
        self.config_loader = ConfigLoader(config_file)
        self.lists_dir = self.config_loader.get_output_lists_dir()
        self.templates_dir = 'templates'
        self.employee_list_template = self.load_template('employee_list_template.html')

    def load_template(self, template_name):
        """Ładuje szablon HTML."""
        template_path = os.path.join(self.templates_dir, template_name)
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                template_content = file.read()
            return Template(template_content)
        except FileNotFoundError:
            logger.error(f"Plik szablonu {template_path} nie został znaleziony.")
            return None

    def generate_employee_list(self, group_name, employees):
        """Generuje listę pracowników w formacie HTML dla jednej grupy."""
        if not employees:
            logger.info(f"Brak pracowników w grupie '{group_name}'.")
            return

        if not self.employee_list_template:
            logger.error("Szablon listy pracowników nie został poprawnie załadowany.")
            return

        file_name = f"{group_name.lower().replace(' ', '_')}_lista.html"
        file_path = os.path.join(self.lists_dir, file_name)
        html_content = self.employee_list_template.render(group_name=group_name, employees=employees)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Lista pracowników '{group_name}' zapisana w {file_path}")

    def generate_lists_for_all_groups(self, kadra_zarzadcza, kadra_kierownicza, pracownicy):
        """Generuje listy dla wszystkich grup zawodowych."""
        if kadra_zarzadcza:
            self.generate_employee_list('Kadra Zarządzająca', kadra_zarzadcza)
        if kadra_kierownicza:
            self.generate_employee_list('Kadra Kierownicza', kadra_kierownicza)
        if pracownicy:
            self.generate_employee_list('Pracownicy', pracownicy)