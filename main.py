import win32file
from gui.main_window import MainWindow
from utils.hardware import MyComputer
from utils.pipe import connect_pipe
from PySimpleGUI import theme
from sys import argv
from configparser import ConfigParser

if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.ini")
    pipe_name = rf'{config.get("Advanced", "pipe_name")}'
    connect_pipe(pipe_name)
    my_computer = MyComputer()
    frequency = argv[1] if len(argv) > 1 else None
    theme(config.get("Appearance", "Theme"))
    window = MainWindow(my_computer, frequency, pipe_name, config)
