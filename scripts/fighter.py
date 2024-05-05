import pygame

from random import randint
from scripts.utils import load_image, get_filename_without_extension, text_image
from scripts.fighter_statictics import Stats
import math

DMG_FONT_SIZE = 32

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
        critical_dmg = False

        if self.battle_stats[Stats.CRITICAL_DMG] * 5 > randint(0, 99):
            times = 2
            critical_dmg = True

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

        dmg_text = self.get_dmg_text(dmg_delt, critical_dmg)
        return dmg_text, other
    

    def get_dmg_text(self, dmg_delt, critical_dmg):
        if critical_dmg:
            dmg_text = text_image(str(dmg_delt), DMG_FONT_SIZE + 10, "data/fonts/Retro.ttf", color=(255, 0, 0)) # critical_hit -> red
        else:
            dmg_text = text_image(str(dmg_delt), DMG_FONT_SIZE, "data/fonts/Retro.ttf", color=(0, 255, 255))
        return dmg_text


    def render(self, surf, x, y, width=None, height=None):
        if width and height:
            scaled_img = pygame.transform.scale(self.img, (width, height))
            surf.blit(scaled_img, (x, y))
        else:
            surf.blit(self.img, (x, y))


    def render_battle_statistics(self, surf, x, y):
        table_width = 120
        table_height = 38
        table_boarder_width = 2
        table_offset = 5
    
        background = pygame.Rect(x, y, table_width, table_height)
        pygame.draw.rect(surf, (255, 255, 255), background)
        pygame.draw.rect(surf, (0, 0, 0),  background, table_boarder_width)
        curr_y = background.y + table_offset
        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=10)        
        
        ################## LVL
        stat_text = text_font.render(f"LVL: {self.lvl}", True, "black")
        surf.blit(stat_text, (x+table_offset, curr_y))
        curr_y += 2 + stat_text.get_height()

        ################## HP
        health_bar_width = 80
        health_bar_height = 10

        stat_text = text_font.render("HP", True, "black")
        surf.blit(stat_text, (x+table_offset, curr_y))
        curr_y += 1

        h_rect = pygame.Rect(x+24, curr_y, health_bar_width, health_bar_height)
        pygame.draw.rect(surf, (0, 0, 0), h_rect)

        stat_len = round(self.battle_stats[Stats.HEALTH]/self.stats[Stats.HEALTH] * health_bar_width)
        h_rect = pygame.Rect(x+24, curr_y, stat_len, health_bar_height)
        pygame.draw.rect(surf, (255, 100, 100),  h_rect)


    def render_other_battle_statistics(self, surf, x, y):
        width = 120
        height = 100
        border_width = 2
        border_offset = 5

        background = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surf, (255, 255, 255), background) 
        pygame.draw.rect(surf, (0, 0, 0),  background, border_width)
        curr_y = background.y + border_offset
        left = background.x + border_offset        
        
        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=10)

        stat_names = ["Health", "Attack", "Defence", "Crit. damage", "Agility", "Luck"]
        for i, (stat, val) in enumerate(self.battle_stats.items()):
            if self.battle_stats[stat] < self.stats[stat]:
                stat_text = text_font.render(stat_names[i] + f": {val}", True, "red")
            elif self.battle_stats[stat] > self.stats[stat]:
                stat_text = text_font.render(stat_names[i] + f": {val}", True, "green")
            else:
                stat_text = text_font.render(stat_names[i] + f": {val}", True, "black")
            surf.blit(stat_text, (left, curr_y))
            curr_y += 3 + stat_text.get_height()

    """
        table_width = 120
        table_height = 100
        curr_y = 17 + y

        ################## OTHER STATS
        pentagon_center = (x + table_width//2, curr_y + table_height//2)
        
        points_stats = {Stats.ATTACK: round(200*self.battle_stats[Stats.ATTACK]/10),
                        Stats.DEFENCE: round(200*self.battle_stats[Stats.DEFENCE]/10),
                        Stats.CRITICAL_DMG: round(200*self.battle_stats[Stats.CRITICAL_DMG]/10),
                        Stats.AGILITY: round(200*self.battle_stats[Stats.AGILITY]/10),
                        Stats.LUCK: round(200*self.battle_stats[Stats.LUCK]/10)}
            
        
        points = [None for _ in range(5)]
        points[0] = (pentagon_center[0], pentagon_center[1] - points_stats[Stats.ATTACK])
        points[1] = (pentagon_center[0] - points_stats[Stats.DEFENCE]*math.cos(math.pi * 16/180), pentagon_center[1] - points_stats[Stats.DEFENCE]*math.sin(math.pi * 16/180))
        points[2] = (pentagon_center[0] - points_stats[Stats.CRITICAL_DMG]*math.cos(math.pi * 58/180), pentagon_center[1] + points_stats[Stats.CRITICAL_DMG]*math.sin(math.pi * 58/180))
        points[3] = (pentagon_center[0] + points_stats[Stats.AGILITY]*math.cos(math.pi * 58/180), pentagon_center[1] + points_stats[Stats.AGILITY]*math.sin(math.pi * 58/180))
        points[4] = (pentagon_center[0] + points_stats[Stats.LUCK]*math.cos(math.pi * 16/180), pentagon_center[1] - points_stats[Stats.LUCK]*math.sin(math.pi * 16/180))

        # stat_text = text_font.render(f"{stat.value}: {val}", True, "black")
        # surf.blit(stat_text, (x+4, curr_y))
        pygame.draw.polygon(surf, (127, 23, 246), points)
    """
