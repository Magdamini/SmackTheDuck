import pygame
from scripts.utils import Button

ROWS = 3
COLUMNS = 5
BORDER_WIDTH = 2

class Backpack:
    def __init__(self):
        self.items = {}
        self.spot_size = 56
        self.item_size = 32
        self.last_click = False

        
    def update(self, new_item):
        if new_item.name == "Letter": return
        if self.items.get(new_item.name) is None:
            self.items[new_item.name] = [1, new_item, Button(0, 0, new_item.img)]
        else:
            self.items[new_item.name][0] += 1

    
    def render(self, surf):
        width, height = surf.get_width(), surf.get_height()
        background = pygame.Rect(0, 0, self.spot_size * COLUMNS, self.spot_size * ROWS)
        background.center = (width // 2, height // 2)
        
        pygame.draw.rect(surf, (97, 63, 40), background) 
        
        curr_items = sorted(list(self.items.keys()))
        
        i = 0
        for row in range(ROWS):
            for col in range(COLUMNS):
                curr_spot = pygame.Rect(0, 0, self.spot_size, self.spot_size)
                curr_spot.x = background.x + col * self.spot_size 
                curr_spot.y = background.y + row * self.spot_size
                
                pygame.draw.rect(surf, (0, 0, 0), curr_spot, BORDER_WIDTH // 2)
                
                if i < len(curr_items):
                    self.render_item(surf, curr_items[i], curr_spot, col, row)             
                i += 1
        

        pygame.draw.rect(surf, (0, 0, 0), background, BORDER_WIDTH)
        
        
    def render_item(self, surf, item, curr_spot, col, row):
        item_rect = pygame.Rect(0, 0, self.item_size, self.item_size)
        item_rect.center = curr_spot.center
        item_img = self.items[item][1].img
        surf.blit(pygame.transform.scale(item_img, (self.item_size, self.item_size)), (item_rect.x, item_rect.y))
        
        offset_x = BORDER_WIDTH
        if col == 0: offset_x += BORDER_WIDTH // 2
        
        offset_y = BORDER_WIDTH
        if row == 0: offset_y += BORDER_WIDTH // 2
        
        quantity = self.items[item][0]
        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=15)
        text = text_font.render(str(quantity), True, "black")
        
        surf.blit(text, (curr_spot.x + offset_x, curr_spot.y + offset_y))
        
        
    # # zwraca None jeśli nie kliknięto w nic, jak kliknięto to zmniejsza wartość w plecaku i zwraca item
    def get_clicked_item(self, surf, scale=2):
        pos = [p // scale for p in pygame.mouse.get_pos()]
        offset_x = (surf.get_width() - COLUMNS * self.spot_size) // 2
        offset_y = (surf.get_height() - ROWS * self.spot_size) // 2
        
        curr_items = sorted(list(self.items.keys()))
        i = 0
        
        for row in range(ROWS):
            for col in range(COLUMNS):
                if row * COLUMNS + col == len(curr_items):
                    return None
        
                rect = pygame.Rect(0, 0, self.item_size, self.item_size)
                rect.x = offset_x + col * self.spot_size + (self.spot_size - self.item_size) // 2
                rect.y = offset_y + row * self.spot_size + (self.spot_size - self.item_size) // 2
            
                if rect.collidepoint(pos):  # mouse over button
                    if pygame.mouse.get_pressed()[0]: # left button pressed
                        if not self.last_click:
                            self.last_click = True
                            return self.remove_item(curr_items[i])
                    else:
                        self.last_click = False
                        
                    
                i += 1
            
    def remove_item(self, item_name):
        if self.items[item_name][0] == 1:
            return self.items.pop(item_name)[1]
        else:
            self.items[item_name][0] -= 1
            return self.items[item_name][1]
                
        
                
                
        
        
        