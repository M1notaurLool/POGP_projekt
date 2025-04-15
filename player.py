import pygame
import math
from bullet import Bullet

class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.angle = 0
        self.color = color

        self.image = pygame.image.load("obrazok/RaketaPassive.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, g):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        g.blit(rotated_image, rect.topleft)

    def move_forward(self):
        """Pohyb vpred podľa uhla raketky"""
        radian_angle = math.radians(self.angle)
        speed = self.velocity  # Normalizovaná rýchlosť
        self.x += speed * math.cos(radian_angle)
        self.y -= speed * math.sin(radian_angle)

    def rotate_left(self):
        """Otáčanie raketky doľava"""
        self.angle += 3  # Normalizované otáčanie doľava

    def rotate_right(self):
        """Otáčanie raketky doprava"""
        self.angle -= 3

    def move(self, dirn):
        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity