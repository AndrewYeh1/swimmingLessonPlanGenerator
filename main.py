# other imports
import sys

# pyqt6 imports for gui
from PyQt6.QtWidgets import QApplication

# python file imports
import mainWindow


def main():
    # prints error messages
    sys.excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys.excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    # starts the window
    app = QApplication(sys.argv)
    window = mainWindow.MainWindow(app)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
