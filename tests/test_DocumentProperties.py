import logging

import pytest


from qmlcontext.pyqt import QApplication, QEventLoop, QTimer
from qmlcontext import Condition
from qmlcontext.items import Document
from qmlcontext.models import DocumentModel
from qmlcontext.views import DocumentProperties

from .test_documentmodel import document

_log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def _init(our_qtbot):
    pass


@pytest.fixture
def model():
    return DocumentModel()


@pytest.fixture
def view(qApp, qtbot):
    _view = DocumentProperties()
    _view.resize(640, 480)
    _view.show()
    qtbot.addWidget(_view)
    qtbot.waitActive(_view)
    yield _view


@pytest.fixture
def document():
    i = 123
    document = Document()
    document.setTitle(f"Title {i}")
    document.setCategories([f"Category {i}", f"Category {i + 1}", f"Category {i + 2}"])
    document.setCategoryIndex(i)
    return document


def test_init(view):
    assert view.contextProperty("document") is not None
    assert view.itemProp("titleField.text") == ""
    assert view.itemProp("categoryBox.model") == []
    assert view.itemProp("categoryBox.currentIndex") == -1


def test_set_document(view, document):
    titleChanged = Condition(view.model.titleChanged)
    categoriesChanged = Condition(view.model.categoriesChanged)
    categoryIndexChanged = Condition(view.model.categoryIndexChanged)
    view.model.setDocument(document)

    assert titleChanged.called()
    assert view.itemProp("titleField.text") == document.title

    assert categoriesChanged.called()
    assert view.itemProp("categoryBox.model") == document.categories

    assert categoryIndexChanged.called()
    assert view.itemProp("categoryBox.currentIndex") == document.categoryIndex


def test_clear_document(view, document):
    titleChanged = Condition(view.model.titleChanged)
    categoriesChanged = Condition(view.model.categoriesChanged)
    categoryIndexChanged = Condition(view.model.categoryIndexChanged)

    view.model.setDocument(document)
    view.model.setDocument(None)

    assert titleChanged.called()
    assert view.itemProp("titleField.text") == ""

    assert categoriesChanged.called()
    assert view.itemProp("categoryBox.model") == []

    assert categoryIndexChanged.called()
    assert view.itemProp("categoryBox.currentIndex") == -1


def waitALittle():
    # Added for qml components since init is deferred. Works better than
    # QApplication.processEvents()
    loop = QEventLoop()
    QTimer.singleShot(10, loop.quit)  # may need to be longer?
    loop.exec()


def dumpWidget(widget):
    import os.path, time
    from PyQt5.QtGui import QPixmap

    ROOT = os.path.join(os.path.dirname(__file__), "..")
    pixmap = QPixmap(widget.size())
    widget.render(pixmap)
    fileDir = os.path.realpath(os.path.join(ROOT, "dumps"))
    pngPath = os.path.join(fileDir, "dump_%s.png" % time.time())
    os.makedirs(fileDir, exist_ok=True)
    if not pixmap.isNull():
        pixmap.save(pngPath)
        _log.info(f"Dumped widget to: {pngPath}")
        os.system('open "%s"' % pngPath)


def test_set_fields(view, document):
    NEW_TITLE = "New Title"
    NEW_CATEGORY_INDEX = 1

    view.model.setDocument(document)

    # view.focusItem("titleField")
    # assert view.item("titleField").hasActiveFocus() == True
    view.keyClicks("titleField", NEW_TITLE, selectAllFirst=True)

    view.setItemProp("categoryBox.currentIndex", NEW_CATEGORY_INDEX)
    assert document.title == NEW_TITLE
    assert document.categoryIndex == NEW_CATEGORY_INDEX


def test_responsive_fields(view, document):
    NEW_TITLE = "New Title"
    NEW_CATEGORY_INDEX = 1

    view.model.setDocument(document)

    titleChanged = Condition(view.model.titleChanged)
    categoryIndexChanged = Condition(view.model.categoryIndexChanged)

    def onCategoryIndexChanged(index):
        assert index == NEW_CATEGORY_INDEX

    view.model.categoryIndexChanged.connect(onCategoryIndexChanged)

    document.setTitle(NEW_TITLE)
    document.setCategoryIndex(NEW_CATEGORY_INDEX)

    assert titleChanged.called()
    assert view.itemProp("titleField.text") == NEW_TITLE

    assert categoryIndexChanged.called()
    assert view.itemProp("categoryBox.currentIndex") == NEW_CATEGORY_INDEX
