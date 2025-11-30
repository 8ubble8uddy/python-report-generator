import sqlite3
from lib.sql_executor import SQLExecutor


def test_full_sql_flow():
    conn = sqlite3.connect(':memory:')
    executor = SQLExecutor(conn)
    ddl = """
        CREATE TABLE table_name (
            position TEXT,
            performance REAL);
    """

    executor.create_table(ddl, 'performance')
    headers = ['position', 'performance']
    rows = [
        ('Dev', 3.0),
        ('Dev', 6.0),
        ('QA', 5.0)
    ]

    executor.insert_data('performance', headers, rows, 'file.csv')
    sql = """
        SELECT position, AVG(performance) as performance
        FROM table_name
        GROUP BY position
        ORDER BY performance DESC;
    """

    headers, result = executor.get_report(sql, 'performance')

    print(result)

    assert headers == ['position', 'performance']
    assert result[0][0] == 'QA'
