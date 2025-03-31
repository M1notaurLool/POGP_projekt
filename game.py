import pygame
from player import Player
from enemy import Enemy
from powerup import PowerUp
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    def __init__(self):
        self.players = [
            Player(200, 300, "up", "left", "right", "space"),
            Player(600, 300, "w", "a", "d", "control")
        ]
        self.enemies = [Enemy()]
        self.powerups = [PowerUp()]

    def update(self):
        for player in self.players:
            player.update()
        for enemy in self.enemies:
            enemy.update()
        for powerup in self.powerups:
            powerup.update()
            for player in self.players:
                if powerup.collides_with(player):
                    if powerup.type == "boost":
                        player.activate_boost()
                    elif powerup.type == "shield":
                        player.activate_shield()
                    self.powerups.remove(powerup)

    def draw(self, screen):
        for player in self.players:
            player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for powerup in self.powerups:
            powerup.draw(screen)