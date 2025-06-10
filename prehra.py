import subprocess
import sys
import os
import pygame
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class Okno(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.return_to_lobby_requested = False  # kontrolný príznak

        self.setWindowTitle("Triskáč blast")
        self.showFullScreen()
        self.init_ui()

        # 🔊 Spusti prehrávanie hudby
        pygame.mixer.init()
        pygame.mixer.music.load("soundFx/lose.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.setStyleSheet("""
            QMainWindow {
                background-image: url('Obrazok/wellcome.png');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }

            QPushButton {
                background-color: white;
                color: black;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: lightgray;
            }
        """)

    def init_ui(self):
        central = QWidget(self)
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(20)

        label = QLabel("VÝHRA!", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            color: white;
            font-size: 100px;
            font-weight: bold;
            background-color: transparent;
        """)
        vbox.addStretch()
        vbox.addWidget(label)

        btn = QPushButton("Vrátiť do hlavného menu", self)
        btn.setFixedSize(300, 50)
        btn.clicked.connect(self.return_to_lobby)
        vbox.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addStretch()

    def return_to_lobby(self):
        self.return_to_lobby_requested = True  # nastav príznak
        pygame.mixer.music.stop()
        self.close()

    def closeEvent(self, event):
        pygame.mixer.music.stop()
        event.accept()  # len akceptuj — neštartuj lobby tu!

if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = Okno()
    okno.show()
    app.exec()

    if okno.return_to_lobby_requested:
        path_to_lobby = os.path.join(os.path.dirname(__file__), "lobby.py")
        if os.path.isfile(path_to_lobby):
            subprocess.Popen([sys.executable, path_to_lobby])
