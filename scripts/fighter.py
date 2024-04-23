import pygame

from scripts.utils import load_image
from scripts.fighter_statictics import Stats

class Fighter:
    def __init__(self, img, name, health, attack, defence, critical_dmg, agility, luck, moves, level, size=64):
        self.name = name
        self.img = pygame.transform.scale(load_image(img), (size, size))
        self.stats = {Stats.HEALTH: health,
                      Stats.ATTACK: attack,
                      Stats.DEFENCE: defence,
                      Stats.CRITICAL_DMG: critical_dmg,
                      Stats.AGILITY: agility,
                      Stats.LUCK: luck}
        self.moves = moves
        self.lvl = level


    def perform_attack(self, other, move):
        other.stats[Stats.HEALTH] -= self.stats[Stats.ATTACK] * self.moves[move]
        if other.stats[Stats.HEALTH] < 1:
            return True
        return False
