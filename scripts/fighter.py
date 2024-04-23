import pygame

from random import randint
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
        times = 1
        if self.battle_stats[Stats.CRITICAL_DMG] * 5 > randint(0, 99):
            times = 2

        dmg_blocked = other.battle_stats[Stats.DEFENCE] - self.moves[move][1] if other.battle_stats[Stats.DEFENCE] > self.moves[move][1] else 0

        if times * int(self.battle_stats[Stats.ATTACK] * self.moves[move][0]) > dmg_blocked:
            dmg_delt = times * round(self.battle_stats[Stats.ATTACK] * self.moves[move][0]) - dmg_blocked 
        else:
            dmg_delt = 0
        other.battle_stats[Stats.HEALTH] -= dmg_delt

        if self.moves[move][2] > 0:

            if other.battle_stats[Stats.DEFENCE] < self.moves[move][2]:
                other.battle_stats[Stats.DEFENCE] = 0
            else:
                other.battle_stats[Stats.DEFENCE] -= self.moves[move][2]

            if other.battle_stats[Stats.ATTACK] < self.moves[move][2]:
                other.battle_stats[Stats.ATTACK] = 0
            else:
                other.battle_stats[Stats.ATTACK] -= self.moves[move][2]

            if other.battle_stats[Stats.CRITICAL_DMG] < self.moves[move][2]:
                other.battle_stats[Stats.CRITICAL_DMG] = 0
            else:
                other.battle_stats[Stats.CRITICAL_DMG] -= self.moves[move][2]

            if other.battle_stats[Stats.LUCK] < self.moves[move][2]:
                other.battle_stats[Stats.LUCK] = 0
            else:
                other.battle_stats[Stats.LUCK] -= self.moves[move][2]

            if other.battle_stats[Stats.AGILITY] < self.moves[move][2]:
                other.battle_stats[Stats.AGILITY] = 0
            else:
                other.battle_stats[Stats.AGILITY] -= self.moves[move][2]

        if other.battle_stats[Stats.HEALTH] < 1:
            return True
        return False

# def perform_attack(self, other, move):
#         other.stats[Stats.HEALTH] -= self.stats[Stats.ATTACK] * self.moves[move]
#         if other.stats[Stats.HEALTH] < 1:
#             return True
#         return False


    def render(self, surf, x, y, width=None, height=None):
        if width and height:
            scaled_img = pygame.transform.scale(self.img, (width, height))
            surf.blit(scaled_img, (x, y))
        else:
            surf.blit(self.img, (x, y))
