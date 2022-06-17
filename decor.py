from functools import wraps
import datetime as dt
import inspect
import csv
import os


def log_file_path(path, file_name):
    def log_func(old_func):
        @wraps(old_func)
        def wraper(*args, **kwargs):
            date = f'{dt.datetime.now()}'
            name = old_func.__name__
            arg = inspect.getfullargspec(old_func).args
            arg = [a for a in arg if a not in kwargs.keys()]
            arg_value = dict(zip(arg, list(args))) | kwargs
            result = old_func(*args, **kwargs)
            log = {
                'name_func': name,
                'args_values': arg_value,
                'date': date,
                'result': result
            }
            log_to_csv(os.path.join(path, file_name), log)
            return result

        return wraper

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


def _folder_creation(base_path, path):
    """
    Создание вложенной папки для директории base_path
    """
    file_path = os.path.join(base_path, path)
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    return file_path
