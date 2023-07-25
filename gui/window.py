from __future__ import annotations
from typing import TYPE_CHECKING
from gui.tray import Tray
import utils.pipe as pipe
import utils.frequency as freq
import utils.wrappers as wrappers
import PySimpleGUI as Psg
import threading
import time

if TYPE_CHECKING:
    from configparser import ConfigParser
    from utils.hardware import MyComputer


class MainWindow(Psg.Window):
    def __init__(self, config: ConfigParser, pipe_name: str, computer: MyComputer,
                 frequency: int, hidden: bool, debug: bool) -> None:

        threading.Thread(target=
                         pipe.create_pipe if debug else
                         wrappers.no_debug(pipe.create_pipe),
                         args=(pipe_name, self),
                         daemon=True
                         ).start()

        self.config: ConfigParser = config
        self.computer: MyComputer = computer
        self.frequency: int = frequency

        self.cpu_temperature: str = self.computer.get_str_cpu_temperature()
        self.gpu_temperature: str = self.computer.get_str_gpu_temperature()

        self.slider: Psg.Slider = self.get_slider()
        self.text: Psg.Text = Psg.Text(self.get_updated_text())
        set_button: Psg.Button = Psg.Button('Set', button_color=(
            Psg.theme_element_text_color(),
            Psg.theme_background_color()
        ))

        super().__init__(
            self.config.get("Advanced", "name"),
            [[self.slider], [set_button, self.text]],
            icon=self.config.get("Advanced", "logo"),
            alpha_channel=float(self.config.get("Appearance", "Transparency")),
            grab_anywhere=True,
            finalize=hidden,
            enable_close_attempted_event=True,
        )

        if hidden:
            self.hide()

        threading.Thread(target=
                         self.update_temperature if debug else
                         wrappers.no_debug(self.update_temperature),
                         daemon=True
                         ).start()

        self.tray: Tray = Tray(self)
        self.event_loop()
        self.tray.close()
        self.close()

    def event_loop(self) -> None:
        while True:
            event, values = self.read()
            if event == self.tray.key:
                event = values[event]
            if event in (None, 'Exit'):
                break
            elif event == Psg.WIN_CLOSE_ATTEMPTED_EVENT:
                self.hide()
            elif event == 'Show':
                self.show_window()
            elif event == Psg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
                self.hide() if self.TKroot.winfo_viewable() else self.show_window()
            elif event.isdigit():
                self.update_frequency(int(values['-TRAY-']))
            else:
                self.update_frequency(int(values["slider"]))

    def show_window(self) -> None:
        self.bring_to_front()
        self.un_hide()
        self.TKroot.deiconify()

    def get_tray_tooltip(self) -> str:
        return f"{self.frequency} MHz " \
               f"{self.cpu_temperature} {self.gpu_temperature}"

    def get_updated_text(self) -> str:
        return f"Current Frequency is {self.frequency} MHz" \
               f"\t{self.cpu_temperature}\t{self.gpu_temperature}"

    def update_frequency(self, value: int) -> None:
        self.frequency = value
        self.slider.update(value)
        freq.set_frequency(value)
        self.tray.set_tooltip(self.get_tray_tooltip())
        self.text.update(self.get_updated_text())

    def update_temperature(self) -> None:
        while True:
            time.sleep(1)
            self.cpu_temperature = self.computer.get_str_cpu_temperature()
            self.gpu_temperature = self.computer.get_str_gpu_temperature()
            self.tray.set_tooltip(self.get_tray_tooltip())
            self.text.update(self.get_updated_text())

    def get_slider(self) -> Psg.Slider:
        max_frequency: int = int(self.config.get("CPU", "max_frequency"))
        min_frequency: int = int(self.config.get("CPU", "min_frequency"))
        slider_step: int = int(self.config.get("CPU", "slider_step"))
        slider_text_step: int = int(self.config.get("CPU", "slider_text_step"))
        return Psg.Slider((min_frequency, max_frequency), self.frequency,
                          slider_step, slider_text_step, "h", size=(50, 10),
                          key="slider"
                          )
