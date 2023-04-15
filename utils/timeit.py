import time
from datetime import datetime


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        return result, duration
    return wrapper


def current_data_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")