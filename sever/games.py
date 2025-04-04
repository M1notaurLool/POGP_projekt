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

        threading.Thread(target=self.send_data_thread, daemon=True).start()

    def send_data_thread(self):
        """Beží na pozadí a neustále posiela dáta na server bez blokovania hry."""
        while True:
            data = f"{self.net.id}:{self.player.x},{self.player.y}"
            reply = self.net.send(data)
            if reply:
                self.last_received_data = reply
            time.sleep(0.05)

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

            # Posielanie údajov na server len každých 10 snímkov
            if frame_counter % 10 == 0:
                self.last_received_data = self.send_data()

            # Aktualizujeme hráča 2 len z posledných platných dát
            self.player2.x, self.player2.y = self.parse_data(self.last_received_data)

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

    @staticmethod
    def parse_data(data):
        """Spracuje dáta od servera."""
        try:
            d = data.split(":")[1].split(",")
            return float(d[0]), float(d[1])
        except:
            return 0, 0


class Canvas:
    """Grafická plocha pre hru."""

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h), pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.flip()  # Použijeme flip() pre lepší rendering

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0, 0, 0))  # Čierne pozadie
