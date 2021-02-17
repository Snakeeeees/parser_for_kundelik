from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import json


class Schedule(QTableWidget):
    def __init__(self, parent=None):
        super(Schedule, self).__init__(parent)
        self.setColumnCount(6)
        self.setRowCount(10)
        self.setHorizontalHeaderLabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
        self.setVerticalHeaderLabels(list(map(str, range(1, 11))))
        self.update_table()

    def update_table(self):
        # self.clear()
        try:
            with open("schedule.json", "r") as f:
                schedule = json.load(f)
            week_days = list(schedule.keys())
            for i in range(len(week_days)):
                for j in range(len(schedule[week_days[i]])):
                    self.setItem(j, i, QTableWidgetItem(schedule[week_days[i]][j]))
        except Exception as e:
            print(e)
