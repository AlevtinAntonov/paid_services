import sys
from PyQt6 import QtWidgets as qtw

from controller.login_form import LoginForm

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyle('Fusion') #Windows
    app.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                color: #000000;
                font-family: "Times New Roman";
                font-size: 14px;
            }
            QAbstractItemView::item:selected {
            background-color: #FAEBD7;  /* Цвет выделения */
            color: black;                 /* Цвет текста при выделении */
            }
            QTextEdit {
                selection-background-color: lightgray;  /* Цвет выделения в текстовом редакторе */
                selection-color: black;                  /* Цвет текста при выделении в текстовом редакторе */
            }
        """)
    form = LoginForm()
    sys.exit(app.exec())
