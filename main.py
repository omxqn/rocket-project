import random
import sys
import time
import threading

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *
from ui import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.Qt import *
from password_manager import PasswordDialog
# pip install PyQtChart
from cryption import *
from PyQt5 import *


# pip install PyQtChart
data = {"speed": 0, "altitude": 0, "pressure": 0, "location": {"log": "0", "lat": "0"}}


def refresh():
    print("Updating")
    data["speed"] = random.randint(150, 300)
    data["altitude"] = random.randint(100, 150)
    data["pressure"] = random.randint(1000, 2000)
    data["location"]["long"] = str(random.randint(0, 90))
    data["location"]["lat"] = str(random.randint(0, 90))


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

        # Create a QLineSeries and add some data
        series2 = QLineSeries()
        series2.append(0, 6)
        series2.append(2, 4)
        series2.append(3, 8)
        series2.append(4, 4)
        series2.append(5, 5)

        # Create a QLineSeries and add some data
        series3 = QLineSeries()
        series3.append(0, 6)
        series3.append(2, 4)
        series3.append(3, 8)
        series3.append(4, 4)
        series3.append(5, 5)

        # Create a QLineSeries and add some data
        series4 = QLineSeries()
        series4.append(0, 6)
        series4.append(2, 4)
        series4.append(3, 8)
        series4.append(4, 4)
        series4.append(5, 5)

        # Create a QChart and add the series to it
        chart = QChart()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setMargins(QMargins(0, 0, 0, 0))
        chart.legend().hide()

        # Create a QChart and add the series to it
        chart2 = QChart()
        chart2.addSeries(series2)
        chart2.createDefaultAxes()
        chart2.setMargins(QMargins(0, 0, 0, 0))
        chart2.legend().hide()

        # Create a QChart and add the series to it
        chart3 = QChart()
        chart3.addSeries(series3)
        chart3.createDefaultAxes()
        chart3.setMargins(QMargins(0, 0, 0, 0))
        chart3.legend().hide()

        # Create a QChart and add the series to it
        chart4 = QChart()
        chart4.addSeries(series4)
        chart4.createDefaultAxes()
        chart4.setMargins(QMargins(0, 0, 0, 0))
        chart4.legend().hide()

        # Create a QChartView and set the chart as its model
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setFocusPolicy(Qt.NoFocus)
        chart_view.setFrameStyle(QFrame.NoFrame)
        chart_view.setFixedSize(190, 140)

        # Create a QChartView and set the chart as its model
        chart_view2 = QChartView(chart2)
        chart_view2.setRenderHint(QPainter.Antialiasing)
        chart_view2.setFocusPolicy(Qt.NoFocus)
        chart_view2.setFrameStyle(QFrame.NoFrame)
        chart_view2.setFixedSize(190, 140)


        # Create a QChartView and set the chart as its model
        chart_view3 = QChartView(chart3)
        chart_view3.setRenderHint(QPainter.Antialiasing)
        chart_view3.setFocusPolicy(Qt.NoFocus)
        chart_view3.setFrameStyle(QFrame.NoFrame)
        chart_view3.setFixedSize(190, 140)


        # Create a QChartView and set the chart as its model
        chart_view4 = QChartView(chart4)
        chart_view4.setRenderHint(QPainter.Antialiasing)
        chart_view4.setFocusPolicy(Qt.NoFocus)
        chart_view4.setFrameStyle(QFrame.NoFrame)
        chart_view4.setFixedSize(190, 140)




        # Create a QVBoxLayout and add the chart view to it
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        layout.addWidget(chart_view2)
        layout.addWidget(chart_view3)
        layout.addWidget(chart_view4)

        # Set the layout on the central widget
        central_widget = self.ui.centralwidget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        chart_view.setParent(self)
        chart_view.move(10,70)

        chart_view2.setParent(self)
        chart_view2.move(200, 70)

        chart_view3.setParent(self)
        chart_view3.move(10, 200)

        chart_view4.setParent(self)
        chart_view4.move(200, 200)


        #layout.removeWidget(chart_view)
        #chart_view.unsetLayoutDirection()
        #chart_view.move(50,50)
        self.ui.status.setLayout(layout)

        #chart_view.setGeometry(QRect(190, 140, 121, 81))
        def update_chart():
            speed = data["speed"]  # Update the self.speed with the latest data value
            altitude = data["altitude"]
            pressure = data["pressure"]
            tempreture = random.randint(29,80)


            # Generate a random y value
            y = random.randint(1, 50)
            y1 = random.randint(1, 50)
            y2 = random.randint(1, 50)
            y3 = random.randint(1, 50)
            # Append the new data to the series
            series.append(series.count(), speed)
            series2.append(series2.count(), altitude)
            series3.append(series3.count(), pressure)
            series4.append(series4.count(), tempreture)


            if int(series.count()) < 10:
                return

            # Shift the x-axis of the chart
            chart.axisX().setRange(series.count()-10,series.count())
            chart2.axisX().setRange(series2.count() - 10, series2.count())
            chart3.axisX().setRange(series3.count() - 10, series3.count())
            chart4.axisX().setRange(series4.count() - 10, series4.count())

            # Set the range of the y-axis to the minimum and maximum values of the y-values in the series
            y_values = [point.y() for point in series.pointsVector()]
            y_values2 = [point.y() for point in series2.pointsVector()]
            y_values3 = [point.y() for point in series3.pointsVector()]
            y_values4 = [point.y() for point in series4.pointsVector()]
            chart.axisY().setRange(min(y_values), max(y_values))
            chart2.axisY().setRange(min(y_values2), max(y_values2))
            chart3.axisY().setRange(min(y_values3), max(y_values3))
            chart4.axisY().setRange(min(y_values4), max(y_values4))
            # Resize the chart to fit in the chart view
            # chart.setFixedSize(chart_view.size())

            # Redraw the chart
            chart_view.repaint()
            chart_view2.repaint()
            chart_view3.repaint()
            chart_view4.repaint()


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
