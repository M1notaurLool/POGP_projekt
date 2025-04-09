import socket
import sys

import pygame
from PyQt6 import QtWidgets, QtCore
import game
from network import Network

PORT = 5555

class Okno(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triskáč blast")
        self.setFixedSize(700, 600)

        # Nastavenie pozadia
        self.setStyleSheet("background-image: url('Obrazok/wellcome.png');")

        # Inicializácia hlavného okna
        self.main_windov()

        # Timer pre periodické kontroly správ
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.periodic)
        self._timer.start(1000)

        # Socket na počúvanie správ
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('0.0.0.0', PORT))

        # Defaultné IP a port
        self._saved_address = "127.0.0.1"
        self._saved_port = 11000

        self.show()

    def clear(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.hide()

    def main_windov(self):
        self.clear()

        self._btn_start = QtWidgets.QPushButton("ŠTART", self)
        self._btn_start.clicked.connect(self.start)
        self._btn_start.setGeometry(540, 540, 150, 50)
        self._btn_start.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; background-color:none; border-radius: 5px;")

        self._btn_multy = QtWidgets.QPushButton("MULTY PLAYER", self)
        self._btn_multy.clicked.connect(self.multy)
        self._btn_multy.setGeometry(200, 300, 300, 50)
        self._btn_multy.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; background-color: none; border-radius: 5px;")

        self._btn_exit = QtWidgets.QPushButton("Exit", self)
        self._btn_exit.clicked.connect(self.exit)
        self._btn_exit.setGeometry(200, 400, 300, 50)
        self._btn_exit.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; border-radius: 5px;")

        self._btn_start.show()
        self._btn_multy.show()
        self._btn_exit.show()

    def multy(self):
        self.clear()

        self._address = QtWidgets.QLineEdit("127.0.0.1", self)
        self._address.setGeometry(10, 540, 150, 50)
        self._address.setStyleSheet("font-size: 20px; font-family: 'Comic Sans MS'; border: none; padding-left: 10px;")

        self._port = QtWidgets.QLineEdit("11000", self)
        self._port.setGeometry(170, 540, 120, 50)
        self._port.setStyleSheet("font-size: 20px; font-family: 'Comic Sans MS'; border: none; padding-left: 10px;")

        self._btn_save = QtWidgets.QPushButton("ULOŽIŤ", self)
        self._btn_save.clicked.connect(self.button_pressed)
        self._btn_save.setGeometry(300, 540, 150, 50)
        self._btn_save.setStyleSheet("font-size: 20px; font-family: 'Comic Sans MS'; border: none; border-radius: 5px;")

        self._btn_back_main = QtWidgets.QPushButton("VRÁTIŤ SA", self)
        self._btn_back_main.clicked.connect(self.main_windov)
        self._btn_back_main.setGeometry(540, 540, 150, 50)
        self._btn_back_main.setStyleSheet("font-size: 20px; font-family: 'Comic Sans MS'; border: none; background-color:none; border-radius: 5px;")

        self._address.show()
        self._port.show()
        self._btn_save.show()
        self._btn_back_main.show()

    def button_pressed(self):
        self._saved_address = self._address.text()
        self._saved_port = int(self._port.text())
        print(f"Uložená IP adresa: {self._saved_address}")
        print(f"Uložený PORT: {self._saved_port}")

    def get_saved_address(self):
        return self._saved_address

    def get_saved_port(self):
        return self._saved_port

    def start(self):
        print("Spúšťam hru")
        try:
            network = Network(self)
            print(f"Pripojenie na server: {self.get_saved_address()}:{self.get_saved_port()}")
            g = game.Game(1000, 1000, self)
            g.run()
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

    def add_message(self, ip, msg):
        print(f"[{ip}]: {msg}")

    def exit(self):
        sys.exit()


app = QtWidgets.QApplication([])
win = Okno()
sys.exit(app.exec())