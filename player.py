import pygame




class Player():
    width = height = 50

    def __init__(self, startx, starty, color=(255,0,0), image_path="RaketaPassive.png"):
        self.x = startx
        self.y = starty
        self.angle = 0
        self.velocity = 2
        self.color = color

        self.original_image = pygame.image.load(image_path)  # Načítanie obrázka
        self.original_image = pygame.transform.rotate(self.original_image, -90)  # Otočenie o 90° doprava
        self.original_image = pygame.transform.scale(self.original_image,(self.width, self.height))  # Zmenšenie obrázka
        self.image = self.original_image

    def draw(self, screen):
        """Nakreslí raketku ako obrázok na obrazovku."""
        # Otočenie obrázka podľa uhla rakety
        rotated_image = pygame.transform.rotate(self.image, self.angle)


        # Nájdeme stred obrázka po otočení
        rect = rotated_image.get_rect(center=(self.x, self.y))

        # Vykreslenie obrázka
        screen.blit(rotated_image, rect.topleft)




    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity
