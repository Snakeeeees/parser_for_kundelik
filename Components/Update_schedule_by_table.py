from PyQt5.QtWidgets import QPushButton
import json


class UpdateScheduleByTableButton(QPushButton):
    def __init__(self, schedule, parent=None):
        super(UpdateScheduleByTableButton, self).__init__(parent)
        self.schedule = schedule

    def mousePressEvent(self, event):
        print("It's working")
        schedule_by_table = {"Monday": [],
                             "Tuersday": [],
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
