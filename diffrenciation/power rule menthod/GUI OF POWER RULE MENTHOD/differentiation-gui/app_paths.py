import sys
from pathlib import Path


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS)
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent
