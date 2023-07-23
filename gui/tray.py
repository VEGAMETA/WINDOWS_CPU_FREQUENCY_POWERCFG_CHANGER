from __future__ import annotations
from typing import TYPE_CHECKING
from psgtray import SystemTray

if TYPE_CHECKING:
    from gui.window import MainWindow


class Tray(SystemTray):
    def __init__(self, window: MainWindow) -> None:
        fast_set_list: list = window.config.get("CPU", "fast_set_list").split(", ")
        tray_menu: list = ['', ['Open', "Set", fast_set_list, '---', 'Exit']]
        super().__init__(
            tray_menu,
            single_click_events=False,
            window=window,
            tooltip=window.get_tray_text(),
            icon=window.config.get("Advanced", "logo_tray")
        )
