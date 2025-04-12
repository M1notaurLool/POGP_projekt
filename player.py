import pygame

class Player:
    def __init__(self, x, y, width=50, height=50, color=(255, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 5

    def move(self, dx, dy):
        """Posunie postavu o zadané hodnoty."""
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        """Vykreslí postavu na danom plátne."""
        pygame.draw.rect(screen, self.color, self.rect)
