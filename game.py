import pygame
import sys
from network import Network
from player import Player

class Game:
    def __init__(self, width, height, network):
        # Inicializácia Pygame
        pygame.init()

        self.width = width
        self.height = height
        self.net = network
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Nastavenie ID hráča a súperovej postavy podľa získaného ID
        if self.net.id == "0":
            self.my_id = "0"
            self.enemy_id = "1"
            self.players = {
                "0": Player(50, 50),    # Moja postava
                "1": Player(100, 100)   # Súperova postava
            }
        else:
            self.my_id = "1"
            self.enemy_id = "0"
            self.players = {
                "1": Player(50, 50),    # Moja postava
                "0": Player(100, 100)   # Súperova postava
            }

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Vymažeme obrazovku

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Spracovanie vstupu – pohyb mojej postavy
            self.handle_player_movement()

            # Odoslanie mojej pozície a prijatie pozície súperovej postavy zo servera
            reply = self.send_data()
            if reply:
                x, y = self.parse_data(reply)
                # Aktualizácia pozície súperovej postavy
                self.players[self.enemy_id].rect.x = x
                self.players[self.enemy_id].rect.y = y

            # Vykreslenie oboch hráčov
            for player in self.players.values():
                player.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_player_movement(self):
        """Spracuje vstup z klávesnice a pohne mojou postavou."""
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.players[self.my_id].speed
        if keys[pygame.K_RIGHT]:
            dx = self.players[self.my_id].speed
        if keys[pygame.K_UP]:
            dy = -self.players[self.my_id].speed
        if keys[pygame.K_DOWN]:
            dy = self.players[self.my_id].speed
        self.players[self.my_id].move(dx, dy)

    def send_data(self):
        """Odošle aktuálnu pozíciu mojej postavy a vráti pozíciu súperovej postavy."""
        rect = self.players[self.my_id].rect
        data = f"{self.net.id}:{rect.x},{rect.y}"
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        """
        Rozparsuje prijaté dáta zo servera.
        Predpokladaný formát: "ID:x,y"
        """
        try:
            if data == "no_data":
                return 0, 0
            parts = data.split(":")
            coords = parts[1].split(",")
            return int(coords[0]), int(coords[1])
        except Exception as e:
            print("Parsing error:", e)
            return 0, 0
