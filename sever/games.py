import threading
import time
import math
import pygame
from networks import Network
from player import Player, Bullet

class Game:
    def __init__(self, w, h, okno_instance):
        self.net = Network(okno_instance)
        self.width = w
        self.height = h
        self.player = Player(250, 250)  # Hlavný hráč
        self.player2 = Player(100, 100, image_path="RaketaPassive.png")  # Druhý hráč (súper)
        self.canvas = Canvas(self.width, self.height, "Triskáč Blast")
        self.last_received_data = "0,0"

    def run(self):
        run = True
        frame_counter = 0
        clock = pygame.time.Clock()

        while run:
            dt = clock.tick(60) / 1000.0  # Delta čas

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.player.move("right", dt)
            if keys[pygame.K_LEFT]:
                self.player.move("left", dt)
            if keys[pygame.K_UP]:
                self.player.move("forward", dt)
            if keys[pygame.K_SPACE]:  # Streľba
                self.player.shoot()

            # Aktualizujeme strely
            self.player.update_bullets()

            # Posielame údaje na server
            if frame_counter % 10 == 0:
                self.last_received_data = self.send_data()

            # Aktualizujeme pozíciu hráča 2 len z posledných platných dát
            print("Received data:", self.last_received_data)
            self.player2.x, self.player2.y = self.parse_data(self.last_received_data)
            print("Updated player2 position:", self.player2.x, self.player2.y)

            # Kreslenie
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

            frame_counter += 1  # Zvyšujeme počítadlo snímkov

        pygame.quit()

    def send_data(self):
        """Posiela pozíciu hráča na server."""
        data = f"{self.net.id}:{self.player.x},{self.player.y}"
        reply = self.net.send(data)
        return reply


    def parse_data(self, data):
        """Spracuje dáta od servera."""
        """Spracuje dáta od servera a vráti súradnice druhého hráča."""
        try:
            players = data.split(";")  # Ak je viac hráčov, oddelíme ich stredníkom
            for p in players:
                player_id, coords = p.split(":")  # Rozdelíme ID a súradnice
                if int(player_id) != self.net.id:  # Ak to NIE SOM JA, uložím to ako súpera
                    x, y = map(float, coords.split(","))
                    return x, y
            return self.player2.x, self.player2.y  # Ak nič nenašlo, vráť staré súradnice
        except:
            return self.player2.x, self.player2.y  # Ak je chyba, zachovaj predchádzajúcu hodnotu


class Canvas:
    """Grafická plocha pre hru."""

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0,0,0))
