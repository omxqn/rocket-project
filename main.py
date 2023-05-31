import random
import sys
import time
import threading
from ui import Ui_MainWindow
from PyQt5.Qt import *
from password_manager import PasswordDialog
# pip install PyQtChart
from cryption import *

# pip install PyQtChart
data = {"speed": 0, "altitude": 0, "pressure": 0, "location": {"log": "0", "lat": "0"}}


def refresh():
    print("Updating")
    data["speed"] = random.randint(10, 2000)
    data["altitude"] = random.randint(10, 2000)
    data["pressure"] = random.randint(10, 2000)
    data["location"]["long"] = str(random.randint(10, 2000))
    data["location"]["lat"] = str(random.randint(10, 2000))


class MyForm(QMainWindow):
    def __init__(self):

        super(MyForm, self).__init__()

        self.timer = QTimer()  # Create a QTimer
        self.timer.timeout.connect(self.refresh)  # Connect timeout signal to update_speed slot
        self.timer.start(1000)  # Start the timer with an interval of 1000 milliseconds (1 second)
        self.main_wind()
        self.default_settings()
        print("started")


    def main_wind(self):
        QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.buttons()
        self.menu_bar()
        self.charts()

    def menu_bar(self):
        self.menubar = self.menuBar()  # Update this line to get the menu bar from self
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 798, 21))
        self.menuchange_password = QMenu(self.menubar)
        self.menuchange_password.setObjectName(u"menuchange_password")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)
        self.menuchange_password.setTitle(QCoreApplication.translate("MainWindow", u"change password", None))
        self.menubar.addAction(self.menuchange_password.menuAction())
        self.change_pass = QAction("m", self)
        self.change_pass.setText(QCoreApplication.translate("MainWindow", u"change fire password", None))
        self.change_pass.setObjectName(u"actionchange_fire_password")
        self.change_pass.triggered.connect(self.change_fire_password)  # Connect triggered signal to slot
        self.menuchange_password.addAction(self.change_pass)

    def default_settings(self):

        self.autherized = False
        self.speed = data["speed"]
        self.altitude = data["altitude"]
        self.pressure = data["pressure"]
        self.location = data["location"]
        self.long = data["location"].get("long") or "0"
        self.lat = data["location"]["lat"] or "0"
        self.ui.checkButton.hide()
        self.ui.initiate_Button.hide()
        self.ui.fireButton.hide()
        try:
            with open("database.key", "r") as f:
                self.launch_password = f.read()
                f.close()
        except:
            password_dialog = PasswordDialog(m="Enter New Auth password")
            # Show the dialog and get the result
            result = password_dialog.exec_()

            if result == QDialog.Accepted:
                self.launch_password = password_dialog.getPassword()
                self.launch_password = self.encryption_system(en=True,passw=self.launch_password)
                with open("database.key", "w") as f:
                    f.write(self.launch_password)
                    f.close()
                QMessageBox.information(self, "Authentecation Success",
                                    f"Your password: {password_dialog.getPassword()} has been created")
            else:
                QMessageBox.warning(self, "Authentecation Error",
                                    "Please enter a valid password")


    def encryption_system(self,passw,en=None,dec=None):
        if check_key():
            if en:
                print(f"Key for word '{passw}' is \n {encrypting(passw)}")
                return encrypting(passw)
            if dec:
                print(decrypting(passw))
                return decrypting(passw)
            #if choice.startswith(help_keys[4]) or choice == "my key":
            #    print("Your key is: {}".format(key))

        else:
            new_password()

    def buttons(self):
        self.ui.checkButton.clicked.connect(self.check_sensors)
        self.ui.unlock_Button.clicked.connect(self.get_authorization)



    def get_authorization(self):
        # Create an instance of PasswordDialog
        password_dialog = PasswordDialog()

        # Show the dialog and get the result
        result = password_dialog.exec_()

        # If OK button is clicked, retrieve the password and print it
        if result == QDialog.Accepted:
            password = password_dialog.getPassword()
            password = self.encryption_system(en=True,passw=password)
            print(f"keyv: {self.encryption_system(dec=True,passw=self.launch_password)}, now:{password}")
            try:
                if self.encryption_system(dec=True,passw=self.launch_password) == self.encryption_system(dec=True,passw=password):
                    print("Password: ", password)
                    print("USER HAS BEEN APPROVED")
                    self.autherized = True
                    self.ui.checkButton.show()
                    self.ui.initiate_Button.show()
                    self.ui.fireButton.show()
                    self.ui.unlock_Button.hide()
                else:
                    QMessageBox.warning(self,"Authentecation Error","Entered password is not correct with stored password in database")
            except:
                pass
    def change_fire_password(self):
        if self.autherized:
            # Create an instance of PasswordDialog
            password_dialog = PasswordDialog()

            # Show the dialog and get the result
            result = password_dialog.exec_()

            # If OK button is clicked, retrieve the password and print it
            if result == QDialog.Accepted:
                passwords = password_dialog.getPassword()
                password = self.encryption_system(en=True,passw=passwords)

                print("New Password: ", passwords)
                print("USER HAS BEEN APPROVED")
                self.launch_password = password

                with open("database.key","w") as f:
                    f.write(self.launch_password)
                    f.close()

                QMessageBox.information(self,"Change Password",f"The password {passwords} has been changed")

    def refresh(self):
        print("refreshing UI")
        refresh()
        self.speed = data["speed"]  # Update the self.speed with the latest data value
        self.altitude = data["altitude"]
        self.pressure = data["pressure"]
        self.location = data["location"]
        self.long = data["location"]["long"]
        self.lat = data["location"]["lat"]

        self.ui.speed.setText(f"Speed: {self.speed}")  # Update the speed label with the latest value`
        self.ui.pressure.setText(f"Pressure: {self.pressure}")
        self.ui.altitude.setText(f"Altitude: {self.altitude}")
        self.ui.location.setText(f"Location {self.long} || {self.lat}")
        print("Updated in UI")


    def charts(self):

        from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
        from PyQt5.QtChart import QChart, QChartView, QLineSeries
        from PyQt5.QtCore import Qt

        # Create a QLineSeries and add some data
        series = QLineSeries()
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(4, 4)
        series.append(5, 5)

        # Create a QChart and add the series to it
        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setMargins(QMargins(0, 0, 0, 0))
        chart.legend().hide()

        # Create a QChartView and set the chart as its model
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setFocusPolicy(Qt.NoFocus)
        chart_view.setFrameStyle(QFrame.NoFrame)
        # Create a QVBoxLayout and add the chart view to it
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        chart_view.setFixedSize(190, 140)
        self.ui.status.setLayout(layout)

        def update_chart():
            # Generate a random y value
            y = random.randint(1, 50)

            # Append the new data to the series
            series.append(series.count(), y)
            print(series.count(), y)

            if int(series.count()) < 10:
                return

            # Shift the x-axis of the chart
            chart.axisX().setRange(series.count()-10,series.count())

            # Set the range of the y-axis to the minimum and maximum values of the y-values in the series
            y_values = [point.y() for point in series.pointsVector()]
            chart.axisY().setRange(min(y_values), max(y_values))

            # Resize the chart to fit in the chart view
            # chart.setFixedSize(chart_view.size())

            # Redraw the chart
            chart_view.repaint()

        # Create a QTimer to update the chart every second
        timer = QTimer(self)
        timer.timeout.connect(update_chart)
        timer.start(1000)

    def check_sensors(self):
        QMessageBox.information(self,"Warning","كل الحساسات تعمل بكفائة")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    thred1 = threading.Thread(target=refresh)
    thred1.setDaemon(True)
    thred1.start()
    mainwin = MyForm()
    mainwin.show()
    sys.exit(app.exec_())
