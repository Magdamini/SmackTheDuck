import pygame
from random import randint
from scripts.fighter_statictics import Stats

MAX_LVL = 15
BAR_OFFESET = 10


class LevelManager:
    def __init__(self, animal, item_collector, level=1):
        self.animal = animal
        self.item_collector = item_collector
        self.level = level
        self.xp = 0

        # draw
        self.width = 96
        self.height = 30
        self.border_width = 1
        self.bar_height = 14
        self.bar_width = self.width - 2 * BAR_OFFESET


    def xp_to_next_level(self, level):   
        if level == MAX_LVL: level -= 1
        return round( 0.04 * (level ** 3) + 0.8 * (level ** 2) + 2 * level) + 5
    
    
    def render(self, surf):
        background = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(surf, (255, 255, 255), background) 
        pygame.draw.rect(surf, (0, 0, 0),  background, self.border_width)
        
        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=10)
        lvl_text = text_font.render("Lvl. " + str(self.level), True, "black")
        surf.blit(lvl_text, ((self.width - lvl_text.get_width()) // 2, self.border_width))
        
        xp_bar = pygame.Rect(0, 0, self.bar_width, self.bar_height)   
        xp_bar.centerx = background.centerx
        xp_bar.bottom = background.bottom - self.border_width * 2
        
        next_xp = self.xp_to_next_level(self.level)
        
        xp_curr = pygame.Rect(xp_bar.x, xp_bar.y, int(self.xp / next_xp * self.bar_width), self.bar_height)  
        pygame.draw.rect(surf, (100, 100, 100), xp_bar)
        pygame.draw.rect(surf, (105, 245, 66), xp_curr)
        pygame.draw.rect(surf, (0,0,0), xp_bar, width=1)
        
        xp_text = text_font.render(str(self.xp) + "/" + str(next_xp), True, "black")
        surf.blit(xp_text, (xp_bar.centerx - xp_text.get_width() // 2, xp_bar.y + 1))
        

    def update(self, xp, available_maps):
        if self.level == MAX_LVL: return
        self.xp = max(0, self.xp + xp)
        if self.xp >= self.xp_to_next_level(self.level):
            self.level += 1
            self.animal.lvl = self.level
            
            if self.level == MAX_LVL: self.xp = self.xp_to_next_level(self.level)
            else: self.xp = 0
            
            # ile nowych przedmiotów
            new_items = round(len(available_maps))
            
            self.item_collector.new_random_items(available_maps, new_items)
            return NewLevelWindow(self.level, self.animal)
        
        
#######################################################################
    
class NewLevelWindow:
    def __init__(self, new_level, animal):
        self.new_level = new_level
        self.animal = animal
        self.finish = False
        
        # co podnosimy i mniej więcej o ile zawsze
        self.upgrade_stats = [(Stats.HEALTH, randint(3, 6)), (Stats.ATTACK, randint(2, 4)), (Stats.DEFENCE, randint(1, 3))]
        
        # losowe dwa z trzech pozostałych do upgradowania
        self.rand_stats = self.random_stats()
        self.chosen_stat = None
        
        # draw
        self.width = 140
        self.height = 165
        self.border_width = 2
        self.border_offset = 10

        
        
    def render(self, surf, scale):
        background = pygame.Rect(0, 0, self.width, self.height)
        background.center = (surf.get_width() // 2, surf.get_height() // 2)
        pygame.draw.rect(surf, (255, 255, 255), background) 
        pygame.draw.rect(surf, (0, 0, 0),  background, self.border_width)
        curr_y = background.y + 8
        
        big_text_font = pygame.font.Font("data/fonts/Retro.ttf", size=16)
        lvl_text = big_text_font.render("Level Up!", True, "black")
        surf.blit(lvl_text, (background.centerx - lvl_text.get_width() // 2, curr_y))
        left = background.x + self.border_offset
        
        curr_y += 10 + lvl_text.get_height()
        
        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=10)
        for stat, val in self.upgrade_stats:
            stat_text = text_font.render(f"+{val} {stat.value}", True, "black")
            surf.blit(stat_text, (left, curr_y))
            curr_y += 3 + stat_text.get_height()
        
        curr_y += 3
        
        line_offset = 3
        pygame.draw.line(surf, (0, 0, 0), (left - line_offset, curr_y), (background.right - self.border_offset + line_offset, curr_y))
        curr_y += 7
        
        choose_text = big_text_font.render(f"Select:", True, "black")
        surf.blit(choose_text, (background.centerx - choose_text.get_width() // 2, curr_y))
        curr_y += 5 + choose_text.get_height()
        
        texts = []
        for stat, val in self.rand_stats:
            stat_text = text_font.render(f"+{val} {stat.value}", True, "black")
            texts.append((stat_text, left, curr_y))
            surf.blit(stat_text, (left, curr_y))
            curr_y += 3 + stat_text.get_height()
            
        stat_no = self.select_option(surf, texts, scale)
        if stat_no is not None:
            self.chosen_stat = self.rand_stats[stat_no]
            
            
    def select_option(self, surf, texts, scale):
        pos = [p // scale for p in pygame.mouse.get_pos()]
        
        for i in range(len(texts)):
            txt, x, y = texts[i]
            rect = pygame.Rect(x, y, self.width - 2 * self.border_offset, txt.get_height())
            rect.x = x
            rect.y = y
            
            if rect.collidepoint(pos):
                pygame.draw.rect(surf, (120, 162, 222), rect)
                surf.blit(txt, (x, y))
                if pygame.mouse.get_pressed()[0]:
                    self.finish = True
                    return i
        
        
    def random_stats(self, n=2):
        all_stats = [Stats.CRITICAL_DMG, Stats.AGILITY, Stats.LUCK]
        rand_stats = []
        for _ in range(n):
            stat = all_stats.pop(randint(0, len(all_stats) - 1))
            val = randint(1, 2)                   
            rand_stats.append((stat, val))
        return rand_stats
    
    
    def is_finished(self):
        if self.finish:
            for stat, val in self.upgrade_stats:
                self.animal.stats[stat] += val
            if self.chosen_stat is not None:
                self.animal.stats[self.chosen_stat[0]] += self.chosen_stat[1]
        return self.finish
                    
    #     self.health = randint(8*level, 11*level)
    #     self.attack = randint(2*level, 3*level)
    #     self.defence = randint(level, int(level*1.5))
    #     self.critical_dmg = randint(0, 10)
    #     self.agility = randint(level, int(level*1.5))
    #     self.luck = randint(0, 10)
