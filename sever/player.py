import pygame
import math
from Bullet import Bullet

class Player:
    WIDTH = HEIGHT = 50  # Veľkosť raketky

    def __init__(self, x, y, color=(255, 0, 0)):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 3  # Rýchlosť pohybu
        self.angle = 0  # Uhol otočenia (v stupňoch)
        self.color = color
        self.bullets = []  # Zoznam vystrelených projektilov

    def move(self, direction, dt):
        """Posunie raketu podľa smeru a času"""
        if direction == "forward":  # Pohyb vpred
            self.move_forward(dt)
        elif direction == "left":  # Otáčanie doľava
            self.rotate_left(dt)
        elif direction == "right":  # Otáčanie doprava
            self.rotate_right(dt)

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

    def shoot(self):
        """Vytvorí novú strelu v smere raketky."""
        bullet_speed = 7  # Rýchlosť strely
        radian_angle = math.radians(self.angle)
        bullet_x = self.x + (self.WIDTH // 2) * math.cos(radian_angle)
        bullet_y = self.y - (self.HEIGHT // 2) * math.sin(radian_angle)

        self.bullets.append(Bullet(bullet_x, bullet_y, self.angle, bullet_speed))

    def update_bullets(self):
        """Aktualizuje polohu striel a odstráni tie, ktoré sú mimo obrazovky."""
        for bullet in self.bullets[:]:
            bullet.move()
            if not (0 <= bullet.x <= 1000 and 0 <= bullet.y <= 1000):  # Predpokladaná veľkosť mapy
                self.bullets.remove(bullet)

    def draw(self, screen):
        """Nakreslí raketku a strely na obrazovku."""
        radian_angle = math.radians(self.angle)
        # Určíme vrcholy trojuholníka s ohľadom na uhol
        points = [
            (self.x + math.cos(radian_angle) * self.HEIGHT, self.y - math.sin(radian_angle) * self.HEIGHT),  # Hrot
            (self.x + math.cos(radian_angle + math.pi / 2) * self.WIDTH, self.y - math.sin(radian_angle + math.pi / 2) * self.WIDTH),  # Ľavý okraj
            (self.x + math.cos(radian_angle - math.pi / 2) * self.WIDTH, self.y - math.sin(radian_angle - math.pi / 2) * self.WIDTH)  # Pravý okraj
        ]

        # Vytvoríme povrch pre raketu
        pygame.draw.polygon(screen, self.color, points)  # Trojuholník rakety (hrot je tam, kde sa otáča)

        # Nakreslenie striel
        for bullet in self.bullets:
            bullet.draw(screen)

    def get_hitbox(self):
        """Vráti hitbox ako pygame Rect (na kolízie)."""
        return pygame.Rect(self.x - 25, self.y - 25, self.WIDTH, self.HEIGHT)
