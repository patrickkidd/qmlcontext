import logging

from qmlcontext.pyqt import Qt, QApplication


_log = logging.getLogger(__name__)


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
