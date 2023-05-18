from PyQt5.QtWidgets import QMessageBox, QApplication, QLineEdit, QVBoxLayout, QPushButton, QWidget, QDialog, QLabel

class PasswordDialog(QDialog):
    def __init__(self,m="Enter Password:",parent=None):
        super(PasswordDialog, self).__init__(parent)
        self.setWindowTitle("Password Dialog")

        # Create a label for password input
        password_label = QLabel(m)
        # Create a line edit for password input
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        # Create OK and Cancel buttons
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)


        # Create a vertical layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        # Set the layout to the dialog
        self.setLayout(layout)

    def getPassword(self):
        return self.password_edit.text()


