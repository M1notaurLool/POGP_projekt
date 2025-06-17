import sys
import socket
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QVBoxLayout
import subprocess
import tkinter as tk

import game
import share

BUTTON_STYLE = """
QPushButton {
    font-size: 20px;
    font-family: 'Poppins';
    font-weight: bold;
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
    font-family: 'Poppins';
    font-weight: bold;
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
        try:
            self.client.sendto("get_id".encode(), self.addr)
            data, _ = self.client.recvfrom(2048)
            return data.decode()
        except socket.error as e:
            print(f"Error getting ID: {e}")
            return None

    def send(self, data):
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

        # Default IP and port
        self._saved_address = share.Share.ip_add if share.Share.ip_add != "0.0.0.0" else "192.168.88.11"
        self._saved_port = share.Share.port if share.Share.port != 0 else 11000

        self.main_window()
        self.showFullScreen()

    def button_pressed(self):
        ip = self._address.text()
        port_text = self._port.text()
        try:
            port = int(port_text)
            self._saved_address = ip
            self._saved_port = port

            share.Share.ip_add = ip
            share.Share.port = port

            print(f"Saved IP: {ip}, PORT: {port}")
        except ValueError:
            print("Please enter a valid port number.")

    def clear(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.hide()

    def main_window(self):
        self.clear()

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

        self._btn_multy_settings = QtWidgets.QPushButton("SETTINGS", self)
        self._btn_multy_settings.clicked.connect(self.multy)
        self._btn_multy_settings.setStyleSheet(BUTTON_STYLE)

        self._btn_server = QtWidgets.QPushButton("SERVER", self)
        self._btn_server.clicked.connect(self.server)
        self._btn_server.setStyleSheet(BUTTON_STYLE + "QPushButton { margin-bottom: 50px; }")

        self._btn_exit = QtWidgets.QPushButton("EXIT", self)
        self._btn_exit.clicked.connect(self.exit)
        self._btn_exit.setStyleSheet(BUTTON_STYLE)

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addSpacing(30)
        main_layout.addWidget(self._btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._btn_multy_settings, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._btn_server, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._btn_exit, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def server_pressed(self):
        ip = self.s_address.text()
        port_text = self.s_port.text()
        try:
            port = int(port_text)
            self._saved_address = ip
            self._saved_port = port

            share.Share.s_ip = ip
            share.Share.s_port = port

            print(f"Saved Server IP: {ip}, PORT: {port}")
        except ValueError:
            print("Please enter a valid port number.")

    def run_server(self):
        ip = self._saved_address
        port = str(self._saved_port)

        subprocess.Popen([sys.executable, "server.py", ip, port])

    def server(self):
        self.clear()

        self.s_address = QtWidgets.QLineEdit(self._saved_address, self)
        self.s_address.setStyleSheet(INPUT)

        self.s_port = QtWidgets.QLineEdit(str(self._saved_port), self)
        self.s_port.setStyleSheet(INPUT)

        self._btn_save = QtWidgets.QPushButton("SAVE", self)
        self._btn_save.clicked.connect(self.server_pressed)
        self._btn_save.setStyleSheet(BUTTON_STYLE)

        self._btn_spusti_server = QtWidgets.QPushButton("START SERVER", self)
        self._btn_spusti_server.clicked.connect(self.run_server)
        self._btn_spusti_server.setStyleSheet(BUTTON_STYLE + "QPushButton { margin-bottom: 50px; }")

        self._btn_back_main = QtWidgets.QPushButton("BACK", self)
        self._btn_back_main.clicked.connect(self.main_window)
        self._btn_back_main.setStyleSheet(BUTTON_STYLE)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addSpacing(30)
        layout.addWidget(self.s_address, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.s_port, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._btn_save, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._btn_spusti_server, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._btn_back_main, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def multy(self):
        self.clear()

        self._address = QtWidgets.QLineEdit(self._saved_address, self)
        self._address.setStyleSheet(INPUT)

        self._port = QtWidgets.QLineEdit(str(self._saved_port), self)
        self._port.setStyleSheet(INPUT)

        self._btn_save = QtWidgets.QPushButton("SAVE", self)
        self._btn_save.clicked.connect(self.button_pressed)
        self._btn_save.setStyleSheet(BUTTON_STYLE + "QPushButton { margin-bottom: 50px; }")

        self._btn_back_main = QtWidgets.QPushButton("BACK", self)
        self._btn_back_main.clicked.connect(self.main_window)
        self._btn_back_main.setStyleSheet(BUTTON_STYLE)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addSpacing(30)
        layout.addWidget(self._address, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._port, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._btn_save, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._btn_back_main, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def exit(self):
        sys.exit()

    def start(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()

        try:
            player.stop()  # Stop music before starting game
        except Exception:
            pass

        self.close()  # Close lobby window

        # Start the game
        g = game.Game(screen_width, screen_height)
        g.run()

app = QtWidgets.QApplication([])

audio_output = QAudioOutput()
player = QMediaPlayer()
player.setAudioOutput(audio_output)

player.setSource(QUrl.fromLocalFile("soundFx/lobby_music.mp3"))
audio_output.setVolume(0.4)

player.setLoops(QMediaPlayer.Loops.Infinite)
player.play()

win = Okno()
win.show()
app.exec()
