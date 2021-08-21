from functools import wraps
from time import time


def timeit(func):
    """A simple timer decorator (PyBites tips book)"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        elapsed = time() - start_time
        print(f'Elapsed time {func.__name__}: {elapsed}')
        return result
    return wrapper
