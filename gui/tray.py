from __future__ import annotations
from typing import TYPE_CHECKING
from psgtray import SystemTray

if TYPE_CHECKING:
    from gui.window import MainWindow


class Tray(SystemTray):
    def __init__(self, window: MainWindow) -> None:
        fast_set_list: list = window.config.get("CPU", "fast_set_list").split(", ")
        super().__init__(
            ['', ['Show', "Set", fast_set_list, '---', 'Exit']],
            window.config.get("Advanced", "logo_tray"),
            window.get_tray_tooltip(),
            False,
            window
        )
