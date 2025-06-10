import time

import pygame
import math
from bullet import Bullet

pygame.mixer.init()
hit_channel = pygame.mixer.Channel(1)
hit_sound = pygame.mixer.Sound("soundFx/hit.mp3")
hit_sound.set_volume(0.3)

class Player():
    def __init__(self, startx, starty, color=(255,0,0), image_path="obrazok/raketa_blue.png"):
        self.x = startx
        self.y = starty
        self.velocity = 8
        self.SCALE = 6
        self.angle = 0
        self.color = color
        self.bullets = []
        self.hits = 50
        self.last_shot_time = 0
        self.shield_active = False
        self.shield_timer = 0
        self.boost_timer = 0
        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 0.3
        self.max_speed = 6
        self.friction = 0.05
        self.thrusting = False

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.smoothscale(
            self.image,
            (self.image.get_width() // self.SCALE, self.image.get_height() // self.SCALE)
        )
        self.mask = pygame.mask.from_surface(self.image)

        self.flame_image = pygame.image.load("obrazok/flames.png").convert_alpha()
        self.flame_image = pygame.transform.smoothscale(self.flame_image, (20, 40))

    def draw(self, g):
        if abs(self.vel_x) > 0.1 or abs(self.vel_y) > 0.1:
            rotated_flame = pygame.transform.rotozoom(self.flame_image, self.angle-90, 1.0)

            # Získaj zadnú časť rakety (stred + opačný smer)
            rad_angle = math.radians(self.angle)
            offset_x = -math.cos(rad_angle) * (self.image.get_height() // 2 + 10)
            offset_y = math.sin(rad_angle) * (self.image.get_height() // 2 + 10)

            flame_pos = (self.x + offset_x - rotated_flame.get_width() // 2,
                         self.y + offset_y - rotated_flame.get_height() // 2)

            g.blit(rotated_flame, flame_pos)
        # Otočenie rakety
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)
        self.mask = pygame.mask.from_surface(rotated_image)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        g.blit(rotated_image, rect.topleft)

        # ✅ Vizualizácia štítu
        if self.shield_active:
            pygame.draw.circle(g, (0, 100, 255), (int(self.x), int(self.y)), self.image.get_width() // 2 + 10, 3)

        # Nakreslenie striel
        for bullet in self.bullets:
            bullet.draw(g)

    def move_forward(self):
        radian_angle = math.radians(self.angle)
        self.vel_x += self.acceleration * math.cos(radian_angle)
        self.vel_y -= self.acceleration * math.sin(radian_angle)

        # Orezanie na maximálnu rýchlosť
        speed = math.hypot(self.vel_x, self.vel_y)
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vel_x *= scale
            self.vel_y *= scale
    def plamen(self):
        self.thrusting = True

    def apply_friction_and_move(self):
        # Aplikuj trenie
        if self.vel_x > 0:
            self.vel_x -= self.friction
            if self.vel_x < 0:
                self.vel_x = 0
        elif self.vel_x < 0:
            self.vel_x += self.friction
            if self.vel_x > 0:
                self.vel_x = 0

        if self.vel_y > 0:
            self.vel_y -= self.friction
            if self.vel_y < 0:
                self.vel_y = 0
        elif self.vel_y < 0:
            self.vel_y += self.friction
            if self.vel_y > 0:
                self.vel_y = 0

        # Posun hráča
        self.x += self.vel_x
        self.y += self.vel_y

        # Udržiavaj hráča v rámci obrazovky
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()
        image_width = self.image.get_width() // 2
        image_height = self.image.get_height() // 2

        self.x = max(image_width, min(self.x, screen_width - image_width))
        self.y = max(image_height, min(self.y, screen_height - image_height))

    def rotate_left(self):
        """Otáčanie raketky doľava"""
        self.angle += 4  # Normalizované otáčanie doľava

    def rotate_right(self):
        """Otáčanie raketky doprava"""
        self.angle -= 4

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
        bullet_speed = self.max_speed + 6
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
        # Formát: id:x,y,angle|x1,y1|x2,y2|...|hits|shield
        base = f"{id}:{int(self.x)},{int(self.y)},{int(self.angle)}"
        bullets_str = "|".join([f"{int(b.x)},{int(b.y)}" for b in self.bullets])
        shield_flag = "1" if self.shield_active else "0"
        if bullets_str:
            return f"{base}|{bullets_str}|{self.hits}|{shield_flag}"
        return f"{base}||{self.hits}|{shield_flag}"

    def deserialize(self, data):
        try:
            parts = data.split(":")[1].split("|")
            pos_parts = parts[0].split(",")
            self.x = int(pos_parts[0])
            self.y = int(pos_parts[1])
            self.angle = int(pos_parts[2])

            self.bullets = []
            # Strely sú medzi pozíciou a hits
            for bullet_data in parts[1:-2]:
                if bullet_data:
                    bx, by = bullet_data.split(",")
                    from bullet import Bullet
                    self.bullets.append(Bullet(int(bx), int(by), self.angle, speed=0))

            self.hits = int(parts[-2])
            self.shield_active = parts[-1] == "1"
        except Exception as e:
            print("Deserialization error:", e)

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
                hit_channel.play(hit_sound)

                print(f"Zásah! Moje životy: {self.hits}, súperove životy: {other_player.hits}")
    def activate_shield(self):
        self.shield_active = True
        self.shield_timer = pygame.time.get_ticks()
        print("Štít aktivovaný")

    def activate_speed_boost(self):
        self.max_speed += 5
        self.boost_timer = pygame.time.get_ticks()
        print("Rýchlostný boost aktivovaný")

    def update(self):
        self.thrusting = False
        # Vypnutie štítu a boostu
        if self.shield_active and pygame.time.get_ticks() - self.shield_timer > 3000:
            self.shield_active = False

        if self.max_speed > 6 and pygame.time.get_ticks() - self.boost_timer > 5000:
            self.max_speed = 6

        # 💠 Fyzika pohybu
        self.apply_friction_and_move()
          # Resetujeme po každom update frame


