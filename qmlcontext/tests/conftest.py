import os
import sys
import logging

import pytest
import mock

# from PyQt5.QtTest import QTest

from qmlcontext import Application, QuickWidget

_log = logging.getLogger(__name__)


# def pytest_generate_tests(metafunc):
#     os.environ["QT_QPA_PLATFORM"] = "offscreen"


_qtbot = None


def qtbot():
    global _qtbot

    return _qtbot


@pytest.fixture(scope="session", autouse=True)
def qApp():

    qApp = Application(sys.argv)

    yield qApp


@pytest.fixture
def our_qtbot(qtbot):
    global _qtbot
    _qtbot = qtbot

    with mock.patch.object(QuickWidget, "qtbot"):
        yield qtbot

    _qtbot = None
