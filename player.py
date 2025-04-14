import pygame
import math


class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0), image_path="player.png"):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color

        # Načítanie obrázka a zmenšenie na veľkosť hráča
        self.image = pygame.image.load("obrazok/RaketaPassive.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, g):
        # Vykreslí obrázok na pozíciu (x, y)
        g.blit(self.image, (self.x, self.y))

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
        else:
            self.y += self.velocity
