import win32pipe
import win32file
import pywintypes
from os import getpid
from os import kill
from signal import SIGINT

def create_pipe(pipe_name, widnow):
    pipe = win32pipe.CreateNamedPipe(pipe_name, win32pipe.PIPE_ACCESS_DUPLEX, win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT, 1, 0, 0, 0, None)
    while True:
        win32pipe.ConnectNamedPipe(pipe, None)
        win32pipe.DisconnectNamedPipe(pipe)
        widnow.bring_to_front()
        if not widnow.visible:
            widnow.un_hide()

def connect_pipe(pipe_name):
    try:
        win32file.CreateFile(pipe_name, win32file.GENERIC_READ, 0, None, win32file.OPEN_EXISTING, 0, None)
        kill(getpid(), SIGINT)
    except pywintypes.error: ...
