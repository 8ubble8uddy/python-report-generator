import csv
import os


class FileLoader:
    SUPPORTED_FORMATS = {'.csv'}

    def load(self, file_path: str):
        ext = os.path.splitext(file_path)[1].lower()

        if ext not in self.SUPPORTED_FORMATS:
            raise RuntimeError(
                f'Данный формат файла не поддерживается: {file_path}'
            )

        return self._load_csv(file_path)

    def _load_csv(self, file_path: str):
        try:
            with open(file_path) as f:
                reader = csv.reader(f)
                headers = next(reader)
                rows = [tuple(row) for row in reader]
            return headers, rows

        except UnicodeDecodeError:
            raise RuntimeError(f'Ошибка в кодировке: {file_path}')
        except StopIteration:
            raise RuntimeError(f'Файл пустой: {file_path}')
        except csv.Error as e:
            raise RuntimeError(
                f'Проблема с разбором CSV-файла {file_path}: {e}')
