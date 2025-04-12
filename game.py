import pygame
import sys
from network import Network

class Game:
    def __init__(self, width, height, network):
        self.width = width
        self.height = height
        self.net = network
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Nastavenie ID hráča a súperovskej pozície podľa získaného ID
        if self.net.id == "0":
            self.my_id = "0"
            self.enemy_id = "1"
            # Moja postava a súper (predvolené pozície – môžu byť upravené)
            self.players = {
                "0": pygame.Rect(50, 50, 50, 50),
                "1": pygame.Rect(100, 100, 50, 50)
            }
        else:
            self.my_id = "1"
            self.enemy_id = "0"
            self.players = {
                "1": pygame.Rect(50, 50, 50, 50),
                "0": pygame.Rect(100, 100, 50, 50)
            }

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Vymaž obrazovku

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Spracovanie vstupu a pohyb mojej postavy.
            self.handle_player_movement()

            # Odoslanie mojej pozície a prijatie pozície súperovej postavy.
            reply = self.send_data()
            if reply:
                x, y = self.parse_data(reply)
                # Aktualizácia pozície súperovej postavy.
                self.players[self.enemy_id].x = x
                self.players[self.enemy_id].y = y

            # Vykreslenie oboch hráčov.
            for player_rect in self.players.values():
                pygame.draw.rect(self.screen, (255, 0, 0), player_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_player_movement(self):
        """Spracuje vstup z klávesnice a pohne mojou postavou."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.players[self.my_id].x -= 5
        if keys[pygame.K_RIGHT]:
            self.players[self.my_id].x += 5
        if keys[pygame.K_UP]:
            self.players[self.my_id].y -= 5
        if keys[pygame.K_DOWN]:
            self.players[self.my_id].y += 5

    def send_data(self):
        """Odošle moju aktuálnu pozíciu na server a vráti pozíciu súperovej postavy."""
        rect = self.players[self.my_id]
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
