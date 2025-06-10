import sys

import pygame
from network import Network
from player import Player
import subprocess
import random
from heal_boost import HealBoost
from shield_boost import Shield
from turbo_boost import TurboBoost

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, "Space Blast")
        self.player = Player(50, 50)
        self.player2 = Player(100, 100)
        self.boosts = []  # budú sa prijímať zo servera

        # === BOOSTY ===
        self.boosts = [
            HealBoost("obrazok/heal.png", 600, 300),
            Shield("obrazok/shield.png", 800, 500),
            TurboBoost("obrazok/turbo.png", 1000, 400)
        ]

    def run(self):
        clock = pygame.time.Clock()
        run = True

        background_image = pygame.image.load('obrazok/pozadie_hra.jpg')
        background_image = pygame.transform.scale(background_image, (self.width, self.height))

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    subprocess.Popen([sys.executable, "lobby.py"]) #zapne lobby ked vypinam hru
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

            keys = pygame.key.get_pressed()

            # OVLÁDANIE RAKETY
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.move_forward()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.rotate_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.rotate_right()

            # Strely
            self.player.update_bullets()

              # BOOST TRVANIE
            current_time = pygame.time.get_ticks()
            if self.player.shield_active and current_time - self.player.shield_timer > 5000:
                self.player.shield_active = False
            if hasattr(self.player, "boost_timer") and current_time - self.player.boost_timer > 3000:
                self.player.velocity = 8


            # Synchronizácia s druhým hráčom cez server
            self.parse_data(self.send_data())

            # Po update_bullets() a pred kreslením
            self.player.check_hit(self.player2)
            self.player2.check_hit(self.player)

            if self.player.hits <= 0:
                print("Vyhráva Hráč 2!")
                pygame.quit()
                subprocess.Popen([sys.executable, "prehra.py"])

            if self.player2.hits <= 0:
                print("Vyhráva Hráč 1!")
                pygame.quit()
                subprocess.Popen([sys.executable, "vyhra.py"])

            # Kreslenie
            self.canvas.draw_background(background_image)

            # === BOOSTY ===
            for boost in self.boosts[:]:
                boost.update()
                if boost.check_collision(self.player):
                    self.boosts.remove(boost)
                else:
                    boost.draw(self.canvas.get_canvas())

            # Respawn boostov po čase
            if len(self.boosts) < 3:  # Napr. max 3 boosty
                if random.randint(0, 100) == 1:  # Malá šanca každý frame
                    boost_type = random.choice([HealBoost, Shield, TurboBoost])
                    image_path = {
                        HealBoost: "obrazok/heal.png",
                        Shield: "obrazok/shield.png",
                        TurboBoost: "obrazok/turbo.png"
                    }[boost_type]
                    new_boost = boost_type(image_path, random.randint(100, 1800), random.randint(100, 900))
                    self.boosts.append(new_boost)

            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.draw_player_info("Hráč 1", self.player.hits, max_hits=50, align="left", y_offset=10, color=(0, 200, 255), bar_color=(0, 200, 255))
            self.canvas.draw_player_info("Hráč 2", self.player2.hits, max_hits=50, align="right", y_offset=10,color=(255, 100, 100), bar_color=(255, 100, 100))
            self.canvas.update()

    def send_data(self):
        """
        Odošle pozíciu, uhol aj strely hráča na server
        """
        data = self.player.serialize(self.net.id)
        reply = self.net.send(data)
        return reply

    def parse_data(self,data):
        """
        Získaj info o druhom hráčovi a aktualizuj jeho pozíciu + strely
        """
        self.player2.deserialize(data)
        return self.player2.x, self.player2.y, self.player2.angle

class Canvas:
    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption(name)

    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, color)
        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

    def update(self):
        pygame.display.update()

    def draw_background(self, image):
        self.screen.blit(image,(0, 0))

    def draw_player_info(self, label, hits, max_hits, align="left", y_offset=10, color=(255, 255, 255), bar_color=(0, 200, 255)):
         pygame.font.init()
         font = pygame.font.SysFont("Poppins", 30, bold=True)
         text = f"{label}: {hits}"
         render = font.render(text, True, color)
         text_width, text_height = font.size(text)

         bar_width = 400
         bar_height = 20
         bar_padding = 5

         # Zarovnanie
         if align == "left":
             x_text = y_offset
             x_bar = y_offset
         elif align == "right":
             x_text = self.width - text_width - y_offset
             x_bar = self.width - bar_width - y_offset
         else:
             x_text = (self.width - text_width) // 2
             x_bar = (self.width - bar_width) // 2

         y_text = y_offset
         y_bar = y_text + text_height + bar_padding

         # Text
         self.screen.blit(render, (x_text, y_text))

         # Progress bar background (frame)


         # Výpočet dĺžky zaplnenej časti
         fill_width = int((hits / max_hits) * bar_width)

         # Výplň barov
         if align == "right":
             # Výplň sprava doľava
             fill_x = x_bar + (bar_width - fill_width)
         else:
             # Výplň zľava doprava
             fill_x = x_bar

         pygame.draw.rect(self.screen, bar_color, (fill_x, y_bar, fill_width, bar_height))
         pygame.draw.rect(self.screen, (255, 255, 255), (x_bar, y_bar, bar_width, bar_height), 2)
