from __future__ import annotations
from typing import TYPE_CHECKING
from gui.tray import Tray
import utils.pipe as pipe
import utils.frequency as freq
import PySimpleGUI as psg
import threading
import time
import sys

if TYPE_CHECKING:
    from configparser import ConfigParser
    from utils.hardware import MyComputer


class MainWindow(psg.Window):
    def __init__(self, computer: MyComputer, frequency: int,
                 pipe_name: str, config: ConfigParser, hidden: bool):
        threading.Thread(target=pipe.create_pipe,
                         args=(pipe_name, self),
                         daemon=True
                         ).start()

        self.frequency = frequency
        self.config = config

        self.computer = computer
        self.cpu_temperature = self.computer.get_str_cpu_temperature()
        self.gpu_temperature = self.computer.get_str_gpu_temperature()

        self.slider = self.get_slider()
        self.set_button = self.get_button()
        self.text = psg.Text(self.get_updated_text())

        super().__init__(
            self.config.get("Advanced", "name"),
            [[self.slider], [self.set_button, self.text]],
            icon=self.config.get("Advanced", "logo"),
            alpha_channel=float(self.config.get("Appearance", "Transparency")),
            grab_anywhere=True,
            enable_close_attempted_event=True,
            finalize=hidden,
        )

        if hidden:
            self.hide()

        threading.Thread(target=self.update_temperature, daemon=True).start()

        self.tray = Tray(self)
        self.event_loop()
        self.tray.close()
        self.close()

    def event_loop(self):
        while True:
            event, values = self.read()
            if event == self.tray.key: event = values[event]
            if event in (None, 'Exit'):
                sys.exit(0)
            elif event == psg.WIN_CLOSE_ATTEMPTED_EVENT:
                self.hide()
            elif event == 'Open':
                self.show_window()
            elif event == psg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
                self.hide() if self.TKroot.winfo_viewable() else self.un_hide()
            elif event.isdigit():
                self.update_frequency(int(values['-TRAY-']))
            else:
                self.update_frequency(int(values["slider"]))

    def show_window(self):
        self.bring_to_front()
        self.un_hide()

    def get_tray_text(self):
        return f"{self.frequency} MHz " \
               f"{self.cpu_temperature} {self.gpu_temperature}"

    def get_updated_text(self):
        return f"Current Frequency is {self.frequency} MHz" \
               f"\t{self.cpu_temperature}\t{self.gpu_temperature}"

    def update_frequency(self, value):
        self.frequency = value
        self.slider.update(value=value)
        freq.set_frequency(value)
        self.tray.set_tooltip(self.get_tray_text())
        self.text.update(self.get_updated_text())

    def update_temperature(self):
        while True:
            time.sleep(1)
            self.cpu_temperature = self.computer.get_str_cpu_temperature()
            self.gpu_temperature = self.computer.get_str_gpu_temperature()
            self.tray.set_tooltip(self.get_tray_text())
            self.text.update(self.get_updated_text())

    def get_slider(self):
        max_frequency = int(self.config.get("CPU", "max_frequency"))
        min_frequency = int(self.config.get("CPU", "min_frequency"))
        slider_step = int(self.config.get("CPU", "slider_step"))
        slider_text_step = int(self.config.get("CPU", "slider_text_step"))
        return psg.Slider((min_frequency, max_frequency), self.frequency,
                          slider_step, slider_text_step, "h", size=(50, 10),
                          key="slider"
                          )

    def get_button(self):
        return psg.Button('Set', button_color=(psg.theme_element_text_color(),
                                               psg.theme_background_color()))
