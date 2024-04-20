import pygame

ROWS = 3
COLUMNS = 5
BORDER_WIDTH = 2


# TODO -> co robimy z listem? w sensie czy go wgl trzymać w plecaku?

class Backpack:
    def __init__(self):
        self.items = {}
        self.spot_size = 56
        self.item_size = 32
        
    def update(self, new_item):
        if self.items.get(new_item.name) is None:
            self.items[new_item.name] = [1, new_item]
        else:
            self.items[new_item.name][0] += 1
        
        
    
    def render(self, surf):
        width, height = surf.get_width(), surf.get_height()
        background = pygame.Rect(0, 0, self.spot_size * COLUMNS, self.spot_size * ROWS)
        background.center = (width // 2, height // 2)
        
        pygame.draw.rect(surf, (97, 63, 40), background) 
        
        curr_items = list(self.items.keys())
        if "Letter" in curr_items: curr_items.remove("Letter")
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
        
        