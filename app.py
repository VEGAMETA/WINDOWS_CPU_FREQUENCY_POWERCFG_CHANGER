from utils.hardware import MyComputer
from configparser import ConfigParser
from gui.window import MainWindow
from PySimpleGUI import theme
import utils.frequency as freq
import utils.pipe as pipe
import sys


def run() -> None:
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
