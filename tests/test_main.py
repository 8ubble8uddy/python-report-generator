import json
import subprocess
import sys



# flake8: noqa
def test_full_cli_run(tmp_path):
    csv = tmp_path / 'employees.csv'
    csv.write_text(
        'name,position,completed_tasks,performance,skills,team,experience_years\n'
        'Alex Ivanov,Backend Developer,45,4.8,"Python, Django, PostgreSQL, Docker",API Team,5\n'
        'Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4\n' 
        'John Smith,Data Scientist,29,4.6,"Python, ML, SQL, Pandas",AI Team,3\n'
        'Anna Lee,DevOps Engineer,52,4.9,"AWS, Kubernetes, Terraform, Ansible",Infrastructure Team,6\n'
        'Mike Brown,QA Engineer,41,4.5,"Selenium, Jest, Cypress, Postman",Testing Team,4\n'
    )

    ddl = tmp_path / 'ddl.sql'
    ddl.write_text("""
        CREATE TABLE table_name (
            name TEXT,
            position TEXT,
            completed_tasks INTEGER,
            performance REAL,
            skills TEXT,
            team TEXT,
            experience_years INTEGER);
    """)

    sql = tmp_path / 'report.sql'
    sql.write_text("""
        SELECT position, AVG(performance) as performance
        FROM table_name
        GROUP BY position
        ORDER BY performance DESC;
    """)

    config = {
        'performance': {
            'name': 'Test',
            "description": 'Test',
            'ddl': str(ddl),
            'sql': str(sql)
        }
    }
    cfg = tmp_path / 'reports.json'
    with open(cfg, 'w') as file:
        json.dump(config, file)

    result = subprocess.run(
        [sys.executable, 'main.py', '--files', str(csv), '--report', 'performance', '--config', str(cfg)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert 'Dev' in result.stdout
