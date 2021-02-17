from PyQt5.QtWidgets import QProgressBar


class Progress(QProgressBar):
    def __init__(self, parent=None):
        super(Progress, self).__init__(parent)
