import pygame
<<<<<<< HEAD
from network import Network
=======
import math
>>>>>>> bd2f44ca5500cef19fd26d9d92e395464780e367


class Player():
    width = height = 50

<<<<<<< HEAD
    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

=======
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
>>>>>>> bd2f44ca5500cef19fd26d9d92e395464780e367
        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
<<<<<<< HEAD
        else:
            self.y += self.velocity
=======

>>>>>>> bd2f44ca5500cef19fd26d9d92e395464780e367
