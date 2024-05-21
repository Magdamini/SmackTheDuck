from scripts.utils import text_image
import pygame

ACTIONS = ["Use arrows to move", "Backpack", "Statistics", "Help", "Talk to NPC", "Close"]
KEYS = ["", "B", "V", "H", "T", "Q"]

class HelpWindow:
    def __init__(self):
        self.title_size = 16
        self.txt_size = 10
        
        self.title = text_image("Help", self.title_size)
        
        self.arrows_text = text_image("Use arrows to move", self.txt_size)
        
        self.action_text = text_image("\n".join(ACTIONS), self.txt_size)
        self.key_text = text_image("\n".join(KEYS), self.txt_size)
        
        # draw
        self.border_offset = 10
        self.width = 180
        self.height = self.title.get_height() + self.arrows_text.get_height() + self.action_text.get_height() + int(2 * self.border_offset)
        self.border_width = 2
 
    def render(self, surf):
        background = pygame.Rect(0, 0, self.width, self.height)
        background.center = (surf.get_width() // 2, surf.get_height() // 2)
        pygame.draw.rect(surf, (255, 255, 255), background) 
        pygame.draw.rect(surf, (0, 0, 0),  background, self.border_width)
        curr_y = background.y + self.border_offset
        
        surf.blit(self.title, (background.centerx - self.title.get_width() // 2, curr_y))
        curr_y += self.border_offset  // 2 + self.title.get_height()
        
        line_offset = 3
        pygame.draw.line(surf, (0, 0, 0), (background.x + self.border_offset - line_offset, curr_y), (background.right - self.border_offset + line_offset, curr_y))
        
        curr_y += self.border_offset // 2

        
        left = background.x + 2 * self.border_offset
        right = background.right - 2 * self.border_offset
        
        right_rect = self.key_text.get_rect()
        right_rect.right = right
        surf.blit(self.action_text, (left, curr_y))
        surf.blit(self.key_text, (right_rect.left, curr_y))