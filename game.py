import pygame
from network import Network
from player import Player

class Game:
    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.window = window
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Pozície hráčov (číslo ID určuje hráča)
        self.players = {
            "0": pygame.Rect(50, 50, 50, 50),
            "1": pygame.Rect(100, 100, 50, 50)
        }

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Vymaž obrazovku

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Pohyb postavičky
            self.handle_player_movement()

            # Zobraziť hráčov (na základe pozícií)
            for player_id, player_rect in self.players.items():
                pygame.draw.rect(self.screen, (255, 0, 0), player_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_player_movement(self):
        """Získaj vstup od užívateľa a pohybuj postavičkami."""
        keys = pygame.key.get_pressed()

        # Ak je stlačená šípka doľava, pohni postavičkou "0" doľava
        if keys[pygame.K_LEFT]:
            self.players["0"].x -= 5
        # Ak je stlačená šípka doprava, pohni postavičkou "0" doprava
        if keys[pygame.K_RIGHT]:
            self.players["0"].x += 5
        # Ak je stlačená šípka hore, pohni postavičkou "0" hore
        if keys[pygame.K_UP]:
            self.players["0"].y -= 5
        # Ak je stlačená šípka dole, pohni postavičkou "0" dole
        if keys[pygame.K_DOWN]:
            self.players["0"].y += 5

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
