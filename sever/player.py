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
        radian_angle = math.radians(self.angle)
        speed = self.velocity * dt * 60  # Normalizovaná rýchlosť

        if direction == "forward":  # Pohyb v smere raketky
            self.x += speed * math.cos(radian_angle)
            self.y -= speed * math.sin(radian_angle)
        elif direction == "left":  # Otáčanie doľava
            self.angle += 3 * dt * 60
        elif direction == "right":  # Otáčanie doprava
            self.angle -= 3 * dt * 60

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
        rotated_image = pygame.transform.rotate(rotated_image, -self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, new_rect.topleft)

        # Nakreslenie striel
        for bullet in self.bullets:
            bullet.draw(screen)

    def get_hitbox(self):
        """Vráti hitbox ako pygame Rect (na kolízie)."""
        return pygame.Rect(self.x - 25, self.y - 25, self.WIDTH, self.HEIGHT)
