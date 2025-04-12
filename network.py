import socket


class Network:
    def __init__(self, host="127.0.0.1", port=11000):
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
