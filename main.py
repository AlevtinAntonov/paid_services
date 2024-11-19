import sys
from PyQt6 import QtWidgets as qtw


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    form = LoginForm()
    sys.exit(app.exec())