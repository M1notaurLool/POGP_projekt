import pygame

class Strela(pygame.sprite.Sprite):
    def __init__(self, x, y, raketa):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 255))  # Biela farba strely
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -5  # Rýchlosť strely
        self.raketa = raketa

    def update(self):
        self.rect.y += self.speed

        # Ak strela vyletí z obrazovky (nad obrazovku), odstráni sa
        if self.rect.bottom < 0:
            self.kill()
