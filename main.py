from utils.hardware import MyComputer
from configparser import ConfigParser
from gui.window import MainWindow
from PySimpleGUI import theme
import utils.wrappers as wrappers
import utils.frequency as freq
import utils.pipe as pipe
import pyuac
import sys


def main() -> None:
    config: ConfigParser = ConfigParser()
    config.read("config.ini")

    pipe_name: str = rf'{config.get("Advanced", "pipe_name")}'
    pipe.kill_if_exists(pipe_name)

    my_computer: MyComputer = MyComputer()

    frequency: int = freq.get_frequency()
    hidden: bool = "-h" in sys.argv
    debug: bool = "-d" in sys.argv

    theme(config.get("Appearance", "Theme"))
    MainWindow(config, pipe_name, my_computer, frequency, hidden, debug)


def check_uac():
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        main() if "-d" in sys.argv else wrappers.no_debug(main)()


if __name__ == "__main__":
    check_uac()
