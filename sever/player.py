import pygame
import math

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
        rotated_image = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(rotated_image, self.color, [(25, 0), (50, 50), (0, 50)])  # Trojuholníková raketa
        rotated_image = pygame.transform.rotate(rotated_image, self.angle)  # Otáčanie raketky
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, new_rect.topleft)

        # Nakreslenie striel
        for bullet in self.bullets:
            bullet.draw(screen)

    def get_hitbox(self):
        """Vráti hitbox ako pygame Rect (na kolízie)."""
        return pygame.Rect(self.x - 25, self.y - 25, self.WIDTH, self.HEIGHT)


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

    def get_hitbox(self):
        """Vráti hitbox strely."""
        return pygame.Rect(self.x - self.SIZE // 2, self.y - self.SIZE // 2, self.SIZE, self.SIZE)
