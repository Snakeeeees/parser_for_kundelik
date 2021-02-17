from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import json


class ParseScheduleButton(QPushButton):
    def __init__(self, functions, table_schedule, table_folders, link, progress, parent=None):
        super(ParseScheduleButton, self).__init__(parent)
        self.setText("Update Schedule")
        self.table_schedule = table_schedule
        self.table_folders = table_folders
        self.link = link
        self.functions = functions
        self.progress = progress
        self.progress.hide()

    def mousePressEvent(self, event):
        with open("match_subjects.json", "r", encoding="utf-8") as f:
            matched_subjects_old = json.load(f)
        self.thread = QThread()
        self.parse = ParseScheduleProcess(self.functions, self.link, matched_subjects_old)
        self.parse.moveToThread(self.thread)
        self.parse.change_value.connect(self.change_progress_value)
        self.parse.set_count.connect(self.set_count)
        self.parse.stop_progress.connect(self.stop_progress)
        self.parse.change_maximum.connect(self.change_progress_maximum)
        self.parse.update_schedule.connect(self.update_schedule)
        self.thread.started.connect(self.parse.run)
        self.progress.show()
        self.thread.start()
        print("It's working")
        self.table_folders.update_table()

    def update_schedule(self, schedule):
        with open("schedule.json", "w", encoding="utf-8") as f:
            json.dump(schedule, f)
        self.table_schedule.update_table()
        print("match_subjects\n")

    def change_progress_value(self, i):
        self.progress.setValue(i)

    def change_progress_maximum(self, maximum):
        self.progress.setMaximum(maximum)

    def stop_progress(self, matched_subjects_new):
        self.progress.hide()
        with open("match_subjects.json", "w", encoding="utf-8") as f:
            json.dump(matched_subjects_new, f)
        self.table_folders.update_table()
        self.thread.quit()

    def set_count(self, count):
        with open("folder.py", "w", encoding="utf-8") as f:
            f.write("count = {}".format(count))


class ParseScheduleProcess(QObject):
    update_schedule = pyqtSignal(dict)
    change_value = pyqtSignal(int)
    change_maximum = pyqtSignal(int)
    set_count = pyqtSignal(int)
    stop_progress = pyqtSignal(dict)

    def __init__(self, functions, link, matched_subjects_old):
        super().__init__()
        self.link = link
        self.functions = functions
        self.matched_subjects_old = matched_subjects_old

    def run(self):
        schedule = self.functions.update_schedule(self.link.schedule_link_edit.text())
        print(schedule)
        self.update_schedule.emit(schedule)
        folder_name_id = self.functions.get_folders(self.link.folder_link_edit.text())
        self.change_maximum.emit(len(folder_name_id))
        self.set_count.emit(len(folder_name_id))
        matched_subjects_new = {}
        i = 0
        for folder_name, folder_id in folder_name_id:
            subject = self.functions.match_subjects(folder_name, self.matched_subjects_old)
            matched_subjects_new[folder_name] = subject
            i += 1
            self.change_value.emit(i)
        self.stop_progress.emit(matched_subjects_new)
