import time

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
        self.hits = 50  # <= Tu sledujeme počet zásahov/životov
        self.last_shot_time = 0  # posledný čas streľby
        self.shield_active = False
        self.shield_timer = 0
        self.boost_timer = 0

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

         # ✨ Vizualizácia aktívneho štítu
        if self.shield_active:
            pygame.draw.circle(g, (0, 150, 255), (int(self.x), int(self.y)), self.image.get_width() // 2 + 10, 3)

        # Nakreslenie striel
        for bullet in self.bullets:
            bullet.draw(g)

    def move_forward(self):
        """Pohyb vpred podľa uhla raketky"""
        radian_angle = math.radians(self.angle)
        speed = self.velocity
        new_x = self.x + speed * math.cos(radian_angle)
        new_y = self.y - speed * math.sin(radian_angle)

        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        image_width = self.image.get_width() // 2
        image_height = self.image.get_height() // 2

        if image_width <= new_x <= screen_width - image_width:
            self.x = new_x
        if image_height <= new_y <= screen_height - image_height:
            self.y = new_y
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
        current_time = time.time()
        bullet_speed = 12
        radian_angle = math.radians(self.angle)
        bullet_x = self.x + (self.image.get_width()/10 // 2) * math.cos(radian_angle)
        bullet_y = self.y - (self.image.get_height()/10 // 2) * math.sin(radian_angle)

        self.bullets.append(Bullet(bullet_x, bullet_y, self.angle, bullet_speed))
        self.last_shot_time = current_time  # aktualizuj čas poslednej strely
    def update_bullets(self):
        """Aktualizuje polohu striel a odstráni tie, ktoré sú mimo obrazovky."""
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        for bullet in self.bullets[:]:
            bullet.move()
            if not (0 <= bullet.x <= pygame.display.get_surface().get_width() and 0 <= bullet.y <= pygame.display.get_surface().get_height()):  #veľkosť mapy
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
            self.hits = int(parts[-1])
        except:
            pass

    def get_rect(self):
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)
        return rotated_image.get_rect(center=(self.x, self.y))

    def check_hit(self, other_player):
        """
        Skontroluje zásahy do druhého hráča a upraví životy.
        """
        other_rect = other_player.get_rect()
        other_mask = other_player.mask

        if other_player.shield_active:
            return  # ignoruj hity ak je shield aktívny

        for bullet in self.bullets[:]:
            bullet_rect = pygame.Rect(bullet.x - 5, bullet.y - 5, 10, 10)  # hitbox
            offset = (bullet_rect.x - other_rect.x, bullet_rect.y - other_rect.y)

            if other_mask.overlap(pygame.mask.Mask((10, 10), fill=True), offset):
                self.bullets.remove(bullet)

                # Tu upravujeme zdravie/hity
                other_player.hits -= 1

                print(f"Zásah! Moje životy: {self.hits}, súperove životy: {other_player.hits}")
    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = pygame.time.get_ticks()
        print("Štít aktivovaný")

    def activate_speed_boost(self):
        self.velocity += 5
        self.boost_timer = pygame.time.get_ticks()
        print("Rýchlostný boost aktivovaný")
