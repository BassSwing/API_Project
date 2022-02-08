import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QComboBox
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lon = 37.622513
        self.lat = 55.75322

        self.z = 17

        self.qp = QPixmap()

        self.initUI()
        self.update()

    def initUI(self):
        self.setGeometry(200, 200, 800, 700)
        self.setWindowTitle("T IT")
        self.typeMap = 'map'

        self.image = QLabel(self)
        self.image.resize(650, 450)
        self.image.move(75, 50)

        self.combobox = QComboBox(self)
        self.combobox.move(625, 510)
        self.combobox.addItems(['map', 'sat', 'skl'])
        self.combobox.setFocusPolicy(Qt.NoFocus)
        self.combobox.activated[str].connect(self.changeMapType)

        self.line = QLineEdit(self)
        self.line.resize(200, 40)
        self.line.move(20, 580)
        self.line.setFocusPolicy(Qt.ClickFocus)

        self.button = QPushButton("Искать", self)
        self.button.resize(80, 40)
        self.button.move(280, 580)
        self.button.clicked.connect(self.update)
        self.button.setFocusPolicy(Qt.NoFocus)


    def update(self):
        self.line.clearFocus()
        try:
            if str(self.line.text()) != "":
                coords = requests.get(
                    f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={str(self.line.text())}&format=json").json()[
                    "response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
                self.lon = coords[0]
                self.lat = coords[1]
                self.line.setText("")
        except:
            pass

        lon = str(self.lon)
        lat = str(self.lat)
        params = {
            "ll": ",".join([lon, lat]),
            "l": self.typeMap,
            "z": self.z,
            "size": ",".join(["650", "450"])
        }
        self.lon = float(self.lon)
        self.lat = float(self.lat)
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

    def changeMapType(self, type):
        self.typeMap = type
        self.update()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
