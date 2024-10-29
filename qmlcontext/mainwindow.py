from qmlcontext.pyqt import (
    pyqtSignal,
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QStackedWidget,
)


class MainWindow(QMainWindow):

    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Application")
        self.setGeometry(100, 100, 800, 600)

        Layout = QHBoxLayout()

        self._centralWidget = QWidget()
        self._centralWidget.setLayout(Layout)
        self.setCentralWidget(self._centralWidget)

        self.content = QWidget(self._centralWidget)
        self.drawer = QStackedWidget(self._centralWidget)

        from qmlcontext.views import DocumentProperties

        self.documentProperties = DocumentProperties(self.drawer)

    def closeEvent(self, event):
        event.accept()
        super.closeEvent(event)
        self.closed.emit()
