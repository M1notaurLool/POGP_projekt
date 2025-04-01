import pygame
from raketa import Raketa

class GameWorld:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Space Battle")

        # Rakety hráčov
        self.raketa1 = Raketa(100, 200, "up", "left", "right", "space", (255, 0, 0))  # Hráč 1
        self.raketa2 = Raketa(300, 200, "w", "a", "d", "LCTRL", (0, 0, 255))  # Hráč 2

        # Skupina pre všetky objekty
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.raketa1, self.raketa2)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Čierne pozadie
        self.all_sprites.draw(self.screen)

        # Zobrazenie skóre
        font = pygame.font.Font(None, 36)
        score_text1 = font.render(f"Skóre Hráč 1: {self.raketa1.score}", True, (255, 255, 255))
        score_text2 = font.render(f"Skóre Hráč 2: {self.raketa2.score}", True, (255, 255, 255))
        self.screen.blit(score_text1, (20, 10))
        self.screen.blit(score_text2, (20, 40))
