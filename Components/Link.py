from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QFileDialog
import json
import inspect
import os


class Link(QWidget):
    def __init__(self, main_window, parent=None):
        super(Link, self).__init__(parent)

        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.main_window = main_window

        layout = QGridLayout()

        self.folder_link_label = QLabel("Ссылка на файлы класса: ")
        layout.addWidget(self.folder_link_label, 0, 0, 1, 3)

        self.folder_link_edit = QLineEdit()
        self.folder_link_edit.setText(data.get("folder_link"))
        layout.addWidget(self.folder_link_edit, 0, 3, 1, 22)

        self.schedule_link_label = QLabel("Файл расписания класса: ")
        layout.addWidget(self.schedule_link_label, 1, 0, 1, 3)

        self.schedule_link_edit = QLineEdit()
        self.schedule_link_edit.setText(data.get("schedule_link"))
        layout.addWidget(self.schedule_link_edit, 1, 3, 1, 20)

        self.file_dialog_button = QPushButton("Browse")
        self.file_dialog_button.clicked.connect(self.open_dialog)
        layout.addWidget(self.file_dialog_button, 1, 23, 1, 2)

        self.setLayout(layout)

    def open_dialog(self):
        file_name = QFileDialog.getOpenFileName(self.main_window, "Open File", os.path.dirname(inspect.getfile(self.main_window.__class__)), "Excel files (*.xls *.xlsx)")[0]
        if file_name:
            self.schedule_link_edit.setText(file_name)
