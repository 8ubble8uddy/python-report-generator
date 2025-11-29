import pytest
from lib.file_loader import FileLoader


def test_load_valid_csv(tmp_path):
    f = tmp_path / 'data.csv'
    f.write_text('a,b\n1,2\n3,4')

    loader = FileLoader()
    headers, rows = loader.load(str(f))

    assert headers == ['a', 'b']
    assert rows == [('1', '2'), ('3', '4')]


def test_unsupported_extension(tmp_path):
    f = tmp_path / 'bad.txt'
    f.write_text('123')

    loader = FileLoader()

    with pytest.raises(RuntimeError):
        loader.load(str(f))
