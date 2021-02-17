from PyQt5.QtWidgets import QPushButton
import json


class SaveButton(QPushButton):
    def __init__(self, schedule, folders_table, folders_link, sign, sign_checkbox, parent=None):
        super(SaveButton, self).__init__(parent)
        self.setText("Save")
        self.schedule = schedule
        self.folders_table = folders_table
        self.folders_link = folders_link
        self.sign = sign
        self.sign_checkbox = sign_checkbox

    def mousePressEvent(self, event):
        print("It's working")
        schedule_by_table = {"Monday": [],
                             "Tuesday": [],
                             "Wednesday": [],
                             "Thursday": [],
                             "Friday": [],
                             "Saturday": []}
        week_days = list(schedule_by_table.keys())
        for j in range(6):
            for i in range(10):
                subject = self.schedule.item(i, j)
                if subject is not None:
                    schedule_by_table[week_days[j]].append(subject.text())

        with open("schedule.json", "w", encoding="utf-8") as f:
            json.dump(schedule_by_table, f)

        folders = {}
        for i in range(self.folders_table.rowCount()):
            if self.folders_table.item(i, 0) is None or self.folders_table is None:
                continue
            folders[self.folders_table.item(i, 1).text()] = self.folders_table.item(i, 0).text()

        with open("match_subjects.json", "w", encoding="utf-8") as f:
            json.dump(folders, f)

        data = {}
        data["folder_link"] = self.folders_link.folder_link_edit.text()
        data["schedule_link"] = self.folders_link.schedule_link_edit.text()
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

        if not self.sign_checkbox.isChecked():
            sign = {}
            sign["login"] = self.sign.edit_login.text()
            sign["password"] = self.sign.edit_password.text()
            with open("sign.json", "w", encoding="utf-8") as f:
                json.dump(sign, f)
