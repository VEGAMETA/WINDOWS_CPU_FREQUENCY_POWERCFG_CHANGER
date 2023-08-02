import sys
import pyuac


def check_uac(func):
    def running_as_admin(*args, **kwargs):
        if pyuac.isUserAdmin():
            func(*args, **kwargs)
        else:
            pyuac.runAsAdmin()

    return running_as_admin


def no_debug(func):
    def exit_on_exception(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            sys.exit(0)

    return exit_on_exception


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
