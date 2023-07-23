from utils.hardware import MyComputer
from configparser import ConfigParser
from gui.window import MainWindow
from PySimpleGUI import theme
import utils.frequency as freq
import utils.pipe as pipe
import sys

if __name__ == "__main__":
    config: ConfigParser = ConfigParser()
    config.read("config.ini")

    pipe_name: str = rf'{config.get("Advanced", "pipe_name")}'
    pipe.kill_if_exists(pipe_name)

    my_computer: MyComputer = MyComputer()
    frequency: int = int(sys.argv[1], 16) if len(sys.argv) > 1 else freq.get_frequency()

    hidden: bool = bool(sys.argv[2]) if len(sys.argv) > 2 else False

    theme(config.get("Appearance", "Theme"))
    window: MainWindow = MainWindow(my_computer, frequency, pipe_name, config, hidden)
