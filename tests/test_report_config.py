import json
import pytest
from lib.report_config import ReportConfig


@pytest.fixture
def valid_reports_json(tmp_path):
    data = {
        'performance': {
            'name': 'test',
            'description': 'test',
            'ddl': 'ddl.sql',
            'sql': 'sql.sql'
        }
    }

    path = tmp_path / 'reports.json'
    with open(path, 'w') as f:
        json.dump(data, f)

    return path


def test_valid_report_config(valid_reports_json, tmp_path):
    f = tmp_path / 'data.csv'
    f.write_text('a,b\n1,2')
    cfg = ReportConfig(
        files=[str(f)],
        report='performance',
        config_path=str(valid_reports_json)
    )

    cfg.run_validators()
    result = cfg.get()

    assert result['report'] == 'performance'
    assert result['name'] == 'test'


def test_report_not_found(valid_reports_json):
    cfg = ReportConfig([], 'not_found', str(valid_reports_json))

    with pytest.raises(RuntimeError):
        cfg.run_validators()


def test_missing_files(valid_reports_json):
    cfg = ReportConfig([], 'performance', str(valid_reports_json))

    with pytest.raises(RuntimeError):
        cfg.run_validators()
