import math
import pygame


class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color
        self.angle = 0  # Uhol otočenia hráča

    def draw(self, g):
        # Rotácia objektu hráča podľa jeho aktuálneho uhla
        rotated_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(rotated_image, self.color, (0, 0, self.width, self.height))
        rotated_image = pygame.transform.rotate(rotated_image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        g.blit(rotated_image, new_rect.topleft)

    def move(self, dirn):
        """
        :param dirn: 0 - forward, 1 - backward, 2 - rotate left, 3 - rotate right
        :return: None
        """
        radian_angle = math.radians(self.angle)

        if dirn == 0:  # Pohyb dopredu
            self.x += self.velocity * math.cos(radian_angle)
            self.y -= self.velocity * math.sin(radian_angle)
        elif dirn == 2:  # Otáčanie doľava
            self.angle += 5
        elif dirn == 3:  # Otáčanie doprava
            self.angle -= 5


