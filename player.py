import pygame
from bullet import Bullet
from config import PLAYER_SPEED, BOOST_DURATION

class Player:
    def __init__(self, x, y, up_key, left_key, right_key, shoot_key):
        self.x, self.y = x, y
        self.up_key, self.left_key, self.right_key, self.shoot_key = up_key, left_key, right_key, shoot_key
        self.speed = PLAYER_SPEED
        self.bullets = []
        self.boost_time = 0
        self.shield = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[getattr(pygame, f"K_UP")]:
            self.y -= self.speed
        if keys[getattr(pygame, "K_LEFT")]:
            self.x -= self.speed
        if keys[getattr(pygame, f"K_RIGHT")]:
            self.x += self.speed
        if keys[getattr(pygame, f"K_SPACE")]:
            self.bullets.append(Bullet(self.x, self.y))

        for bullet in self.bullets:
            bullet.update()

        if self.boost_time > 0:
            self.boost_time -= 1
            if self.boost_time == 0:
                self.speed /= 2  # Deaktivácia boostu

    def activate_boost(self):
        self.speed *= 2
        self.boost_time = BOOST_DURATION

    def activate_shield(self):
        self.shield = 20

    def draw(self, screen):
        color = (0, 255, 0) if self.shield > 0 else (0, 0, 255)
        pygame.draw.rect(screen, color, (self.x, self.y, 50, 30))

        for bullet in self.bullets:
            bullet.draw(screen)