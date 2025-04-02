import socket

import pygame
from PyQt6 import QtWidgets, QtCore
import games
from networks import Network

PORT = 5555

class Okno(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lobby!")
        self.resize(400, 300)

        self._listview = QtWidgets.QListWidget(self)
        self._listview.setGeometry(0, 0, 400, 370)

        self._btn_start = QtWidgets.QPushButton("Spustiť hru", self)
        self._btn_start.clicked.connect(self.start)
        self._btn_start.setGeometry(320, 270, 80, 30)

        self._btn_save = QtWidgets.QPushButton("Uložiť IP", self)
        self._btn_save.clicked.connect(self.button_pressed)
        self._btn_save.setGeometry(200, 270, 80, 30)

        self._message = QtWidgets.QLineEdit("Ahoj", self)
        self._message.setGeometry(80, 273, 100, 25)

        self._address = QtWidgets.QLineEdit("127.0.0.1", self)
        self._address.setGeometry(3, 273, 80, 25)

        self._saved_address = "127.0.0.1"  # Defaultná IP adresa

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.periodic)
        self._timer.start(1000)

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('0.0.0.0', PORT))  # Počúva na všetkých sieťových rozhraniach

        self.show()

    def button_pressed(self):
        """Uloží IP adresu zo vstupu do premennej."""
        self._saved_address = self._address.text()
        print(f"Uložená IP adresa: {self._saved_address}")
        return self._saved_address

    def get_saved_address(self):
        """Vráti poslednú uloženú IP adresu."""
        return self._saved_address

    def start(self):
        print("🔄 Spúšťam hru...")
        try:
            g = games.Game(500, 500, self) # Očakávame, že trieda Game existuje v games.py
            g.run()  # Spustíme hru
        except Exception as e:
            print(f"❌ Chyba pri spúšťaní hry: {e}")
            pygame.quit()

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
win = Okno()  # Vytvoríme GUI okno
network = Network(win)  # Posielame inštanciu do Network
app.exec()
