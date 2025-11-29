import json
import os


class ReportConfig:
    REQUIRED_KEYS = {'name', 'sql', 'ddl'}

    def __init__(self, files: list[str], report: str, config_path: str):
        self.files = files
        self.report_name = report
        self.config_path = config_path

        self.reports = None
        self.report_config = None

    def run_validators(self):
        self._validate_config_file()
        self._load_reports()
        self._validate_report_name()
        self._validate_files()

    def _validate_config_file(self):
        if not self.config_path:
            raise RuntimeError(
                'Параметр --config (конифигурационный файл) не был передан')

        if not os.path.exists(self.config_path):
            raise RuntimeError(
                f'Конфигурационный файл не был найден: {self.config_path}')

        if not self.config_path.lower().endswith('.json'):
            raise RuntimeError('Файл конфигурации должен быть в формате JSON')

    def _load_reports(self):
        with open(self.config_path) as f:
            self.reports = json.load(f)

        if not isinstance(self.reports, dict):
            raise RuntimeError('reports.json должен быть словарём')

        for report_key, report_cfg in self.reports.items():
            missing = self.REQUIRED_KEYS - report_cfg.keys()
            if missing:
                raise RuntimeError(
                    f"В отчёте '{report_key}' нет обязательных ключей: {missing}")  # noqa

    def _validate_report_name(self):
        if not self.report_name:
            raise RuntimeError(
                'Параметр --report (название отчёта) не был передан')

        if self.report_name not in self.reports:
            raise RuntimeError(
                f"Отчёта '{self.report_name}' нет в reports.json")

        self.report_config = self.reports[self.report_name]

    def _validate_files(self):
        if not self.files:
            raise RuntimeError(
                'Параметр --files (список файлов) не был передан')

        for file in self.files:
            if not os.path.exists(file):
                raise RuntimeError(f'Файл не найден: {file}')

            if not file.lower().endswith(".csv"):
                raise RuntimeError(
                    f'Данный формат файла не поддерживается: {file}')

    def get(self):
        return {
            'files': self.files,
            'report': self.report_name,
            'name': self.report_config['name'],
            'description': self.report_config.get('description'),
            'sql': self.report_config['sql'],
            'ddl': self.report_config['ddl'],
        }
