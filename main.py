import sys
from PySide6.QtWidgets import QApplication
from ui.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load Qss
    try:
        with open("style/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except:
        print("QSS tidak ditemukan / gagal load")

    # Run Login
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())