import pygame

from scripts.utils import load_image
from scripts.fighter import Fighter


class Animal(Fighter):
    def __init__(self, img, health, attack, defence, critical_dmg, agility, luck, moves, size=64, level=1):
        super().__init__(img, health, attack, defence, critical_dmg, agility, luck, moves, level)
        
        self.img = pygame.transform.scale(load_image(img), (size, size))
        self.xp_gained = 0
        
        # draw
        self.width = 180
        self.height = 140
        self.border_width = 2
        self.border_offset = 10
        self.stat_img_size = 64
        
        self.stat_img = self.img
        
        
    def render_statistics(self, surf):
        animal_rect = pygame.Rect(0, 0, self.stat_img_size, self.stat_img_size)
        background = pygame.Rect(0, 0, self.width, self.height)
        background.center = (surf.get_width() // 2, surf.get_height() // 2)
        pygame.draw.rect(surf, (255, 255, 255), background) 
        pygame.draw.rect(surf, (0, 0, 0),  background, self.border_width)
        curr_y = background.y + 8
        
        big_text_font = pygame.font.Font("data/fonts/Retro.ttf", size=16)
        title_text = big_text_font.render("Pet Statistics", True, "black")
        surf.blit(title_text, (background.centerx - title_text.get_width() // 2, curr_y))
        left = background.x + self.border_offset
        
        curr_y += 5 + title_text.get_height()
        
        line_offset = 3
        pygame.draw.line(surf, (0, 0, 0), (left - line_offset, curr_y), (background.right - self.border_offset + line_offset, curr_y))
        curr_y += 4
        
        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=10)
        for stat, val in self.stats.items():
            stat_text = text_font.render(f"{stat.value}: {val}", True, "black")
            surf.blit(stat_text, (left, curr_y))
            curr_y += 3 + stat_text.get_height()
        
        animal_rect.right = background.right
        animal_rect.bottom = curr_y - 2 * 3 - stat_text.get_height()
        
        surf.blit(self.stat_img, (animal_rect.x, animal_rect.y))
