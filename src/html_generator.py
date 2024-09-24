""" src/html_generator.py """

import os
from jinja2 import Template
from src.config_loader import ConfigLoader
from datetime import datetime
from src.utility.formatting import format_date
from src.logger_setup import setup_logger
from src.utility.logging_decorator import log_exceptions
logger = setup_logger()

class HTMLReportGenerator:
    def __init__(self, config_file='config/config.ini'):
        self.config_loader = ConfigLoader(config_file)
        self.output_dir = self.config_loader.get_output_lists_dir()
        self.templates_dir = 'templates'
        self.employee_list_template = self.load_template('employee_list_template.html')
        self.company_report_template = self.load_template('employee_report_template.html')

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

    @log_exceptions(logger)
    def generate_employee_list(self, group_name, employees):
        """Generuje listę pracowników w formacie HTML."""
        if not employees:
            logger.info(f"Brak pracowników w grupie '{group_name}'.")
            return

        if not self.employee_list_template:
            logger.error("Szablon listy pracowników nie został poprawnie załadowany.")
            return

        file_name = f"{group_name.lower().replace(' ', '_')}_lista.html"
        file_path = os.path.join(self.output_dir, file_name)
        html_content = self.employee_list_template.render(group_name=group_name, employees=employees)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Lista pracowników '{group_name}' zapisana w {file_path}")

    def _get_training_summary(self, employees):
        """Zwraca podsumowanie liczby pracowników z różnym statusem szkoleń."""
        valid_training = [emp for emp in employees if emp.is_valid_training]
        soon_expiring = [emp for emp in employees if emp.is_soon_expiring]
        expired = [emp for emp in employees if emp.is_expired]
        return valid_training, soon_expiring, expired

    @log_exceptions(logger)
    def generate_training_report(self, employees):
        """Generuje raport HTML o stanie szkoleń."""
        valid_training, soon_expiring, expired = self._get_training_summary(employees)

        current_date = format_date(datetime.now(), "%d.%m.%Y")

        file_name = f"raport_wyszkolenia_{datetime.now().strftime('%Y-%m-%d')}.html"
        file_path = os.path.join(self.output_dir, file_name)
        html_content = self.company_report_template.render(
            valid_training=len(valid_training),
            soon_expiring=len(soon_expiring),
            expired=len(expired),
            employees=employees,
            current_date=current_date
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Raport HTML wygenerowany: {file_path}")