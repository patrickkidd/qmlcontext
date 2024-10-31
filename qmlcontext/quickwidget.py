import os.path
import logging

from qmlcontext.pyqt import (
    Qt,
    QUrl,
    QRectF,
    QQuickWidget,
    QSurfaceFormat,
    QQuickItem,
    QApplication,
)


SURFACE_FORMAT = QSurfaceFormat()
SURFACE_FORMAT.setSamples(8)


_log = logging.getLogger(__name__)


def qml(path: str) -> str:
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, "resources", "qml", path)


class QuickWidget(QQuickWidget):

    qtbot = None  # testing

    def init(self, sourceFile: str, **contextProperties):
        for key, value in contextProperties.items():
            self.rootContext().setContextProperty(key, value)
        super().setSource(QUrl(qml(sourceFile)))
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)
        metaObject = self.rootObject().metaObject()
        self._rootProperties = [
            metaObject.property(i).name() for i in range(metaObject.propertyCount())
        ]

    ## Test: Items

    def contextProperty(self, property: str):
        return self.rootContext().contextProperty(property)

    def item(self, name: str):
        if name not in self._rootProperties:
            raise AttributeError(f"Root property '{name}' not found on {self}")

        item = self.rootObject().property(name)
        if not item:
            raise AttributeError(f"Root property item '{name}' is None")

        return item

    def itemProp(self, path: str):
        if not "." in path:
            raise ValueError(
                f"Use dot-notation to get an item's property, e.g. 'comboBox.currentIndex', got {path}"
            )

        rootProp, itemProp = path.split(".")
        return self.item(rootProp).property(itemProp)

    def setItemProp(self, path: str, value):
        if not "." in path:
            raise ValueError(
                f"Use dot-notation to set an item's property, e.g. 'comboBox.currentIndex', got {path}"
            )

        rootProp, itemProp = path.split(".")
        self.item(rootProp).setProperty(itemProp, value)

    ## Test: Interactivity

    def mouseClickItem(self, item: QQuickItem, button=Qt.LeftButton, pos=None):
        assert (
            item.property("enabled") == True
        ), f"The item {item.objectName() if item.objectName() else item} cannot be clicked if it is not enabled."

        assert (
            item.property("visible") == True
        ), f"The item {item.objectName() if item.objectName() else item} cannot be clicked if it is not visible."

        if pos is None:
            rect = item.mapRectToScene(
                QRectF(0, 0, item.property("width"), item.property("height"))
            ).toRect()
            pos = rect.center()
        _log.debug(
            f"QuickWidget.mouseClickItem('{item.objectName()}')"  # , {button}, {pos}) (rect: {rect})'
        )

        self.qtbot.mouseClick(self, button, Qt.NoModifier, pos)

    def mouseClick(self, name: str):
        self.mouseClickItem(self.item(name))

    def focusItem(self, name: str):
        _log.debug(f'QuickWidget.focusItem("{name}")')
        if not self.isActiveWindow():

            QApplication.setActiveWindow(self)
            self.qtbot.waitActive(self)
            if not self.isActiveWindow():
                raise RuntimeError(
                    "Could not set activeWindow to %s, currently is %s"
                    % (self, QApplication.activeWindow())
                )

        item = self.item(name)
        self.mouseClickItem(item)
        if not item.hasActiveFocus():
            item.forceActiveFocus()  # in case mouse doesn't work if item out of view
            self.qtbot.waitUntil(lambda: item.hasActiveFocus())

    def resetFocus(self, itemName: str):
        item = self.item(itemName)
        _log.debug(f'QuickWidget.resetFocus("{itemName}")')
        item.setProperty("focus", False)
        if item.hasActiveFocus():
            self.rootObject().forceActiveFocus()  # TextField?
            if item.hasActiveFocus():
                raise RuntimeError(f"Could not re-set active focus on {itemName}.")

    def keyClick(self, itemName, key, resetFocus=True):
        self.focusItem(itemName)
        _log.debug(f'QmlWidgetHelper.keyClick("{itemName}", {key})')
        self.qtbot.keyClick(self, key)
        if resetFocus:
            self.resetFocus(itemName)

    def keyClicks(self, itemName, s: str, selectAllFirst=True, resetFocus=True, returnToFinish=True):
        self.focusItem(itemName)
        _log.debug(f"QuickWidget.keyClicks('{itemName}', '{s}')")
        item = self.item(itemName)
        if not item.property('enabled'):
            raise RuntimeError(f"Cannot send key clicks to item that is not enabled: {itemName}")
        if not item.property('visible'):
            raise RuntimeError(f"Cannot send key clicks to item that is not visible: {itemName}")
        if selectAllFirst:
            item.selectAll()
        self.qtbot.keyClicks(self, s)
        if returnToFinish:
            self.qtbot.keyClick(self, Qt.Key_Return)  # only for TextInput?
        if resetFocus:
            self.resetFocus(itemName)
