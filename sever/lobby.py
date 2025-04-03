import socket

import pygame
from PyQt6 import QtWidgets, QtCore
import games
from networks import Network

PORT = 5555


class Okno(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triskáč blast")
        self.resize(700, 600)

        #nastavenie pozadia
        self.setStyleSheet("background-image: url('Obrazok/wellcome.png');")


        # Tlačidlo na spustenie hry
        self._btn_start = QtWidgets.QPushButton("ŠTART", self)
        self._btn_start.clicked.connect(self.start)
        self._btn_start.setGeometry(540, 540, 150, 50)
        self._btn_start.setStyleSheet("font-size: 20px; font-family: 'Comic Sans MS'; border: none; background-color:none; border-radius: 5px; ")



        # Tlačidlo na uloženie IP
        self._btn_nastavenia = QtWidgets.QPushButton("Nastavenia", self)
        self._btn_nastavenia.clicked.connect(self.options)
        self._btn_nastavenia.setGeometry(300, 400, 150, 50)
        self._btn_nastavenia.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; border-radius: 5px;")


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

    def clear(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.hide()

    def main_windov(self):
        self.clear()

        # Tlačidlo na spustenie hry
        self._btn_start = QtWidgets.QPushButton("ŠTART", self)
        self._btn_start.clicked.connect(self.start)
        self._btn_start.setGeometry(540, 540, 150, 50)
        self._btn_start.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; background-color:none; border-radius: 5px; ")

        # Tlačidlo na uloženie IP
        self._btn_save = QtWidgets.QPushButton("Nastavenia", self)
        self._btn_save.clicked.connect(self.options)
        self._btn_save.setGeometry(300, 400, 150, 50)
        self._btn_save.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; border-radius: 5px;")

        self._btn_save.show()
        self._btn_start.show()

    def options(self):
        self.clear()

        # Pole pre nastavenie IP adresy
        self._address = QtWidgets.QLineEdit("127.0.0.1", self)
        self._address.setGeometry(10, 540, 150, 50)
        self._address.setStyleSheet(
                "font-size: 20px; font-family: 'Comic Sans MS'; border: none; padding-left: 10px;")

        self._port = QtWidgets.QLineEdit("11000", self)
        self._port.setGeometry(170, 540, 120, 50)
        self._port.setStyleSheet(
                "font-size: 20px; font-family: 'Comic Sans MS'; border: none; padding-left: 10px;")

            # Tlačidlo na uloženie IP
        self._btn_save = QtWidgets.QPushButton("ULOŽIŤ", self)
        self._btn_save.clicked.connect(self.button_pressed)
        self._btn_save.setGeometry(300, 540, 150, 50)
        self._btn_save.setStyleSheet(
                "font-size: 20px; font-family: 'Comic Sans MS'; border: none; border-radius: 5px;")

        # Tlačidlo na vratenie do main
        self._btn_back_main = QtWidgets.QPushButton("VRATIT SA", self)
        self._btn_back_main.clicked.connect(self.main_windov)
        self._btn_back_main.setGeometry(540, 540, 150, 50)
        self._btn_back_main.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; background-color:none; border-radius: 5px; ")

        # Uložená IP adresa a port
        self._saved_address = "127.0.0.1"  # Defaultná IP adresa
        self._saved_port = 11000

            # 4️⃣ Zobrazenie nových prvkov
        self._address.show()
        self._port.show()
        self._btn_save.show()
        self._btn_back_main.show()



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