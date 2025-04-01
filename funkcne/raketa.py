import pygame
import math
from strela import Strela

class Raketa(pygame.sprite.Sprite):
    def __init__(self, x, y, up_key, left_key, right_key, shoot_key, color):
        super().__init__()
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0  # Počiatočný uhol rakety
        self.speed = 3
        self.score = 0

        # Zmena klávesov na správne Pygame konštanty
        self.key_map = {
            "up": pygame.K_UP,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "space": pygame.K_SPACE,
            "w": pygame.K_w,
            "a": pygame.K_a,
            "d": pygame.K_d,
            "LCTRL": pygame.K_LCTRL
        }

        # Nastavenie ovládacích kláves
        self.up_key = self.key_map.get(up_key, pygame.K_UP)
        self.left_key = self.key_map.get(left_key, pygame.K_LEFT)
        self.right_key = self.key_map.get(right_key, pygame.K_RIGHT)
        self.shoot_key = self.key_map.get(shoot_key, pygame.K_SPACE)

    def update(self):
        keys = pygame.key.get_pressed()

        # Otáčanie rakety pomocou šípok
        if keys[self.left_key]:
            self.angle += 5  # Otočiť doľava
        if keys[self.right_key]:
            self.angle -= 5  # Otočiť doprava

        # Pohyb rakety dopredu
        if keys[self.up_key]:
            self.move_forward()

        # Kontrola kolízií medzi strelami a raketou
        self.check_collisions()

        # Aktualizácia pozície a obrázku rakety
        self.update_image()

    def move_forward(self):
        # Výpočet pohybu vpred podľa aktuálneho uhla rakety
        radian_angle = math.radians(self.angle)

        # Ak raketa ukazuje doľava (180°) alebo doprava (0°), upravíme pohyb v smere y a x
        self.rect.x += self.speed * math.cos(radian_angle)  # Používame cos pre x
        self.rect.y -= self.speed * math.sin(radian_angle)  # Používame sin pre y (Y-axis je obrátene v Pygame)

    def update_image(self):
        # Rotácia obrázku rakety podľa aktuálneho uhla
        old_center = self.rect.center
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        self.image.fill((0, 255, 0))  # Predstav si, že sem nahráš svoj obrázok rakety
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=old_center)

    def shoot(self):
        # Strela vyletí zo stredu rakety a je otočená podľa uhla rakety
        radian_angle = math.radians(self.angle)
        x_offset = math.cos(radian_angle) * 25  # Offset na začiatok strely
        y_offset = -math.sin(radian_angle) * 25  # Offset na začiatok strely

        strela = Strela(self.rect.centerx + x_offset, self.rect.centery + y_offset, self)
        self.groups()[0].add(strela)  # Pridanie strely do skupiny objektov

    def check_collisions(self):
        # Kontrola, či sa raketa stretla so strelami (detekcia kolízií)
        for strela in self.groups()[0]:  # Predpokladáme, že všetky strieľajúce objekty sú v tejto skupine
            if isinstance(strela, Strela) and self.rect.colliderect(strela.rect):
                # Ak sa raketa zrazí so strelou
                strela.kill()  # Odstránime strelu z obrazovky
                self.pricitaj_skore(1)  # Zvyšujeme skóre (závisí na tvojej logike, možno aj od iného hráča)
                print(f"Score: {self.score}")  # Tlač skóre do konzoly

    def pricitaj_skore(self, oKolko):
        self.score += oKolko

    def odcitaj_skore(self, oKolko):
        self.score -= oKolko
