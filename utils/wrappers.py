import sys


def no_debug(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            sys.exit(0)

    return wrapper


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
