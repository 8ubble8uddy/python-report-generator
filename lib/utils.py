import sys
import traceback


def stage(name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"""
                    Произошла ошибка на этапе "{name}".
                    Текст ошибки: {e}
                """)

                tb = traceback.extract_tb(e.__traceback__)
                if tb:
                    last = tb[-1]
                    print(f"""
                        Конкретное место ошибки:
                        Файл {last.filename}
                        Строка {last.lineno}
                    """)

                sys.exit(1)

        return wrapper
    return decorator
