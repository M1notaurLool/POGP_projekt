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

        # Tlačidlo na spustenie hry
        self._btn_start = QtWidgets.QPushButton("Spustiť hru", self)
        self._btn_start.clicked.connect(self.start)
        self._btn_start.setGeometry(320, 270, 80, 30)

        # Tlačidlo na uloženie IP
        self._btn_save = QtWidgets.QPushButton("Uložiť IP", self)
        self._btn_save.clicked.connect(self.button_pressed)
        self._btn_save.setGeometry(203, 270, 80, 30)

        # Pole pre nastavenie IP adresy
        self._address = QtWidgets.QLineEdit("127.0.0.1", self)
        self._address.setGeometry(3, 273, 100, 25)

        self._port = QtWidgets.QLineEdit("11000", self)
        self._port.setGeometry(113, 273, 80, 25)

        # Uložená IP adresa a port
        self._saved_address = "127.0.0.1"  # Defaultná IP adresa
        self._saved_port = 11000

        # Timer pre periodické kontroly správ
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.periodic)
        self._timer.start(1000)

        # Socket na počúvanie správ
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('0.0.0.0', PORT))  # Počúva na všetkých sieťových rozhraniach

        self.show()

    #funkcia ked stlacim tlacidlo ulozi z riadku v pyqt do premennej hodnoty
    def button_pressed(self):
        """Uloží IP adresu zo vstupu do premennej."""
        self._saved_address = self._address.text()
        self._saved_port = int(self._port.text())
        print(f"Uložená IP adresa: {self._saved_address}")
        print(f"Uloženy PORT: {self._saved_port}")

    #vracia hodnotu address
    def get_saved_address(self):
        """Vráti uloženú IP adresu."""
        return self._saved_address


    #vracia hodnotu portu
    def get_saved_port(self):
        """Vráti uložený port."""
        return self._saved_port

    #zapinanie hry pygame a pripajanie na server
    def start(self):
        """Spustí hru a pripojí sa na server."""
        print("Spúšťam hru")
        try:
            # Vytvorte objekt Network až po stlačení tlačidla
            network = Network(self)  # Odovzdáme Okno inštanciu
            print(f"Pripojenie na server: {self.get_saved_address()}:{self.get_saved_port()}")
            g = games.Game(1000, 1000, self)  # Očakávame, že trieda Game existuje v games.py
            g.run()  # Spustíme hru
        except Exception as e:
            print(f"Chyba pri spúšťaní hry: {e}")

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
app.exec()  # Spustíme aplikáciu
