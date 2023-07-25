import sys


def no_debug(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            sys.exit(0)

    return wrapper
