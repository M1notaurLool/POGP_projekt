import socket

import sys
class Network:
    def __init__(self, okno_instance):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #nacitanie IP address zadanej v PyQt
        self.host = okno_instance.get_saved_address()


        self.port = okno_instance.get_saved_port()

        self.addr = (self.host, self.port)
        self.id = self.connect()


    #Funkcia ktora kontorluje ci je klient pripojeny alebo nie
    def connect(self):
        try:
            self.client.connect(self.addr)
            print(f"Pripojený k: {self.addr}")
            return self.client.recv(2048).decode()
        except Exception as e:
            print(f"Chyba pri pripájaní: {e}")
            sys.exit()
            return "ERROR"


    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            #odoslanie dat cez soket
            self.client.send(str.encode(data))
            #prijatie odpocede od servera
            reply = self.client.recv(2048).decode()
            #vrati odpoved sercera
            return reply
        except socket.error as e:
            #Ak nastane chyba vrati spravu o chybe
            return str(e)