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
            self._document.titleChanged.disconnect(self.onDocumentTitleChanged)
            self._document.categoriesChanged.disconnect(
                self.onDocumentCategoriesChanged
            )
            self._document.categoryIndexChanged.disconnect(
                self.onDocumentCategoryIndexChanged
            )
        self._document = document
        if self._document:
            self._document.titleChanged.connect(self.onDocumentTitleChanged)
            self._document.categoriesChanged.connect(self.onDocumentCategoriesChanged)
            self._document.categoryIndexChanged.connect(
                self.onDocumentCategoryIndexChanged
            )
        self.onDocumentTitleChanged()
        self.onDocumentCategoriesChanged()
        self.onDocumentCategoryIndexChanged()

    # Document listeners

    def onDocumentTitleChanged(self):
        if self._document:
            self.titleChanged.emit(self._document.title)
        else:
            self.titleChanged.emit("")

    def onDocumentCategoriesChanged(self):
        if self._document:
            self.categoriesChanged.emit(self._document.categories)
        else:
            self.categoriesChanged.emit([])

    def onDocumentCategoryIndexChanged(self):
        if self._document:
            self.categoryIndexChanged.emit(self._document.categoryIndex)
        else:
            self.categoryIndexChanged.emit(-1)

    # Getters and setters

    def setTitle(self, title: str):
        if self._document:
            self._document.setTitle(title)

    @pyqtProperty(str, fset=setTitle, notify=titleChanged)
    def title(self):
        ret = self._document.title if self._document else ""
        return ret

    def setCategories(self, categories: list):
        if self._document:
            self._document.setCategories(categories)

    @pyqtProperty(list, fset=setCategories, notify=categoriesChanged)
    def categories(self):
        ret = self._document.categories if self._document else []
        return ret

    def setCategoryIndex(self, index: int):
        if self._document:
            self._document.setCategoryIndex(index)

    @pyqtProperty(int, fset=setCategoryIndex, notify=categoryIndexChanged)
    def categoryIndex(self):
        ret = self._document.categoryIndex if self._document else -1
        return ret
