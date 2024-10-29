import logging

from qmlcontext.pyqt import pyqtProperty, pyqtSignal, QObject
from qmlcontext.items import Document


_log = logging.getLogger(__name__)


class DocumentModel(QObject):
    """
    Static wrapper that updates the properties when the underlying Document
    object gets swapped out.
    """

    titleChanged = pyqtSignal(str)
    categoriesChanged = pyqtSignal(list)
    categoryIndexChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._document = None

    def setDocument(self, document: Document):
        if self._document:
            self._document.titleChanged.disconnect(self.titleChanged)
            self._document.categoriesChanged.disconnect(self.categoriesChanged)
            self._document.categoryIndexChanged.disconnect(self.categoryIndexChanged)
        self._document = document
        if self._document:
            self._document.titleChanged.connect(self.titleChanged)
            self._document.categoriesChanged.connect(self.categoriesChanged)
            self._document.categoryIndexChanged.connect(self.categoryIndexChanged)
            self.titleChanged.emit(self._document.title)
            self.categoriesChanged.emit(self._document.categories)
            self.categoryIndexChanged.emit(self._document.categoryIndex)
        else:
            self.titleChanged.emit("")
            self.categoriesChanged.emit([])
            self.categoryIndexChanged.emit(-1)

    def setTitle(self, title: str):
        if self._document:
            _log.debug(f"documentModel.setTitle('{title}')")
            self._document.setTitle(title)

    @pyqtProperty(str, fset=setTitle, notify=titleChanged)
    def title(self):
        ret = self._document.title if self._document else ""
        _log.debug(f"documentModel.title: {ret}")
        return ret

    def setCategories(self, categories: list):
        if self._document:
            _log.debug(f"documentModel.setCategories('{categories}')")
            self._document.setCategories(categories)

    @pyqtProperty(list, fset=setCategories, notify=categoriesChanged)
    def categories(self):
        ret = self._document.categories if self._document else []
        _log.debug(f"documentModel.categories: {ret}")
        return ret

    def setCategoryIndex(self, index: int):
        _log.debug(f"documentModel.setCategoryIndex('{index}')")
        self._document.setCategoryIndex(index)

    @pyqtProperty(int, fset=setCategoryIndex, notify=categoryIndexChanged)
    def categoryIndex(self):
        ret = self._document.categoryIndex if self._document else -1
        _log.debug(f"documentModel.categoryIndex: {ret}")
        return ret
