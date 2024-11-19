from PyQt6 import QtWidgets as qtw

from controller.start_window import StartWindow
from view.login_window import Ui_FormLogin


class LoginForm(qtw.QWidget, Ui_FormLogin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect the login button to the method
        self.pb_Login.clicked.connect(self.check_user_password)

        self.show()

    def check_user_password(self):
        if self.le_username.text() == '' and self.le_password.text() == '':
            self.enter_to_prog()
        else:
            self.le_result.setText('Wrong Username or Password! Try again.')
            print('Wrong Username or Password !!!')

    def enter_to_prog(self):

        try:
            self.start_window = StartWindow()
            self.start_window.show()
            self.hide()
        except Exception as e:
            print(f"An error occurred: {e}")
