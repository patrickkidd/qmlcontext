import pytest


from qmlcontext.pyqt import QApplication, QEventLoop, QTimer
from qmlcontext import Condition
from qmlcontext.items import Document
from qmlcontext.models import DocumentModel
from qmlcontext.views import DocumentProperties

from qmlcontext.tests.test_documentmodel import document


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

    assert titleChanged.mock.call_count == 1
    assert view.itemProp("titleField.text") == document.title

    assert categoriesChanged.mock.call_count == 1
    assert view.itemProp("categoryBox.model") == document.categories

    assert categoryIndexChanged.mock.call_count == 1
    assert view.itemProp("categoryBox.currentIndex") == document.categoryIndex


def test_clear_document(view, document):
    titleChanged = Condition(view.model.titleChanged)
    categoriesChanged = Condition(view.model.categoriesChanged)
    categoryIndexChanged = Condition(view.model.categoryIndexChanged)

    view.model.setDocument(document)
    view.model.setDocument(None)

    assert titleChanged.mock.call_count == 2
    assert view.itemProp("titleField.text") == ""

    assert categoriesChanged.mock.call_count == 2
    assert view.itemProp("categoryBox.model") == []

    assert categoryIndexChanged.mock.call_count == 2
    assert view.itemProp("categoryBox.currentIndex") == -1


def waitALittle():
    # Added for qml components since init is deferred. Works better than
    # QApplication.processEvents()
    loop = QEventLoop()
    QTimer.singleShot(10, loop.quit)  # may need to be longer?
    loop.exec()


def test_set_fields(view, document):
    NEW_TITLE = "New Title"
    NEW_CATEGORY_INDEX = 1

    view.model.setDocument(document)

    view.focusItem("titleField")
    assert view.item("titleField").hasActiveFocus() == True

    waitALittle()
    # QApplication.instance().processEvents()

    # QApplication.instance().exec_()

    view.keyClicks("titleField", NEW_TITLE)
    view.setItemProp("categoryBox.currentIndex", NEW_CATEGORY_INDEX)
    assert document.title == NEW_TITLE
    assert document.categoryIndex == NEW_CATEGORY_INDEX


def test_responsive_fields(view, document):
    NEW_TITLE = "New Title"
    NEW_CATEGORY_INDEX = 1

    view.model.setDocument(document)

    titleChanged = Condition(view.model.titleChanged)
    categoriesChanged = Condition(view.model.categoriesChanged)
    categoryIndexChanged = Condition(view.model.categoryIndexChanged)

    document.setTitle(NEW_TITLE)
    document.setCategoryIndex(NEW_CATEGORY_INDEX)

    assert titleChanged.mock.call_count == 1
    assert view.itemProp("titleField.text") == NEW_TITLE

    assert categoriesChanged.mock.call_count == 1
    assert view.itemProp("categoryBox.model") == []

    assert categoryIndexChanged.mock.call_count == 1
    assert view.itemProp("categoryBox.currentIndex") == NEW_CATEGORY_INDEX
