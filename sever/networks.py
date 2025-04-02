import socket

import sys
class Network:
    def __init__(self, okno_instance):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = okno_instance.get_saved_address()  # Použijeme metódu na získanie IP
        self.port = 11000
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            print(f"✅ Pripojený k: {self.addr}")
            return self.client.recv(2048).decode()
        except Exception as e:
            print(f"❌ Chyba pri pripájaní: {e}")
            sys.exit()
            return "ERROR"


    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
