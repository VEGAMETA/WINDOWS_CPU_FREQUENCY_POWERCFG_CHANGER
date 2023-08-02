import utils.wrappers as wrappers
import app
import sys


@wrappers.check_uac
def main() -> None:
    app.run() if "-d" in sys.argv else wrappers.no_debug(app.run)()


if __name__ == "__main__":
    main()
