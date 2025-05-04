import pygame
import random

class Boost:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        pygame.draw.circle(screen, (0, 255, 0), self.rect.center, 5)  # Debug kruh

    def check_collision(self, player):
        offset = (int(self.rect.x - player.get_rect().x), int(self.rect.y - player.get_rect().y))
        if player.mask.overlap(self.mask, offset):
            self.apply_to_player(player)
            return True
        return False

    def apply_to_player(self, player):
        raise NotImplementedError("Subclasses must implement this method")

class HealBoost(Boost):
    def apply_to_player(self, player):
        player.hits += 20
        if player.hits > 100:  # Max zdravie (ak chceš limit)
            player.hits = 100

class Shield(Boost):
    def apply_to_player(self, player):
        player.activate_shield()

class TurboBoost(Boost):
    def apply_to_player(self, player):
        player.activate_speed_boost()
