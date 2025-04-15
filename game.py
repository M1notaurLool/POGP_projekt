import pygame
from network import Network
from player import Player

class Game:

    def __init__(self, w, h):
        self.net = Network()
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

            # Synchronizácia s druhým hráčom cez server
            self.player2.x, self.player2.y, self.player2.angle = self.parse_data(self.send_data())

            # Kreslenie
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Odošle pozíciu a uhol hráča na server
        """
        data = f"{self.net.id}:{self.player.x},{self.player.y},{self.player.angle}"
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return float(d[0]), float(d[1]), float(d[2])
        except:
            return 0, 0, 0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0, 0, 0))
        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

    def update(self):
        pygame.display.update()

    def draw_background(self):
        self.screen.fill((255, 255, 255))
