import sys

from qmlcontext import Application, MainWindow


app = Application(sys.argv)
mw = MainWindow()
mw.show()
mw.closed.connect(app.quit)
app.exec_()
