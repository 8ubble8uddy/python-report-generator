import os
import sqlite3


class SQLExecutor:
    TABLE_NAME = 'table_name'

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection

    def read_sql(self, sql_or_path: str) -> str:
        if not sql_or_path:
            raise RuntimeError('SQL-запрос пустой')

        if os.path.exists(sql_or_path):
            with open(sql_or_path) as f:
                return f.read()

        return sql_or_path

    def create_table(self, ddl: str, report_name: str):
        try:
            ddl_sql = self.read_sql(ddl)
            self.conn.executescript(ddl_sql)

            if not self._check_table_exists():
                raise ValueError("Название таблицы в параметре 'ddl' должно быть только 'table_name'")

        except sqlite3.Error as e:
            raise RuntimeError(f"""
                Произошла ошибка при создании таблицы для отчёта '{report_name}'.
                Ошибка SQLite: {e}
                Проверь параметр 'ddl' в reports.json""") # noqa

    def insert_data(self, report_name: str, headers: list[str], rows: list[tuple], file_name: str):  # noqa
        try:
            pholders = ','.join(['?'] * len(headers))
            columns = ','.join(headers)
            sql = f'INSERT INTO {self.TABLE_NAME} ({columns}) VALUES ({pholders})'
            self.conn.executemany(sql, rows)
            self.conn.commit()

        except sqlite3.Error as e:
            raise RuntimeError(f"""
                Произошла ошибка при обработке файла '{file_name}' для отчёта '{report_name}'.
                Ошибка SQLite: {e}
                Проверь соответствие данных структуре таблицы""")

    def get_report(self, sql: str, report_name: str):
        try:
            query = self.read_sql(sql)
            cursor = self.conn.cursor()
            cursor.execute(query)
            headers = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            return headers, rows

        except sqlite3.Error as e:
            raise RuntimeError(f"""
                'Произошла ошибка при выполнении запроса' для отчёта '{report_name}'.
                Ошибка SQLite: {e}'
                Проверь параметр 'sql' в reports.json""")  # noqa
        
    def _check_table_exists(self):
        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.TABLE_NAME}'"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
