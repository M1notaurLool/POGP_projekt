import pygame
from raketa import Raketa
from strela import Strela

pygame.init()

# Nastavenie okna
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Vytvoriť dve rakety pre dvoch hráčov
raketa1 = Raketa(400, 300, 'w', 'a', 'd', 'LCTRL', (0, 255, 0))  # Prvý hráč
raketa2 = Raketa(200, 300, 'up', 'left', 'right', 'space', (255, 0, 0))  # Druhý hráč

# Skupiny pre rakety a strely
raketa_group = pygame.sprite.Group()
raketa_group.add(raketa1, raketa2)

# Vytvoriť skupiny pre strely
strely_group = pygame.sprite.Group()

# Hlavná herná slučka
running = True
while running:
    screen.fill((0, 0, 0))  # Čierne pozadie

    # Udalosti
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                raketa1.shoot()  # Prvý hráč strieľa
            if event.key == pygame.K_RETURN:
                raketa2.shoot()  # Druhý hráč strieľa

    # Aktualizácie rakiet a strel
    raketa_group.update()
    strely_group.update()

    # Detekcia kolízií: Ak raketa1 zasiahne raketu2 (druhý hráč)
    for strela in strely_group:
        if isinstance(strela, Strela) and raketa2.rect.colliderect(strela.rect):
            strela.kill()  # Odstránime strelu
            raketa1.pricitaj_skore(1)  # Zvyšujeme skóre pre hráča 1
            print(f"Player 1 Score: {raketa1.score}")  # Tlač skóre hráča 1
        elif isinstance(strela, Strela) and raketa1.rect.colliderect(strela.rect):
            strela.kill()  # Odstránime strelu
            raketa2.pricitaj_skore(1)  # Zvyšujeme skóre pre hráča 2
            print(f"Player 2 Score: {raketa2.score}")  # Tlač skóre hráča 2

    # Zobrazenie skóre
    font = pygame.font.Font(None, 36)
    score_text1 = font.render(f"Player 1 Score: {raketa1.score}", True, (255, 255, 255))
    score_text2 = font.render(f"Player 2 Score: {raketa2.score}", True, (255, 255, 255))
    screen.blit(score_text1, (10, 10))  # Zobrazenie skóre hráča 1
    screen.blit(score_text2, (600, 10))  # Zobrazenie skóre hráča 2

    # Vykreslenie rakiet a strel
    raketa_group.draw(screen)
    strely_group.draw(screen)

    pygame.display.flip()  # Aktualizácia obrazovky
    clock.tick(60)  # 60 FPS

pygame.quit()
