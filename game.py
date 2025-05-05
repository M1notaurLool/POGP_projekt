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
        background_image = pygame.transform.scale(background_image, (1920, 1080))

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

            # Po update_bullets() a pred kreslením
            self.player.check_hit(self.player2)
            self.player2.check_hit(self.player)

            if self.player.hits <= 0:
                print("Vyhráva Hráč 2!")
                pygame.quit()
                subprocess.Popen([sys.executable, "vyherca_2.py"])

            if self.player2.hits <= 0:
                print("Vyhráva Hráč 1!")
                pygame.quit()
                subprocess.Popen([sys.executable, "vyherca_1.py"])

            # Synchronizácia s druhým hráčom cez server
            self.parse_data(self.send_data())

            # Kreslenie
            self.canvas.draw_background(background_image)

            # === BOOSTY ===
            for boost in self.boosts[:]:
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
            self.canvas.draw_text(f"Hráč 1 hity: {self.player.hits}", 30, 10, 10)
            self.canvas.draw_text(f"Hráč 2 hity: {self.player2.hits}", 30, 10, 40)
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

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (255, 255, 255))
        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

    def update(self):
        pygame.display.update()

    def draw_background(self, image):
        self.screen.blit(image,(0, 0))
