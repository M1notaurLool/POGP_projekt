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
        self.showFullScreen()
        self.init_ui()

        # Globálny štýl pre QMainWindow a QPushButton
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
        # Centrálny widget a layout
        central = QWidget(self)
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(20)

        # Nadpis
        label = QLabel("PREHRA!", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            color: white;
            font-size: 100px;
            font-weight: bold;
            background-color: transparent;
        """)
        vbox.addStretch()
        vbox.addWidget(label)

        # Tlačidlo na návrat do menu
        btn = QPushButton("Vrátiť do hlavného menu", self)
        btn.setFixedSize(300, 50)
        btn.clicked.connect(self.return_to_lobby)
        vbox.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addStretch()

    def return_to_lobby(self):
        self.hide()
        subprocess.Popen([sys.executable, "lobby.py"])

    def closeEvent(self, event):
        path_to_lobby = os.path.join(os.path.dirname(__file__), "lobby.py")
        if os.path.isfile(path_to_lobby):
            subprocess.Popen([sys.executable, path_to_lobby])
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = Okno()
    okno.show()
    app.exec()
