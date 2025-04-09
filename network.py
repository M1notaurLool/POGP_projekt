import socket

class Network:
    def __init__(self, okno_instance):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Inicializácia host hodnotou z okna
        self.host = okno_instance.get_saved_address()
        self.port = okno_instance.get_saved_port()
        self.addr = (self.host, self.port)
        self.id = self.connect()  # Získaj svoje ID od servera

    def connect(self):
        # Implementuj logiku pripojenia, prípadne jednoducho zavolaj metódu get_id()
        return self.get_id()

    def get_id(self):
        """Získaj ID od servera pri prvom spojení."""
        try:
            self.client.sendto("get_id".encode(), self.addr)
            data, _ = self.client.recvfrom(2048)
            return data.decode()
        except socket.error as e:
            print(f"Chyba pri získavaní ID: {e}")
            return None

    def send(self, data):
        """
        Pošli dáta serveru a získaj odpoveď.
        :param data: str (napr. "0:100,100")
        :return: str
        """
        try:
            self.client.sendto(data.encode(), self.addr)
            reply, _ = self.client.recvfrom(2048)
            return reply.decode()
        except socket.error as e:
            return str(e)
