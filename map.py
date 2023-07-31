

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
from math import sqrt,sin,cos,radians,atan2

class PathTracker(QMainWindow):
    def __init__(self, gps_coordinates):
        super().__init__()

        self.setWindowTitle("Rocket Flight Path")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.path = []
        self.gps_coordinates = gps_coordinates

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_flight_path)
        self.timer.start(1)  # Refresh rate: 1000 milliseconds (1 second)

        self.current_index = 0
        self.is_flight_started = False

        # Calculate the scaling factors for latitude and longitude
        self.latitude_min = min(coord[0] for coord in gps_coordinates)
        self.latitude_max = max(coord[0] for coord in gps_coordinates)
        self.longitude_min = min(coord[1] for coord in gps_coordinates)
        self.longitude_max = max(coord[1] for coord in gps_coordinates)
        print(self.latitude_max,self.latitude_min)
        self.latitude_scale = self.view.height() / (self.latitude_max - self.latitude_min)
        self.longitude_scale = self.view.width() / (self.longitude_max - self.longitude_min)

    def calculate_path_length(self):
        total_distance = 0.0

        for i in range(1, len(self.path)):
            prev_point = self.path[i - 1]
            curr_point = self.path[i]
            lat1, lon1 = self.reverse_scale(prev_point.x(), prev_point.y())
            lat2, lon2 = self.reverse_scale(curr_point.x(), curr_point.y())

            # Convert latitude and longitude from degrees to radians
            lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

            # Haversine formula to calculate distance between two points
            dlat = lat2_rad - lat1_rad
            dlon = lon2_rad - lon1_rad
            a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = 6371.0 * c  # Earth's radius = 6371.0 km

            total_distance += distance

        return total_distance

    def reverse_scale(self, x, y):
        latitude = y / self.latitude_scale + self.latitude_min
        longitude = x / self.longitude_scale + self.longitude_min
        return latitude, longitude

    def update_flight_path(self):
        if not self.is_flight_started:
            return

        if self.current_index >= len(self.gps_coordinates):
            # Flight completed, stop the timer
            self.timer.stop()
            return

        gps_point = self.gps_coordinates[self.current_index]
        x = (gps_point[1] - self.longitude_min) * self.longitude_scale
        y = (gps_point[0] - self.latitude_min) * self.latitude_scale

        self.path.append(QPointF(x, y))
        self.current_index += 1

        # Redraw the flight path and markers
        self.draw_flight_path()

        if len(self.path) > 1:
            self.draw_markers()

    def start_flight(self):
        self.is_flight_started = True

    def draw_flight_path(self):
        self.scene.clear()

        # Create a QPainterPath for the flight path
        path = QPainterPath()
        path.moveTo(self.path[0])  # Move to the starting point
        for point in self.path[1:]:
            path.lineTo(point)  # Draw lines between consecutive points

        # Draw the flight path
        pen = QPen(QColor(255, 0, 0))  # Red color for the flight path
        pen.setWidth(2)
        self.scene.addPath(path, pen)

        # Draw the current rocket position
        if len(self.path) > 0:
            current_point = self.path[-1]
            pen = QPen(Qt.black)
            pen.setWidth(2)
            self.scene.addEllipse(current_point.x() - 5, current_point.y() - 5, 10, 10, pen)

        # Set the scene's boundaries to fit the flight path
        self.view.setSceneRect(QRectF(path.boundingRect()))

    def draw_markers(self):
        if self.current_index < len(self.gps_coordinates):
            gps_point = self.gps_coordinates[self.current_index]
            x = (gps_point[1] - self.longitude_min) * self.longitude_scale
            y = (gps_point[0] - self.latitude_min) * self.latitude_scale
            brush = QBrush(QColor(0, 0, 255))  # Blue color for the marker
            marker = self.scene.addEllipse(x - 2, y - 2, 4, 4, QPen(Qt.NoPen), brush)
            marker.setZValue(1)  # Ensure the marker is drawn on top of the flight path

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Recalculate the scaling factors when the window is resized
        latitude_range = self.latitude_max - self.latitude_min
        longitude_range = self.longitude_max - self.longitude_min

        # Check if the latitude range is zero to avoid division by zero
        if latitude_range != 0:
            self.latitude_scale = self.view.height() / latitude_range
        else:
            self.latitude_scale = 1.0

        if longitude_range != 0:
            self.longitude_scale = self.view.width() / longitude_range
        else:
            self.longitude_scale = 1.0


if __name__ == '__main__':
    gps_coordinates = [
        (34.0522, -118.2437),  # Los Angeles
        (35.0522, -117.2437),
        (30.0522, -100.2437),
        (30.0, -100.0)

    ]

    app = QApplication(sys.argv)
    tracker = PathTracker(gps_coordinates)
    tracker.show()
    tracker.start_flight()  # Start the flight

    sys.exit(app.exec())
