from PyQt5 import QtWidgets, QtGui, QtCore
from Components.Link import Link
from Components.Login import Login
from Components.Login_button import LoginProcess
from Components.Schedule import Schedule
from Components.Folders import Folders
from Components.Download_button import DownloadButton
from Components.Parse_schedule_button import ParseScheduleButton
from Components.Save_button import SaveButton
from Components.Progress_Bar import Progress

from core import Core
import json


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        core = Core()
        try:
            with open("sign.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"login": None, "password": None}

        pos = core.login(data.get("login"), data.get("password"))

        layout = QtWidgets.QVBoxLayout()
        login = Login(pos)
        layout.addWidget(login)

        login_button = LoginProcess(core, login)
        layout.addWidget(login_button)

        link = Link(self)
        layout.addWidget(link)

        tables_layout = QtWidgets.QHBoxLayout()

        schedule = Schedule()
        folders = Folders()

        tables_layout.addWidget(schedule)
        tables_layout.addWidget(folders)

        layout.addLayout(tables_layout)

        buttons_layout = QtWidgets.QHBoxLayout()

        progress_update = Progress()
        progress_download = Progress()

        buttons_layout.addWidget(SaveButton(schedule, folders, link, login, login_button.checkbox))
        buttons_layout.addWidget(ParseScheduleButton(core, schedule, folders, link, progress_update))

        layout.addLayout(buttons_layout)

        layout.addWidget(DownloadButton(core, link, progress_download))

        layout.addWidget(progress_update)
        layout.addWidget(progress_download)

        self.setLayout(layout)
        self.show()


app = QtWidgets.QApplication([])
win = Window()
app.exec_()
