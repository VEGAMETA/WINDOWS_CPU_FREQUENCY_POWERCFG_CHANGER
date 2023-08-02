import utils.wrappers as wrappers
from app import run
import pyuac
import sys


def check_uac() -> None:
    run() if "-d" in sys.argv else wrappers.no_debug(run)() if pyuac.isUserAdmin() else pyuac.runAsAdmin()


if __name__ == "__main__":
    check_uac()
