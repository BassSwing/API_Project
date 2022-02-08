import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lon = 37.622513
        self.lat = 55.75322

        self.z = 0

        self.qp = QPixmap()

        self.initUI()
        self.update()

    def initUI(self):
        self.setGeometry(200, 200, 800, 700)
        self.setWindowTitle("T IT")

        self.image = QLabel(self)
        self.image.resize(650, 450)
        self.image.move(75, 50)

    def update(self):
        lon = str(self.lon)
        lat = str(self.lat)
        params = {
            "ll": ",".join([lon, lat]),
            "l": "map",
            "z": self.z,
            "size": ",".join(["650", "450"])
        }
        response = requests.get("http://static-maps.yandex.ru/1.x/", params=params)
        self.qp.loadFromData(response.content)
        self.image.setPixmap(self.qp)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.z != 23:
                self.z += 1
        if event.key() == Qt.Key_PageDown:
            if self.z != 0:
                self.z -= 1

        value = (2 ** (17 - int(self.z)))

        if event.key() == Qt.Key_Up:
            if self.lat + 0.001 * value <= 180:
                self.lat += 0.001 * value

        if event.key() == Qt.Key_Down:
            if self.lat - 0.001 * value >= -180:
                self.lat -= 0.001 * value

        if event.key() == Qt.Key_Right:
            if self.lon + 0.002 * value <= 180:
                self.lon += 0.002 * value

        if event.key() == Qt.Key_Left:
            if self.lon - 0.002 * value >= -180:
                self.lon -= 0.002 * value
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())