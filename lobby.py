import sys
import socket
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

import game
import share

BUTTON_STYLE = """
QPushButton {
    font-size: 20px;
    font-family: 'Comic Sans MS';
    border: 1px solid white;
    color: white;
    padding: 15px 20px;
    width: 300px;
}
QPushButton:hover {
    background-color: #333333;
    cursor: pointer;
}
QPushButton:pressed {
    background-color: #222222;
    padding-left: 17px;
    padding-top: 17px;
}
"""

INPUT = """
QLineEdit {
    font-size: 20px;
    font-family: 'Comic Sans MS';
    border: 1px solid white;
    background-color: transparent;
    color: white;
    padding: 15px 20px;
    width: 300px;
}
QLineEdit:hover {
    background-color: #333333;
    cursor: pointer;
}

QLineEdit:focus {
    background-color: #333333;
    border: 4px solid white;
}
"""


class Network:
    def __init__(self, host="0.0.0.0", port=11000):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.id = self.get_id()

    def get_id(self):
        """Získa ID od servera pri prvom spojení."""
        try:
            self.client.sendto("get_id".encode(), self.addr)
            data, _ = self.client.recvfrom(2048)
            return data.decode()
        except socket.error as e:
            print(f"Chyba pri získavaní ID: {e}")
            return None

    def send(self, data):
        """Odošle dáta na server a prijme odpoveď."""
        try:
            self.client.sendto(data.encode(), self.addr)
            reply, _ = self.client.recvfrom(2048)
            return reply.decode()
        except socket.error as e:
            return str(e)

class Okno(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triskáč blast")
        self.setObjectName("MainWindow")
        self.setFixedSize(700, 600)
        self.setStyleSheet("""
            #MainWindow {
                background-image: url('Obrazok/wellcome.png');
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        # Predvolené IP a port
        self._saved_address = "192.168.88.11"
        self._saved_port = 11000

        self.main_window()
        self.showFullScreen()

    def button_pressed(self):
        """Uloží IP adresu a port zo vstupov do globálneho configu."""
        ip = self._address.text()
        port_text = self._port.text()
        try:
            port = int(port_text)
            self._saved_address =   ip
            self._saved_port = port

            share.Share.ip_add = ip
            share.Share.port = port

            print(f"Uložená IP adresa: {ip}, PORT: {port}")
        except ValueError:
            print("Zadaj platný číselný port.")

    def get_saved_address(self):
        return self._saved_address

    def get_saved_port(self):
        return self._saved_port

    def clear(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.hide()

    def main_window(self):
        self.clear()

        # ŠTART tlačidlo
        self._btn_start = QtWidgets.QPushButton("START", self)
        self._btn_start.clicked.connect(self.start)
        self._btn_start.setStyleSheet(BUTTON_STYLE +
                                      "QPushButton {"
                                      "background-color: white;"
                                      "color: black;"
                                      "}"
                                      "QPushButton:hover {"
                                      "background-color: transparent;"
                                      "color: white;"
                                      "}"
                                      )

        # MULTI PLAYER tlačidlo
        self._btn_multy_settings = QtWidgets.QPushButton("SETTINGS", self)
        self._btn_multy_settings.clicked.connect(self.multy)
        self._btn_multy_settings.setStyleSheet(BUTTON_STYLE +
                                               "QPushButton {"
                                               "margin-bottom: 50px;"
                                               "}"
                                               )

        # EXIT tlačidlo
        self._btn_exit = QtWidgets.QPushButton("EXIT", self)
        self._btn_exit.clicked.connect(self.exit)
        self._btn_exit.setStyleSheet(BUTTON_STYLE)

        # Vertikálne: vystredovanie do stredu
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addSpacing(30)
        main_layout.addWidget(self._btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._btn_multy_settings, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._btn_exit, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        # Použije layout na celé okno
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)  # <- required if you're in QMainWindow

    def multy(self):
        self.clear()

        # Vstupy pre IP a port
        self._address = QtWidgets.QLineEdit(self._saved_address, self)
        self._address.setStyleSheet(INPUT)

        self._port = QtWidgets.QLineEdit(str(self._saved_port), self)
        self._port.setStyleSheet(INPUT)

        # ULOŽIŤ tlačidlo
        self._btn_save = QtWidgets.QPushButton("ULOŽIŤ", self)
        self._btn_save.clicked.connect(self.button_pressed)
        self._btn_save.setStyleSheet(BUTTON_STYLE +
                                               "QPushButton {"
                                               "margin-bottom: 50px;"
                                               "}"
                                               )

        # SPÄŤ tlačidlo
        self._btn_back_main = QtWidgets.QPushButton("VRÁTIŤ SA", self)
        self._btn_back_main.clicked.connect(self.main_window)
        self._btn_back_main.setStyleSheet(BUTTON_STYLE)

        multy = QVBoxLayout()
        multy.addStretch()
        multy.addSpacing(30)
        multy.addWidget(self._address, alignment=Qt.AlignmentFlag.AlignCenter)
        multy.addWidget(self._port, alignment=Qt.AlignmentFlag.AlignCenter)
        multy.addWidget(self._btn_save, alignment=Qt.AlignmentFlag.AlignCenter)
        multy.addWidget(self._btn_back_main, alignment=Qt.AlignmentFlag.AlignCenter)
        multy.addStretch()

        # Použije layout na celé okno
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(multy)
        self.setCentralWidget(central_widget)

    def exit(self):
        sys.exit()

    def start(self):

        g = game.Game(500, 500)  # Očakávame, že trieda Game existuje v games.py
        g.run()  # Spustíme hru


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



