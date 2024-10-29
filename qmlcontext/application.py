import logging

from qmlcontext.pyqt import Qt, QApplication, QQmlApplicationEngine


_log = logging.getLogger(__name__)


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        _log.info("qmlcontext.Application()")

        # self.qmlEngine = QQmlApplicationEngine()
        # self.qmlEngine.addImportPath("qrc:/qml")
