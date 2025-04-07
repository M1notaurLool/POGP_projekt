import pygame
import math


class Player:
    WIDTH = HEIGHT = 50  # Veľkosť raketky

    def __init__(self, x, y, image_path="RaketaPassive.png"):
        self.x = float(x)
        self.y = float(y)
        self.velocity = 100  # Zvýšená rýchlosť pohybu
        self.angle = 0  # Uhol otočenia (v stupňoch)
        self.bullets = []  # Zoznam vystrelených projektilov

        # Načítanie obrázka
        self.original_image = pygame.image.load(image_path)  # Načítanie obrázka
        self.original_image = pygame.transform.rotate(self.original_image, -90)  # Otočenie o 90° doprava
        self.original_image = pygame.transform.scale(self.original_image, (self.WIDTH, self.HEIGHT))  # Zmenšenie obrázka
        self.image = self.original_image  # Aktuálny obrázok, ktorý sa bude otáčať pri pohybe

    def move(self, direction, dt):
        # Predpokladáme, že velocity je určená v pixeloch za sekundu
        if direction == 0:  # Right
            self.x += self.velocity * dt
        elif direction == 1:  # Left
            self.x -= self.velocity * dt
        elif direction == 2:  # Up
            self.y -= self.velocity * dt
        elif direction == 3:  # Down
            self.y += self.velocity * dt

    def move_forward(self, dt):
        """Pohyb vpred podľa uhla raketky"""
        radian_angle = math.radians(self.angle)
        speed = self.velocity * dt  # Už nie je potrebné násobiť 60
        self.x += speed * math.cos(radian_angle)
        self.y -= speed * math.sin(radian_angle)

    def rotate_left(self, dt):
        """Otáčanie raketky doľava"""
        self.angle += 3 * dt * 60  # Normalizované otáčanie doľava

    def rotate_right(self, dt):
        """Otáčanie raketky doprava"""
        self.angle -= 3 * dt * 60  # Normalizované otáčanie doprava

    def draw(self, screen):
        """Nakreslí raketku ako obrázok na obrazovku."""
        # Otočenie obrázka podľa uhla rakety
        rotated_image = pygame.transform.rotate(self.image, self.angle)

        # Nájdeme stred obrázka po otočení
        rect = rotated_image.get_rect(center=(self.x, self.y))

        # Vykreslenie obrázka
        screen.blit(rotated_image, rect.topleft)
