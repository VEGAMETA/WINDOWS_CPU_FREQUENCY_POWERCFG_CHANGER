import subprocess
import threading
import time
import sys
import PySimpleGUI as sg
from psgtray import SystemTray
from utils.pipe import create_pipe


class MainWindow(sg.Window):
    def __init__(self, computer, frequency, pipe_name, config):
        threading.Thread(target=create_pipe, args=(pipe_name, self), daemon=True).start()

        self.computer = computer
        self.frequency = self.get_frequency(frequency)
        self.set_cpu_and_gpu_temperature(computer)
        self.slider = self.get_slider(config)
        set_button = self.get_button()
        self.text = sg.Text(self.get_updated_text())

        super().__init__(
            config.get("Advanced", "name"),
            [[self.slider], [set_button, self.text]],
            icon=config.get("Advanced", "logo"),
            alpha_channel=float(config.get("Appearance", "Transparency")),
            grab_anywhere=True,
            enable_close_attempted_event=True
        )

        fast_set_list = config.get("CPU", "fast_set_list").split(", ")
        tray_menu = ['', ['Open', "Set", fast_set_list, '---', 'Exit']]
        self.tray = SystemTray(
            tray_menu,
            single_click_events=False,
            window=self,
            tooltip=self.get_tray_text(),
            icon=config.get("Advanced", "logo_tray")
        )

        threading.Thread(target=self.update_temperature, args=(computer,), daemon=True).start()
        self.visible = True
        self.event_loop()
        self.tray.close()
        self.close

    def event_loop(self):
        while True:
            event, values = self.read()
            if event == self.tray.key: event = values[event]
            if event in (None, 'Exit'): sys.exit(0)
            elif event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
                self.hide()
                self.visible = False
            elif event == 'Open':
                self.un_hide()
                self.bring_to_front()
                self.visible = True
            elif event == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
                self.hide() if self.visible else self.un_hide()
                self.visible = not self.visible
            elif isinstance(event, str) and event.isdigit(): self.update_frequency(int(values['-TRAY-']))
            else: self.update_frequency(int(values["slider"]))

    def update_frequency(self, value):
        self.frequency = value
        self.slider.update(value=value)
        commands = (
            f"powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX {self.frequency}",
            f"powercfg /setdcvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX {self.frequency}",
            "powercfg /S SCHEME_CURRENT"
        )
        subprocess.run(" && ".join(commands), shell=True)
        self.tray.set_tooltip(self.get_tray_text())
        self.text.update(self.get_updated_text())

    def update_temperature(self, computer):
        while True:
            time.sleep(1)
            self.set_cpu_and_gpu_temperature(computer)
            self.tray.set_tooltip(self.get_tray_text())
            self.text.update(self.get_updated_text())

    def set_cpu_and_gpu_temperature(self, computer):
        self.cpu_temperature = "CPU - " + computer.get_cpu_temperature() + "°C"
        self.gpu_temperature = "GPU - " + computer.get_gpu_temperature() + "°C"

    def get_frequency(self, value):
        if value:
            return int(value, 16)
        else:
            return int(subprocess.Popen('powercfg /query SCHEME_CURRENT SUB_PROCESSOR PROCFREQMAX', stdout=subprocess.PIPE).stdout.read()[-12:-4], 16)

    def get_slider(self, config):
        max_frequency = int(config.get("CPU", "max_frequency"))
        min_frequency = int(config.get("CPU", "min_frequency"))
        slider_step = int(config.get("CPU", "slider_step"))
        slider_text_step = int(config.get("CPU", "slider_text_step"))
        return sg.Slider((min_frequency, max_frequency), self.frequency, slider_step, slider_text_step, "h", size=(50, 10), key="slider")

    def get_button(self):
        return sg.Button('Set', button_color=(sg.theme_element_text_color(), sg.theme_background_color()))

    def get_updated_text(self):
        return f"Current Frequency is {self.frequency} MHz\t{self.cpu_temperature}\t{self.gpu_temperature}"

    def get_tray_text(self):
        return f"{self.frequency} MHz {self.cpu_temperature} {self.gpu_temperature}"
