import pygame
import random
from config import ENEMY_SPEED

class Enemy:
    def __init__(self):
        self.x, self.y = random.randint(0, 800), random.randint(0, 600)

    def update(self):
        self.y += ENEMY_SPEED  # Pohyb smerom dole

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, 50, 30))