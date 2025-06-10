import pygame
import random

class Boost:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        # Pridanie pohybu
        self.dx = random.choice([-1, 1]) * 0.5  # Pomalý pohyb
        self.dy = random.choice([-1, 1]) * 0.5
        self.change_direction_timer = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        # Pohyb boostu
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Okraj obrazovky
        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.dy *= -1

        # Zmena smeru každé 3 sekundy
        if pygame.time.get_ticks() - self.change_direction_timer > 3000:
            self.dx = random.choice([-1, 1]) * 0.5
            self.dy = random.choice([-1, 1]) * 0.5
            self.change_direction_timer = pygame.time.get_ticks()

    def check_collision(self, player):
        offset = (int(self.rect.x - player.x), int(self.rect.y - player.y))
        if player.mask.overlap(self.mask, offset):
            self.apply_to_player(player)
            return True
        return False

    def apply_to_player(self, player):
        pass  # Implementujú podtriedy
