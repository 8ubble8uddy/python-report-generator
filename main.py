import argparse
import sqlite3
from tabulate import tabulate

from lib.file_loader import FileLoader
from lib.sql_executor import SQLExecutor
from lib.report_config import ReportConfig
from lib.utils import stage


# ШАГ I
@stage("Загрузка и проверка конфигурации")
def load_config(args):
    config = ReportConfig(
        files=args.files,
        report=args.report,
        config_path=args.config,
    )
    config.run_validators()
    return config.get()


# ШАГ II
@stage('Создание таблицы в SQLite')
def create_table(executor, ddl, report_name):
    executor.create_table(ddl, report_name)


# ШАГ III
@stage('Загрузка данных в SQLite')
def load_data(executor, loader, report_name, files):
    for file in files:
        headers, rows = loader.load(file)
        executor.insert_data(report_name, headers, rows, file)


# ШАГ IV
@stage('Выполнение SQL-запроса отчёта')
def execute_report(executor, sql, report_name):
    return executor.get_report(sql, report_name)


# алгоритм программы
def main():
    # получаем аргументы из CLI
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='*')
    parser.add_argument('--report')
    parser.add_argument('--config', default='reports.json')
    args, _ = parser.parse_known_args()

    # валидируем и получаем параметры для отчёта после валидации
    report_config = load_config(args)

    # инициализируем SQLite в памяти
    conn = sqlite3.connect(':memory:')
    executor = SQLExecutor(conn)
    loader = FileLoader()

    # создаём таблицу для вставки файла в sqlite
    create_table(executor, report_config['ddl'], report_config['report'])

    # загружаем данные из файлов в созданную таблицу
    load_data(
        executor,
        loader,
        report_config['report'],
        report_config['files']
    )

    # выполняем sql-запрос и получаем данные для отчёта
    headers, rows = execute_report(
        executor,
        report_config['sql'],
        report_config['report']
    )

    # выводим отчёт в конслоь
    print(tabulate(rows, headers=headers, floatfmt='.2f'))


if __name__ == '__main__':
    main()
