# src/SelectMode.py
from src.api import API
from src.gui.test_gui import run as gui_run

def ModeSelector(mode):
    match mode:
        case "gui":
            return gui_run
        case "web":
            return API.run
        case _:
            return lambda: print("Unknown mode")
