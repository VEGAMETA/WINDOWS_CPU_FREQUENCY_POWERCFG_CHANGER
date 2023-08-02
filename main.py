import utils.wrappers as wrappers
from app import run
import sys


@wrappers.check_uac
def main() -> None:
    run() if "-d" in sys.argv else wrappers.no_debug(run)()


if __name__ == "__main__":
    main()
