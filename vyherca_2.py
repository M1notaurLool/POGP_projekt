import subprocess
import sys
import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class Okno(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triskáč blast")
        self.setFixedSize(600, 600)
        self.init_ui()

    def init_ui(self):
        # 1) Centrálny widget a layout
        central = QWidget(self)
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(20)

        # 2) "Výherca!" label
        label = QLabel("Výherca!", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white; font-size: 60px; font-weight: bold;")
        vbox.addStretch()  # odsadenie hore
        vbox.addWidget(label)

        # 3) Podnadpis
        label2 = QLabel("Hru vyhral hráč číslo 2!", self)
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label2.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        vbox.addWidget(label2)

        # 4) Tlačidlo vrátania
        btn = QPushButton("Vrátiť do hlavného menu", self)
        btn.setFixedSize(300, 50)
        btn.clicked.connect(self.return_to_lobby)
        vbox.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        vbox.addStretch()  # odsadenie dole

    def return_to_lobby(self):
        self.hide()
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "lobby.py")])

    def closeEvent(self, event):
        # debug výpisy...
        path_to_lobby = os.path.join(os.path.dirname(__file__), "lobby.py")
        if os.path.isfile(path_to_lobby):
            subprocess.Popen([sys.executable, path_to_lobby])
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = Okno()
    okno.show()
    app.exec()
