import pygame

from scripts.utils import load_image
from scripts.fighter_statictics import Stats

class Animal:
    def __init__(self, img, health, attack, defence, critical_dmg, agility, luck, size=64, level=1):
        self.img = pygame.transform.scale(load_image(img), (size, size))
        self.lvl = level
        
        self.stats = {Stats.HEALTH: health,
                      Stats.ATTACK: attack,
                      Stats.DEFENCE: defence,
                      Stats.CRITICAL_DMG: critical_dmg,
                      Stats.AGILITY: agility,
                      Stats.LUCK: luck}
        
        
    def render(self, surf, x, y):
        surf.blit(self.img, (x, y))
