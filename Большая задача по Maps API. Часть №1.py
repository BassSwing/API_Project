import sys
import requests
from io import BytesIO
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PIL import Image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.coords = ["37.622513", "55.75322"]
        self.delta = "0.002"

        self.qp = QPixmap()

        self.initUI()
        self.update()

    def initUI(self):
        self.setGeometry(200, 200, 800, 800)
        self.setWindowTitle("TIT")

        self.image = QLabel(self)
        self.image.resize(450, 450)
        self.image.move(175, 175)

    def update(self):
        lon = self.coords[0]
        lat = self.coords[1]
        params = {
            "ll": ",".join([lon, lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map",
            "size": ",".join(["450", "450"])
        }
        response = requests.get("http://static-maps.yandex.ru/1.x/", params=params)
        self.qp.loadFromData(response.content)
        self.image.setPixmap(self.qp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
