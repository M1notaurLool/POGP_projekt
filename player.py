import pygame
import math
from bullet import Bullet

class Player():
    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 8
        self.angle = 0
        self.color = color
        self.bullets = []  # Zoznam vystrelených projektilov

        self.image = pygame.image.load("obrazok/raketa_green.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)  # Otočenie o 90° doprava
        #nastavenie velkosti raketky podla rozmerov zmensena 10x
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()/10, self.image.get_height()/10))

    def draw(self, g):
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        g.blit(rotated_image, rect.topleft)

        # Nakreslenie striel
        for bullet in self.bullets:
            bullet.draw(g)

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

    def shoot(self):
        """Vytvorí novú strelu v smere raketky."""
        bullet_speed = 7  # Rýchlosť strely
        radian_angle = math.radians(self.angle)
        bullet_x = self.x + (self.image.get_width()/10 // 2) * math.cos(radian_angle)
        bullet_y = self.y - (self.image.get_height()/10 // 2) * math.sin(radian_angle)

        self.bullets.append(Bullet(bullet_x, bullet_y, self.angle, bullet_speed))

    def update_bullets(self):
        """Aktualizuje polohu striel a odstráni tie, ktoré sú mimo obrazovky."""
        for bullet in self.bullets[:]:
            bullet.move()
            if not (0 <= bullet.x <= 1000 and 0 <= bullet.y <= 1000):  # Predpokladaná veľkosť mapy
                self.bullets.remove(bullet)