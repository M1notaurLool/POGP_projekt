import pygame
import os
os.environ["SDL_AUDIODRIVER"] = "dummy"
from game import Game
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game = Game()

running = True
while running:
    screen.fill((0, 0, 0))  # Čierne pozadie
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    game.update()
    game.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()