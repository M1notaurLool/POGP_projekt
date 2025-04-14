import pygame
import math

class Bullet:
    SIZE = 8  # Veľkosť strely

    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed

    def move(self):
        """Posunie strelu v smere uhla."""
        radian_angle = math.radians(self.angle)
        self.x += self.speed * math.cos(radian_angle)
        self.y -= self.speed * math.sin(radian_angle)

    def draw(self, screen):
        """Nakreslí strelu na obrazovku."""
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.SIZE)
