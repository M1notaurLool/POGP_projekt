import sys
import socket
from PyQt6 import QtWidgets
import game
import share

class Network:
    def __init__(self, host="192.168.88.11", port=11000):
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
        self.setFixedSize(700, 600)
        self.setStyleSheet("background-image: url('Obrazok/wellcome.png');")

        # Predvolené IP a port
        self._saved_address = "127.0.0.1"
        self._saved_port = 11000

        self.main_window()
        self.show()

    def button_pressed(self):
        """Uloží IP adresu a port zo vstupov do globálneho configu."""
        ip = self._address.text()
        port_text = self._port.text()
        try:
            port = int(port_text)
            self._saved_address = ip
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
        self._btn_start = QtWidgets.QPushButton("ŠTART", self)
        self._btn_start.clicked.connect(self.start)
        self._btn_start.setGeometry(540, 540, 150, 50)
        self._btn_start.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; background-color:none; border-radius: 5px;"
        )

        # MULTY PLAYER tlačidlo
        self._btn_multy = QtWidgets.QPushButton("MULTY PLAYER", self)
        self._btn_multy.clicked.connect(self.multy)
        self._btn_multy.setGeometry(200, 300, 300, 50)
        self._btn_multy.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; "
            "border-radius: 5px; background-color: black; color: white;"
        )

        # EXIT tlačidlo
        self._btn_exit = QtWidgets.QPushButton("EXIT", self)
        self._btn_exit.clicked.connect(self.exit)
        self._btn_exit.setGeometry(200, 400, 300, 50)
        self._btn_exit.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border: none; border-radius: 5px;"
        )

        self._btn_start.show()
        self._btn_multy.show()
        self._btn_exit.show()

    def multy(self):
        self.clear()

        # Vstupy pre IP a port
        self._address = QtWidgets.QLineEdit(self._saved_address, self)
        self._address.setGeometry(10, 540, 150, 50)
        self._address.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; padding-left: 10px;"
        )

        self._port = QtWidgets.QLineEdit(str(self._saved_port), self)
        self._port.setGeometry(170, 540, 120, 50)
        self._port.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; padding-left: 10px;"
        )

        # ULOŽIŤ tlačidlo
        self._btn_save = QtWidgets.QPushButton("ULOŽIŤ", self)
        self._btn_save.clicked.connect(self.button_pressed)
        self._btn_save.setGeometry(300, 540, 150, 50)
        self._btn_save.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border-radius: 5px;"
        )

        # SPÄŤ tlačidlo
        self._btn_back_main = QtWidgets.QPushButton("VRÁTIŤ SA", self)
        self._btn_back_main.clicked.connect(self.main_window)
        self._btn_back_main.setGeometry(540, 540, 150, 50)
        self._btn_back_main.setStyleSheet(
            "font-size: 20px; font-family: 'Comic Sans MS'; border-radius: 5px;"
        )

        self._address.show()
        self._port.show()
        self._btn_save.show()
        self._btn_back_main.show()

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
g = game.Game(1000, 1000)
g.run()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = Okno()
    app.exec()
