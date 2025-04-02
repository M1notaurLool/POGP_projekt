
import socket
from PyQt6 import QtWidgets, QtCore

import games



PORT = 5555

class Okno(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lobby!")
        self.resize(400, 300)

        self._listview = QtWidgets.QListWidget(self)
        self._listview.setGeometry(0, 0, 400, 370)

        self._btn = QtWidgets.QPushButton("Odoslať", self)
        self._btn.clicked.connect(self.start)
        self._btn.setGeometry(320, 270, 80, 30)

        self._message = QtWidgets.QLineEdit("Ahoj", self)
        self._message.setGeometry(80, 273, 240, 25)

        self._address = QtWidgets.QLineEdit("192.168.10.84", self)
        self._address.setGeometry(3, 273, 65, 25)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.periodic)
        self._timer.start(1000)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('0.0.0.0', PORT))  # Počúva na všetkých sieťových rozhraniach

        self.show()

    def button_pressed(self):
        adresa = self._address.text()
        return adresa

    def start(self):

        if __name__ == "__main__":
            g = games.Game(500, 500)
            g.run()






    def add_message(self, address, message):
        """Pridá správu do QListWidgetu."""
        self._listview.addItem(f"{address}: {message}")

    def periodic(self):
        """Periodicky kontroluje prijaté správy zo socketu."""
        try:
            self._sock.settimeout(0.1)
            data, addr = self._sock.recvfrom(1024)
            message = data.decode()
            self.add_message(addr[0], message)
        except socket.timeout:
            pass

app = QtWidgets.QApplication([])
win = Okno()
app.exec()
