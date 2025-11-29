## Скрипт для формирования отчётов

[![python](https://img.shields.io/static/v1?label=python&message=3.9%20|%203.10%20|%203.11|%203.12|%203.13&color=informational)](https://img.shields.io/static/v1?label=python&message=3.9%20|%203.10%20|%203.11|%203.12|%203.13&color=informational)
[![last updated](https://img.shields.io/static/v1?label=last%20updated&message=november%202025&color=yellow)](https://img.shields.io/static/v1?label=last%20updated&message=november%202022&color=yellow)
[![lint](https://img.shields.io/static/v1?label=lint&message=flake8&color=brightgreen)](https://img.shields.io/static/v1?label=lint&message=flake8&color=brightgreen)
[![tests](https://img.shields.io/static/v1?label=tests&message=%E2%9C%94%207%20|%20%E2%9C%98%200&color=critical)](https://img.shields.io/static/v1?label=tests&message=%E2%9C%94%207%20|%20%E2%9C%98%200&color=critical)
[![coverage](https://img.shields.io/badge/coverage-68%25-orange)](https://img.shields.io/badge/coverage-68%25-orange)

### **Описание**

Утилита для построения отчётов по CSV-файлам с использованием SQLite (в памяти). Поддерживает работу с несколькими входными файлами и позволяет добавлять новые отчёты без изменения Python-кода. Принцип работы: скрипт загружает все переданные файлы в SQLite, выполняет SQL-запрос для выбранного отчёта и выводит результат в консоль в виде таблицы. 

### **Как запустить проект:**

Клонировать репозиторий и перейти внутри него:
```
git clone https://github.com/8ubble8uddy/python-report-generator.git
```
Создать и активировать виртуальное окружение
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Установить библиотеки для тестирования и отображения в консоли отчёта
```
pip install pytest pytest-cov tabulate
```
Запустить скрипт
```
python main.py --files data/employees1.csv data/employees2.csv --report performance
```
Чтобы запустить тесты, нужно выполнить следующую команду
```
pytest --cov=lib --cov=main
```

### **Как добавить новый отчёт:**

Чтобы добавить новый отчёт, необходимо:
- Добавить новый блок в файл reports.json с уникальным ключом отчёта.
- Указать SQL-запрос для создания таблицы (ddl) и SQL-запрос для получения отчёта (sql).
- Запустить скрипт с новым значением параметра --report.
- Изменять код проекта при этом не требуется.

### **Кратко об архитектуре**

Проект разделён на независимые модули:
- ReportConfig — отвечает за загрузку и валидацию конфигурации.
- FileLoader — за чтение входных CSV-файлов.
- SQLExecutor — за работу с SQLite.
- main.py — связывает все компоненты в единый конвейер.

### Автор: Герман Сизов
