from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import os
import json


class LoginProcess(QWidget):
    def __init__(self, functions, sign, parent=None):
        super(LoginProcess, self).__init__(parent)
        layout = QHBoxLayout()

        self.checkbox = LoginCheckBox()
        button = LoginButton(functions, sign, self.checkbox)

        layout.addWidget(button)
        layout.addWidget(self.checkbox)

        self.setLayout(layout)


class LoginButton(QPushButton):
    def __init__(self, functions, sign, checkbox, parent=None):
        super(LoginButton, self).__init__(parent)
        self.setText("Login")
        self.sign = sign
        self.functions = functions
        self.checkbox = checkbox

    def mousePressEvent(self, event):
        login = self.sign.edit_login.text()
        password = self.sign.edit_password.text()
        s = self.functions.login(login, password)
        if s == 0:
            self.sign.pos.setPixmap(QPixmap("src/fail.png"))
        else:
            if not self.checkbox.isChecked():
                with open("sign.json", "w", encoding="utf-8") as f:
                    json.dump({"login": login, "password": password}, f)
            self.sign.pos.setPixmap(QPixmap("src/success.png"))


class LoginCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super(LoginCheckBox, self).__init__(parent)
        self.setText("Не запоминать логин и пароль")
        self.setCheckState(QtCore.Qt.Unchecked)

    def mousePressEvent(self, event):
        print("fdifj")
        print(self.isChecked())
        if self.isChecked():
            print("ew")
            self.setCheckState(QtCore.Qt.CheckState(0))
        else:
            print("ejif")
            try:
                os.remove("sign.json")
            except FileNotFoundError:
                pass
            self.setCheckState(QtCore.Qt.CheckState(2))
