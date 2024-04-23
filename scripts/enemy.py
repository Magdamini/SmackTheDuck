import pygame

from scripts.fighter import Fighter


class Enemy(Fighter):
    def __init__(self, img, name, health, attack, defence, critical_dmg, agility, luck, moves, level=1):
        super().__init__(img, name, health, attack, defence, critical_dmg, agility, luck, moves, level)
        
        
    def render(self, surf, x, y):
        surf.blit(self.img, (x, y))
