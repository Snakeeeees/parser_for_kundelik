from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import json


class Folders(QTableWidget):
    def __init__(self, parent=None):
        super(Folders, self).__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Subject", "Folder"])
        self.update_table()

    def update_table(self):
        # self.clear()
        try:
            from folder import count
        except Exception:
            count = 50
        self.setRowCount(count)
        try:
            with open("match_subjects.json", "r", encoding="utf-8") as f:
                subjects = json.load(f)
                folders = list(subjects.keys())
                print(folders)
                for i in range(len(folders)):
                    self.setItem(i, 1, QTableWidgetItem(folders[i]))
                    self.setItem(i, 0, QTableWidgetItem(subjects[folders[i]]))
        except FileNotFoundError:
            pass
