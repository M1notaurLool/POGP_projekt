import pygame
from network import Network
from player import Player


class Game:

    def __init__(self, w, h, okno_instance):
        self.net = Network(okno_instance)
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.player2 = Player(100, 100)
        self.canvas = Canvas(self.width, self.height, "Triskáč Blast")

    def run(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] and self.player.x <= self.width - self.player.velocity:
                self.player.move(0)
            if keys[pygame.K_LEFT] and self.player.x >= self.player.velocity:
                self.player.move(1)
            if keys[pygame.K_UP] and self.player.y >= self.player.velocity:
                self.player.move(2)
            if keys[pygame.K_DOWN] and self.player.y <= self.height - self.player.velocity:
                self.player.move(3)

            # Odosielame pozíciu hráča, prijímame druhého
            data = self.send_data()
            self.player2.x, self.player2.y = self.parse_data(data)

            # Vykreslenie
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        data = f"{self.net.id}:{self.player.x},{self.player.y}"
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            if data == "no_data":
                return 0, 0
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255, 255, 255))
