from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from app_paths import app_root
from gui.main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("QuickRed Tech Differentiator")
    app.setFont(QFont("Segoe UI", 10))
    logo_path = app_root() / "resources" / "icons" / "logo.png"
    if logo_path.exists():
        from PySide6.QtGui import QIcon

        app.setWindowIcon(QIcon(str(logo_path)))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
