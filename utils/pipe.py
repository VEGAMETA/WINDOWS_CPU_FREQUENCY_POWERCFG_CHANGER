from __future__ import annotations
from typing import TYPE_CHECKING
import pywintypes
import win32pipe
import win32file
import os

if TYPE_CHECKING:
    from gui.window import MainWindow


def create_pipe(pipe_name: str, window: MainWindow) -> None:
    pipe = win32pipe.CreateNamedPipe(pipe_name,
                                     win32pipe.PIPE_ACCESS_DUPLEX,
                                     win32pipe.PIPE_TYPE_MESSAGE |
                                     win32pipe.PIPE_READMODE_MESSAGE |
                                     win32pipe.PIPE_WAIT,
                                     1, 0, 0, 0, None
                                     )
    while True:
        win32pipe.ConnectNamedPipe(pipe, None)
        win32pipe.DisconnectNamedPipe(pipe)
        window.show_window()


def connect_pipe(pipe_name: str) -> None:
    win32file.CreateFile(pipe_name, win32file.GENERIC_READ, 0, None,
                         win32file.OPEN_EXISTING, 0, None
                         )


def kill_if_exists(pipe_name: str) -> None:
    try:
        connect_pipe(pipe_name)
        os.kill(os.getpid(), 2)  # 2 is signal.SIGINT (ctrl+c)
    except pywintypes.error:
        pass
