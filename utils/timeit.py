import time
from datetime import datetime
import pytz
from utils.config import Config


config = Config()


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        return result, duration
    return wrapper


def current_data_time() -> str:
    time_zone = pytz.timezone(config.get_time_zone())
    now = datetime.now(tz=time_zone)
    current_datatime = '%Y-%m-%d %H:%M:%S %Z%z'
    current_datatime = now.strftime(f'{current_datatime} ({time_zone})')
    return current_datatime
