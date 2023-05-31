import os
import base64
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
from folium import IFrame

# Create the Folium map
m = folium.Map(location=[52.16008598500544, 50.4998319149017325], zoom_start=17)
walkData = os.path.join('walk.json')
folium.GeoJson(walkData, name='walk').add_to(m)

# Save the map as HTML
m.save("index.html")

# Create the PyQt5 application
app = QApplication([])
window = QMainWindow()

# Create a web view widget
web_view = QWebEngineView()

# Load the HTML file
html_file = 'index.html'
web_view.load(QUrl.fromLocalFile(os.path.abspath(html_file)))

# Set up the layout and add the web view to it
layout = QVBoxLayout()
layout.addWidget(web_view)

# Create a central widget to hold the layout
central_widget = QWidget()
central_widget.setLayout(layout)

# Set the central widget in the main window
window.setCentralWidget(central_widget)

# Show the main window
window.show()

# Start the event loop
app.exec_()
