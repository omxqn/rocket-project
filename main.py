import os
import base64
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
from folium import IFrame
import numpy as np
print(np.__version__)

# Create the Folium map
m = folium.Map(location=[52.16008598500544, 7.4998319149017325], zoom_start=17)
walkData = os.path.join('walk.json')
folium.GeoJson(walkData, name='walk').add_to(m)

# Save the map as HTML
m.save("index.html")

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QWebEngineView widget
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

        file_path = "index.html"
        self.webview.load(QUrl.fromLocalFile(file_path))        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# Start the event loop
app.exec_()
