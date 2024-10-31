import logging

from qmlcontext.pyqt import pyqtSignal, pyqtProperty, QObject

_log = logging.getLogger(__name__)


class Document(QObject):

    titleChanged = pyqtSignal(str)
    categoriesChanged = pyqtSignal(list)
    categoryIndexChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._title = ""
        self._categories = []
        self._categoryIndex = -1

    def setTitle(self, title: str):
        self._title = title
        self.titleChanged.emit(self._title)

    @pyqtProperty(str, fset=setTitle, notify=titleChanged)
    def title(self):
        return self._title

    def setCategories(self, categories: list):
        self._categories = categories
        self.categoriesChanged.emit(self._categories)

    @pyqtProperty(list, fset=setCategories, notify=categoriesChanged)
    def categories(self):
        return self._categories

    def setCategoryIndex(self, index: int):
        self._categoryIndex = index
        self.categoryIndexChanged.emit(index)

    @pyqtProperty(int, fset=setCategoryIndex, notify=categoryIndexChanged)
    def categoryIndex(self):
        return self._categoryIndex
