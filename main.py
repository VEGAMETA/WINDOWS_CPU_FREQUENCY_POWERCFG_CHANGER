from utils.hardware import MyComputer
from configparser import ConfigParser
from gui.window import MainWindow
from PySimpleGUI import theme
import utils.frequency as freq
import utils.pipe as pipe
import sys

if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")

    pipe_name = rf'{config.get("Advanced", "pipe_name")}'
    pipe.kill_if_exists(pipe_name)

    my_computer = MyComputer()
    frequency = int(sys.argv[1], 16) if len(sys.argv) > 1 else freq.get_frequency()

    hidden = bool(sys.argv[2]) if len(sys.argv) > 2 else False

    theme(config.get("Appearance", "Theme"))
    window = MainWindow(my_computer, frequency, pipe_name, config, hidden)
