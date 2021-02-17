from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import json


class DownloadButton(QPushButton):
    def __init__(self, functions, link, progress, parent=None):
        super().__init__(parent)
        self.setText("Download")
        self.functions = functions
        self.link = link.folder_link_edit.text()
        self.progress = progress
        self.progress.hide()

    def mousePressEvent(self, event):
        with open("schedule.json", "r", encoding="utf-8") as f:
            schedule = json.load(f)
        with open("match_subjects.json", "r", encoding="utf-8") as f:
            subjects = json.load(f)
        self.thread = QThread()
        self.download = DownloadProcess(self.functions, subjects, schedule, self.link)
        self.download.moveToThread(self.thread)
        self.download.change_value.connect(self.change_progress_value)
        self.download.change_maximum.connect(self.change_progress_maximum)
        self.download.stop_progress.connect(self.stop_progress)
        self.thread.started.connect(self.download.run)
        self.progress.show()
        self.thread.start()

    def change_progress_value(self, i):
        self.progress.setValue(i)

    def change_progress_maximum(self, maximum):
        self.progress.setMaximum(maximum)

    def stop_progress(self):
        self.progress.hide()
        self.thread.quit()


class DownloadProcess(QObject):
    change_value = pyqtSignal(int)
    change_maximum = pyqtSignal(int)
    stop_progress = pyqtSignal()

    def __init__(self, functions, subjects, schedule, link):
        super(DownloadProcess, self).__init__()
        self.functions = functions
        self.schedule = schedule
        self.subjects = subjects
        self.link = link

    def run(self):
        count = 0
        folders = self.functions.get_folders(self.link)
        print(folders)
        self.change_maximum.emit(len(folders))
        subjects_for_now = self.functions.get_subjects_for_today(self.schedule)
        links_with_folders = {}
        if subjects_for_now:
            i = 1
            for folder_name, folder_id in folders:
                links, folder_name_new = self.functions.search_for_documents(folder_name, folder_id, self.subjects, subjects_for_now, self.link)
                self.change_value.emit(i)
                i += 1
                if links:
                    links_with_folders[folder_name_new] = links
                    count += len(links)
            i = 1
            print(len(links_with_folders))
            self.change_maximum.emit(count)
            print(count)
            for folder in links_with_folders:
                for file_name in links_with_folders[folder]:
                    self.functions.download_files(file_name, links_with_folders[folder][file_name], folder)
                    self.change_value.emit(i)
                    i += 1
        self.functions.remember_files()
        self.stop_progress.emit()
