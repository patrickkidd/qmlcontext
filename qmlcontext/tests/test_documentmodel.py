import pytest
import mock

from qmlcontext.condition import Condition
from qmlcontext.items import Document
from qmlcontext.models import DocumentModel


@pytest.fixture
def model():
    return DocumentModel()


@pytest.fixture
def document():
    i = 123
    document = Document()
    document.setTitle(f"Title {i}")
    document.setCategories([f"Category {i}", f"Category {i + 1}"])
    document.setCategoryIndex(i)
    return document


def test_init(model):
    assert model.title == ""
    assert model.categories == []
    assert model.categoryIndex == -1


def test_set_document(model, document):
    titleChanged = Condition(model.titleChanged)
    categoriesChanged = Condition(model.categoriesChanged)
    categoryIndexChanged = Condition(model.categoryIndexChanged)
    model.setDocument(document)

    assert titleChanged.mock.call_count == 1
    assert model.title == document.title

    assert categoriesChanged.mock.call_count == 1
    assert model.categories == document.categories

    assert categoryIndexChanged.mock.call_count == 1
    assert model.categoryIndex == document.categoryIndex


def test_clear_document(model, document):
    titleChanged = Condition(model.titleChanged)
    categoriesChanged = Condition(model.categoriesChanged)
    categoryIndexChanged = Condition(model.categoryIndexChanged)

    model.setDocument(document)
    model.setDocument(None)

    assert titleChanged.mock.call_count == 2
    assert model.title == ""

    assert categoriesChanged.mock.call_count == 2
    assert model.categories == []

    assert categoryIndexChanged.mock.call_count == 2
    assert model.categoryIndex == -1


def test_set_document_many_times(model, document):
    NUM = 3

    titleChanged = Condition(model.titleChanged)
    categoriesChanged = Condition(model.categoriesChanged)
    categoryIndexChanged = Condition(model.categoryIndexChanged)

    for i in range(NUM):
        model.setDocument(document)
        model.setDocument(None)

    assert titleChanged.mock.call_count == NUM * 2
    assert model.title == ""

    assert categoriesChanged.mock.call_count == NUM * 2
    assert model.categories == []

    assert categoryIndexChanged.mock.call_count == NUM * 2
    assert model.categoryIndex == -1
