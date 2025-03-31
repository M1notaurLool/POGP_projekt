import socket
import threading
from config import UDP_IP, UDP_PORT

class Network:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.clients = set()
        self.running = True

        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while self.running:
            data, addr = self.sock.recvfrom(1024)
            self.clients.add(addr)
            for client in self.clients:
                if client != addr:
                    self.sock.sendto(data, client)

    def send(self, message):
        for client in self.clients:
            self.sock.sendto(message.encode(), client)

    def close(self):
        self.running = False
        self.sock.close()