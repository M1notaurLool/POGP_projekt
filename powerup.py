import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class PowerUp:
    def __init__(self):
        self.x, self.y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
        self.type = random.choice(["boost", "shield"])
    
    def update(self):
        pass  # PowerUp je statický

    def draw(self, screen):
        color = (255, 255, 0) if self.type == "boost" else (0, 255, 255)
        pygame.draw.circle(screen, color, (self.x, self.y), 10)

    def collides_with(self, player):
        return pygame.Rect(self.x - 10, self.y - 10, 20, 20).colliderect(pygame.Rect(player.x, player.y, 50, 30))