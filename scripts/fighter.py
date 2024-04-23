import pygame

from scripts.utils import load_image, get_filename_without_extension
from scripts.fighter_statictics import Stats

class Fighter:
    def __init__(self, img, health, attack, defence, critical_dmg, agility, luck, moves, level, size=64):
        self.name = get_filename_without_extension(img)
        self.img = pygame.transform.scale(load_image(img), (size, size))
        self.stats = {Stats.HEALTH: health,
                      Stats.ATTACK: attack,
                      Stats.DEFENCE: defence,
                      Stats.CRITICAL_DMG: critical_dmg,
                      Stats.AGILITY: agility,
                      Stats.LUCK: luck}
        self.moves = moves
        self.lvl = level

        self.battle_stats = None


    def perform_attack(self, other, move):
        other.battle_stats[Stats.HEALTH] -= self.battle_stats[Stats.ATTACK] * self.moves[move]
        if other.battle_stats[Stats.HEALTH] < 1:
            return True
        return False


    def render(self, surf, x, y, width=None, height=None):
        if width and height:
            scaled_img = pygame.transform.scale(self.img, (width, height))
            surf.blit(scaled_img, (x, y))
        else:
            surf.blit(self.img, (x, y))
