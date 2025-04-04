import socket


import sys
class Network:
    def __init__(self, okno_instance):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = okno_instance.get_saved_address()
        self.port = okno_instance.get_saved_port()
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Error during connection: {e}")
            from games import Game
            Game.close_game()
            return "ERROR"

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            print(f"Error during send: {e}")
            return str(e)