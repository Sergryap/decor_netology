from functools import wraps
import datetime as dt
import inspect
import csv
import os


def log_file_path(path, file_name, a=None):
    def log_func(old_func):
        nonlocal a

        @wraps(old_func)
        def new_func(*args, **kwargs):
            nonlocal a
            date = f'{dt.datetime.now()}'
            name = old_func.__name__
            arg = inspect.getfullargspec(old_func).args
            arg = [a for a in arg if a not in kwargs.keys()]
            arg_value = dict(zip(arg, list(args))) | kwargs
            result = old_func(*args, **kwargs)
            result = result if result else "Null"
            log = {
                'name_func': name,
                'args_values': arg_value if a else "Null",
                'date': date,
                'result': result
            }
            log_to_csv(os.path.join(path, file_name), log)
            return result

        return new_func

    return log_func


def log_to_csv(file_csv: str, log: dict):
    """Запись результатов в файл csv"""

    if os.path.isfile(file_csv):
        method = "a"
        book_csv = [list(log.values())]
    else:
        method = "w"
        book_csv = [list(log.keys()), list(log.values())]
    with open(file_csv, f"{method}", encoding="utf-8") as file:
        logwriter = csv.writer(file, delimiter=',')
        logwriter.writerows(book_csv)


@log_file_path("log", "log_file.csv", a=True)
def test_func(x, y, z=5):
    return x ** 2 + y ** 2 + z

@log_file_path("log", "log_file.csv", a=True)
def test_func1(x, y, f, z=5):
    return x ** 2 + y ** 2 + z + f


if __name__ == '__main__':
    test_func(4, 5)
    test_func1(4, 5, 98)
