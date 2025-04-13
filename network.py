import socket

from shared_state import SharedState


class Network:

    def __init__(self):
        self.ip = []
        self.ip.append(SharedState.s)
        print(self.ip)





        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = SharedState.s

        self.port = 11000
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

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

n = Network()