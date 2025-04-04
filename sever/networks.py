import pygame

import socket



class Network:
    def __init__(self, okno_instance):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.88.11"  # Get the server IP
        self.port = 11000  # Get the server port
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Error connecting: {e}")
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
            print(f"Error sending data: {e}")
            return str(e)




