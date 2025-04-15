import pygame
import math
from bullet import Bullet

class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)

    def __init__(self, startx, starty, color=(255,0,0), image_path="player.png"):
        self.x = float(startx)
        self.y = float(starty)
        self.velocity = 3  # Rýchlosť pohybu
        self.angle = 0  # Uhol otočenia (v stupňoch)
        self.bullets = []  # Zoznam vystrelených projektilov
        self.color = color

        # Načítanie obrázka a zmenšenie na veľkosť hráča
        self.image = pygame.image.load("obrazok/RaketaPassive.png")
        self.image = pygame.transform.rotate(self.image, -90)  # Otočenie o 90° doprava
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, g):
        # Vykreslí obrázok na pozíciu (x, y)
        rotated_image = pygame.transform.rotate(self.image, self.angle)
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
        self.angle -= 3  # Normalizované otáčanie doprava


    def move(self, direction):
        """Posunie raketu podľa smeru a času"""
        if direction == "forward":  # Pohyb vpred
            self.move_forward()
        elif direction == "left":  # Otáčanie doľava
            self.rotate_left()
        elif direction == "right":  # Otáčanie doprava
            self.rotate_right()

    def shoot(self):
        """Vytvorí novú strelu v smere raketky."""
        bullet_speed = 7  # Rýchlosť strely
        radian_angle = math.radians(self.angle)
        bullet_x = self.x + (self.width // 2) * math.cos(radian_angle)
        bullet_y = self.y - (self.height // 2) * math.sin(radian_angle)

        self.bullets.append(Bullet(bullet_x, bullet_y, self.angle, bullet_speed))

    def update_bullets(self):
        """Aktualizuje polohu striel a odstráni tie, ktoré sú mimo obrazovky."""
        for bullet in self.bullets[:]:
            bullet.move()
            if not (0 <= bullet.x <= 1000 and 0 <= bullet.y <= 1000):  # Predpokladaná veľkosť mapy
                self.bullets.remove(bullet)
