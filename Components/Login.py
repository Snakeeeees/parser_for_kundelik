from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import json


class Login(QWidget):
    def __init__(self, s, parent=None):
        super(Login, self).__init__(parent)

        try:
            with open("sign.json", "r", encoding="utf-8") as f:
                sign = json.load(f)
        except FileNotFoundError:
            sign = {"login": "", "password": ""}

        layout = QGridLayout()

        self.pos = QLabel()
        if s == 0:
            image = QPixmap("src/fail.png")
        else:
            image = QPixmap("src/success.png")
        self.pos.setPixmap(image)
        self.pos.setAlignment(Qt.AlignLeft)

        layout.addWidget(self.pos, 0, 2, 2, 1)

        login = QLabel("Логин: ")
        layout.addWidget(login, 0, 0)

        self.edit_login = QLineEdit()
        self.edit_login.setText(sign.get("login"))
        layout.addWidget(self.edit_login, 0, 1)

        password = QLabel("Пароль: ")
        layout.addWidget(password, 1, 0)

        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setText(sign.get("password"))
        layout.addWidget(self.edit_password, 1, 1)

        self.setLayout(layout)
