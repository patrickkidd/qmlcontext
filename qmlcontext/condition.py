from qmlcontext.pyqt import pyqtSignal


class Condition:

    def __init__(self, signal: pyqtSignal):
        import mock

        self._mock = mock.Mock()
        self._signal = signal
        self._signal.connect(self._mock)

    @property
    def mock(self):
        return self._mock
