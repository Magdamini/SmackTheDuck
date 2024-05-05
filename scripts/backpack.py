import pygame
from scripts.utils import Button

ROWS = 3
COLUMNS = 5
BORDER_WIDTH = 2

class Backpack:
    def __init__(self):
        self.items = {}
        self.spot_size = 50
        self.item_size = 32
        self.last_click = False
        
        
        self.border_offset = 10
        self.width = self.spot_size * COLUMNS + 4 * self.border_offset
        self.height = self.border_offset * 6 + self.spot_size * ROWS
        self.border_width = 2
        

        
    def update(self, new_item):
        if new_item.name == "Letter": return
        if self.items.get(new_item.name) is None:
            self.items[new_item.name] = [1, new_item, Button(0, 0, new_item.img)]
        else:
            self.items[new_item.name][0] += 1
    
    def render(self, surf, scale, get_item=False):
        item_to_ret = None
        background = pygame.Rect(0, 0, self.width, self.height)
        background.center = (surf.get_width() // 2, surf.get_height() // 2)
        pygame.draw.rect(surf, (255, 255, 255), background) 
        pygame.draw.rect(surf, (0, 0, 0),  background, self.border_width)
        curr_y = background.y + 4
        
        
        big_text_font = pygame.font.Font("data/fonts/Retro.ttf", size=16)
        backpack_text = big_text_font.render("Backpack", True, "black")
        surf.blit(backpack_text, (background.centerx - backpack_text.get_width() // 2, curr_y))
        left = background.x + self.border_offset
        curr_y += backpack_text.get_height() + 4
        
        
        backpack = pygame.Rect(left, curr_y, self.spot_size * COLUMNS, self.spot_size * ROWS)
        backpack.centerx = background.centerx
        
        pygame.draw.rect(surf, (97, 63, 40), backpack) 
        
        curr_items = sorted(list(self.items.keys()))
        
        i = 0
        for row in range(ROWS):
            for col in range(COLUMNS):
                curr_spot = pygame.Rect(0, 0, self.spot_size, self.spot_size)
                curr_spot.x = backpack.x + col * self.spot_size 
                curr_spot.y = backpack.y + row * self.spot_size
                
                pygame.draw.rect(surf, (0, 0, 0), curr_spot, self.border_width // 2)
                
                if i < len(curr_items):
                    if self.render_item(surf, curr_items[i], curr_spot, col, row, scale):   # myszka jest nad obrazkiem
                        item = self.items[curr_items[i]][1]
                        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=10)
                        item_text = text_font.render(f'{item.name}: {item.desc}', True, "black")
                        text_rect = pygame.Rect(0, 0, item_text.get_width(), item_text.get_height())
                        text_rect.centerx = background.centerx
                        text_rect.bottom = background.bottom - self.border_offset
                        surf.blit(item_text, (text_rect.x, text_rect.y))
                        
                        if get_item:
                            if pygame.mouse.get_pressed()[0]: # left button pressed
                                if not self.last_click:
                                    self.last_click = True
                                    item_to_ret = self.remove_item(curr_items[i])
                            else:
                                self.last_click = False
                                            
                i += 1
        

        pygame.draw.rect(surf, (0, 0, 0), backpack, self.border_width)
        return item_to_ret
        
        
    def render_item(self, surf, item, curr_spot, col, row, scale):
        item_rect = pygame.Rect(0, 0, self.item_size, self.item_size)
        item_rect.center = curr_spot.center
        item_img = self.items[item][1].img
        surf.blit(pygame.transform.scale(item_img, (self.item_size, self.item_size)), (item_rect.x, item_rect.y))
        
        
        offset_x = BORDER_WIDTH
        if col == 0: offset_x += self.border_width // 2
        
        offset_y = BORDER_WIDTH
        if row == 0: offset_y += self.border_width // 2
        
        quantity = self.items[item][0]
        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=12)
        text = text_font.render(str(quantity), True, "black")
        
        surf.blit(text, (curr_spot.x + offset_x, curr_spot.y + offset_y))
        
        pos = [p // scale for p in pygame.mouse.get_pos()]
        return item_rect.collidepoint(pos)
        
    
            
    def remove_item(self, item_name):
        if self.items[item_name][0] == 1:
            return self.items.pop(item_name)[1]
        else:
            self.items[item_name][0] -= 1
            return self.items[item_name][1]
