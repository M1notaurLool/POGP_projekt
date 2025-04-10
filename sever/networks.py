import socket


import sys
class Network:
    def __init__(self, okno_instance):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #nacitanie IP address zadanej v PyQt
        self.host = "172.20.10.4"

        self.port = 11000

        self.addr = (self.host, self.port)
        self.id = self.connect()


    #Funkcia ktora kontorluje ci je klient pripojeny alebo nie
    def connect(self):
        try:
            self.client.connect(self.addr)
            print(f"Pripojený k: {self.addr}")
            return self.client.recv(2048).decode()
        except:
            from games import Game
            print(f"Pri pripajani nastala chyba skontrolujte udaje na pripojenie na server.")
            Game.close_game()
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