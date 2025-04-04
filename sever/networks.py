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
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)