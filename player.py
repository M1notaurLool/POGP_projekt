import pygame
import math


class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0), image_path="player.png"):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.angle = 0
        self.color = color

        # Načítanie obrázka a zmenšenie na veľkosť hráča
        self.image = pygame.image.load("obrazok/RaketaPassive.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, g):
        # Vykreslí obrázok na pozíciu (x, y)
        g.blit(self.image, (self.x, self.y))

    def move_forward(self, dt):
        """Pohyb vpred podľa uhla raketky"""
        radian_angle = math.radians(self.angle)
        speed = self.velocity * dt * 60  # Normalizovaná rýchlosť
        self.x += speed * math.cos(radian_angle)
        self.y -= speed * math.sin(radian_angle)

    def rotate_left(self, dt):
        """Otáčanie raketky doľava"""
        self.angle += 3 * dt * 60  # Normalizované otáčanie doľava

    def rotate_right(self, dt):
        """Otáčanie raketky doprava"""
        self.angle -= 3 * dt * 60  # Normalizované otáčanie doprava


    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """
        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity

