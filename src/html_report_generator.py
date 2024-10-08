""" src/html_report_generator.py """

import os
from jinja2 import Template
from datetime import datetime
from src.logger_setup import setup_logger
from src.config_loader import ConfigLoader
from src.employee_management import EmployeeManager
from src.utility.formatting import format_date

logger = setup_logger()

class HTMLReportGenerator:
    def __init__(self, config_file='config/config.ini'):
        self.config_loader = ConfigLoader(config_file)
        self.reports_dir = self.config_loader.get_output_reports_dir()  # Path for reports
        self.templates_dir = 'templates'
        self.company_report_template = self.load_template('employee_report_template.html')

    def load_template(self, template_name):
        """Loads the HTML template."""
        template_path = os.path.join(self.templates_dir, template_name)
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                template_content = file.read()
            return Template(template_content)
        except FileNotFoundError:
            logger.error(f"Template file {template_path} not found.")
            return None

    def _get_training_summary(self, employees):
        """Returns a summary of employees with different training statuses."""
        valid_training = [emp for emp in employees if emp.is_valid_training]
        soon_expiring = [emp for emp in employees if emp.is_soon_expiring]
        expired = [emp for emp in employees if emp.is_expired]
        return valid_training, soon_expiring, expired

    def generate_training_report(self, employees):
        """Generates an HTML report about training statuses."""

        company_name = self.config_loader.get_company_name()
        valid_training, soon_expiring, expired = self._get_training_summary(employees)
        total_employees = len(employees)

        # Obliczanie procentów dla wszystkich pracowników
        valid_percentage = round(len(valid_training) / total_employees * 100) if total_employees > 0 else 0
        soon_expiring_percentage = round(len(soon_expiring) / total_employees * 100) if total_employees > 0 else 0
        expired_percentage = round(len(expired) / total_employees * 100) if total_employees > 0 else 0

        manager = EmployeeManager(employees, [])
        kadra_zarzadcza, kadra_kierownicza, pracownicy = manager.filter_by_position()

        # Liczenie pracowników w każdej grupie
        def group_summary(group, total_in_group):
            valid, soon_expiring, expired = self._get_training_summary(group)
            return {
                "valid": len(valid),
                "soon_expiring": len(soon_expiring),
                "expired": len(expired),
                "valid_percentage": round(len(valid) / total_in_group * 100) if total_in_group > 0 else 0,
                "soon_expiring_percentage": round(len(soon_expiring) / total_in_group * 100) if total_in_group > 0 else 0,
                "expired_percentage": round(len(expired) / total_in_group * 100) if total_in_group > 0 else 0
            }
        
        kadra_zarzadcza_summary = group_summary(kadra_zarzadcza, len(kadra_zarzadcza))
        kadra_kierownicza_summary = group_summary(kadra_kierownicza, len(kadra_kierownicza))
        pracownicy_summary = group_summary(pracownicy, len(pracownicy))

        current_date = format_date(datetime.now(), "%d.%m.%Y")

        file_name = f"raport_wyszkolenia_{datetime.now().strftime('%Y-%m-%d')}.html"
        file_path = os.path.join(self.reports_dir, file_name)

        html_content = self.company_report_template.render(
            valid_training=len(valid_training),
            soon_expiring=len(soon_expiring),
            expired=len(expired),
            valid_percentage=valid_percentage,
            soon_expiring_percentage=soon_expiring_percentage,
            expired_percentage=expired_percentage,
            total_employees=total_employees,
            current_date=current_date,
            company_name=company_name,
            kadra_zarzadcza_summary=kadra_zarzadcza_summary,
            kadra_kierownicza_summary=kadra_kierownicza_summary,
            pracownicy_summary=pracownicy_summary,
            kadra_zarzadcza_count=len(kadra_zarzadcza),
            kadra_kierownicza_count=len(kadra_kierownicza),
            pracownicy_count=len(pracownicy)
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"Generated training report: {file_path}")
