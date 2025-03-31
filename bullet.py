import pygame
from config import BULLET_SPEED

class Bullet:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def update(self):
        self.y -= BULLET_SPEED  # Pohyb smerom nahor

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 5, 10))