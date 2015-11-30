import os
import sys
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath('.'))

# Create a single, persistent QApplication for use in all tests.
papp = QApplication(sys.argv)


def _processPendingEvents(app):
    """Process pending application events.
    Timeout is used, because on Windows hasPendingEvents() always returns True
    """
    t = time.time()
    while app.hasPendingEvents() and (time.time() - t < 0.1):
        app.processEvents()


def in_main_loop(func, *args):
    """Decorator executes test method in the QApplication main loop.
    QAction shortcuts doesn't work, if main loop is not running.
    Do not use for tests, which doesn't use main loop, because it slows down execution.
    """
    def wrapper(*args):
        self = args[0]

        def execWithArgs():
            self.qpart.show()
            QTest.qWaitForWindowExposed(self.qpart)
            _processPendingEvents(self.app)

            try:
                func(*args)
            finally:
                _processPendingEvents(self.app)
                self.app.quit()

        QTimer.singleShot(0, execWithArgs)

        self.app.exec_()

    wrapper.__name__ = func.__name__  # for unittest test runner
    return wrapper
