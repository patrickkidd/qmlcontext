from qmlcontext.pyqt import Qt, QUrl, QQuickWidget
from qmlcontext.quickwidget import QuickWidget
from qmlcontext.models import DocumentModel


class DocumentProperties(QuickWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = DocumentModel(self)
        self.init("DocumentProperties.qml", document=self.model)
