import sys

import pygame
from network import Network
from player import Player
import subprocess

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, "Space Blast")
        self.player = Player(50, 50)
        self.player2 = Player(100, 100)


    def run(self):
        clock = pygame.time.Clock()
        run = True

        background_image = pygame.image.load('obrazok/pozadie_hra.jpg')
        background_image = pygame.transform.scale(background_image, (1920, 1080))

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    subprocess.Popen([sys.executable, "lobby.py"]) #zapne lobby ked vypinam hru

            keys = pygame.key.get_pressed()

            # OVLÁDANIE RAKETY
            if keys[pygame.K_UP]:
                self.player.move_forward()
            if keys[pygame.K_LEFT]:
                self.player.rotate_left()
            if keys[pygame.K_RIGHT]:
                self.player.rotate_right()
            if keys[pygame.K_SPACE]:
                self.player.shoot()

            # Strely
            self.player.update_bullets()

            # Po update_bullets() a pred kreslením
            self.player.check_hit(self.player2)
            self.player2.check_hit(self.player)

            # Synchronizácia s druhým hráčom cez server
            self.player2.x, self.player2.y, self.player2.angle = self.parse_data(self.send_data())

            # Kreslenie
            self.canvas.draw_background(background_image)
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.draw_text(f"Hráč 1 hity: {self.player.hits}", 30, 10, 10)
            self.canvas.draw_text(f"Hráč 2 hity: {self.player2.hits}", 30, 10, 40)
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Odošle pozíciu, uhol aj strely hráča na server
        """
        data = self.player.serialize(self.net.id)
        reply = self.net.send(data)
        return reply

    def parse_data(self,data):
        """
        Získaj info o druhom hráčovi a aktualizuj jeho pozíciu + strely
        """
        self.player2.deserialize(data)
        return self.player2.x, self.player2.y, self.player2.angle


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption(name)

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (255, 255, 255))
        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

    def update(self):
        pygame.display.update()

    def draw_background(self, image):
        self.screen.blit(image,(0, 0))
