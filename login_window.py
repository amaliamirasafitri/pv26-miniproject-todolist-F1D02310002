from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox
)
from database.db import Database

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.db = Database()
        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Login")
        self.btn_register = QPushButton("Register")

        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.register)

    def login(self):
        user = self.db.login_user(
            self.username.text(),
            self.password.text()
        )

        if user:
            from ui.main_window import MainWindow
            self.main = MainWindow(self.username.text())
            self.main.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Login failed")

    def register(self):
        success = self.db.register_user(
            self.username.text(),
            self.password.text()
        )

        if success:
            QMessageBox.information(self, "Success", "User created successfully")
        else:
            QMessageBox.warning(self, "Error", "Username already exists")