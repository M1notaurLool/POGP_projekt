import pygame
import math
from bullet import Bullet

class Player():
    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 8
        self.SCALE = 6          #velkost raket (realna velkost/SCALE)
        self.angle = 0
        self.color = color
        self.bullets = []  # Zoznam vystrelených projektilov
        self.hits = 0  # <= Tu sledujeme počet zásahov

        self.image = pygame.image.load("obrazok/raketa_green.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)  # Otočenie o 90° doprava
        #nastavenie velkosti raketky podla rozmerov zmensena 10x
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width()/self.SCALE, self.image.get_height()/self.SCALE))
        self.mask = pygame.mask.from_surface(self.image) #vytvorenie masky pre hitbox

    def draw(self, g):
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)
        self.mask = pygame.mask.from_surface(rotated_image) #otacanie hitboxa podla rakety
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
        bullet_x = self.x + (self.image.get_width()/self.SCALE // 2) * math.cos(radian_angle)
        bullet_y = self.y - (self.image.get_height()/self.SCALE // 2) * math.sin(radian_angle)

        self.bullets.append(Bullet(bullet_x, bullet_y, self.angle, bullet_speed))

    def update_bullets(self):
        """Aktualizuje polohu striel a odstráni tie, ktoré sú mimo obrazovky."""
        for bullet in self.bullets[:]:
            bullet.move()
            if not (0 <= bullet.x <= 1000 and 0 <= bullet.y <= 1000):  # Predpokladaná veľkosť mapy
                self.bullets.remove(bullet)
    def serialize(self, id):
        # Získame pozíciu a uhol + strely ako zoznam x,y
        base = f"{id}:{int(self.x)},{int(self.y)},{int(self.angle)}"
        if self.bullets:
            bullets_str = "|".join([f"{int(b.x)},{int(b.y)}" for b in self.bullets])
            return f"{base}|{bullets_str}|{self.hits}"  # Počet hitov na konci
        return f"{base}||{self.hits}"

    def deserialize(self, data):
        # Očakáva formát: id:x,y,angle|x1,y1|x2,y2|...
        try:
            parts = data.split(":")[1].split("|")
            pos_parts = parts[0].split(",")
            self.x = int(pos_parts[0])
            self.y = int(pos_parts[1])
            self.angle = int(pos_parts[2])
            self.bullets = []
            for bullet_data in parts[1:-1]:
                if bullet_data:
                    bx, by = bullet_data.split(",")
                    from bullet import Bullet
                    self.bullets.append(Bullet(int(bx), int(by), self.angle, speed=0))
            self.hits = int(parts[-1])  # <- tu sa získa hit count
        except:
            pass

    def get_rect(self):
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)
        return rotated_image.get_rect(center=(self.x, self.y))

    def check_hit(self, other_player):
        """
        Skontroluje zásahy do druhého hráča a vymaže strely.
        """
        other_rect = other_player.get_rect()
        other_mask = other_player.mask

        for bullet in self.bullets[:]:
            bullet_rect = pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)               #hitbox
            offset = (bullet_rect.x - other_rect.x, bullet_rect.y - other_rect.y)

            if other_mask.overlap(pygame.mask.Mask((10, 10), fill=True), offset):
                self.bullets.remove(bullet)
                self.hits += 1
                print(f"Zásah! Hráč má {self.hits} hitov.")
