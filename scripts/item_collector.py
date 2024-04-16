import random
import pygame
from scripts.map_handler import ITEM_TYPES, MAP_CHANGE_TILES
from scripts.tilemap import PHYSICS_TILES

class ItemCollector:
    def __init__(self, player, maps):
        self.player = player
        self.maps = maps
        
        sizes = [((m.bounds[0][1] - m.bounds[0][0]) * (m.bounds[1][1] - m.bounds[1][0]), k) for k, m in maps.items() if k != "5a"]
        mini = float('inf')
        for s, _ in sizes:
            mini = min(s, mini)
        self.scale = [(s // mini, k) for s, k in sizes]
        self.item_list = list(ITEM_TYPES.keys())
        self.item_list.remove("14")
        
    def collect_items(self, tilemap): 
        items = tilemap.items_around(self.player.pos) 
        player_rect = self.player.rect()
        for x, y, rect in items:
            if player_rect.colliderect(rect):
                item = tilemap.get_item(x, y)

                self.player.backpack.update(item)
                print(f"New item collected: {item.name}")
                
                
    # maps -> słownik map z map_handlera
    # w jaskini bossa się nic nie pojawia
    def new_random_items(self, no_new_items=1):
        sum_size = sum([s[0] for s in self.scale])
        
        for _ in range(no_new_items):
            rand = random.randint(1, sum_size)
            curr = 0
            total_scale = self.scale[0][0]
            while rand > total_scale:
                curr += 1
                total_scale += self.scale[curr][0]
                
            curr_map = self.maps[self.scale[curr][1]]
            print(self.scale[curr][1])
            
            while True:
                x = random.randint(curr_map.bounds[0][0] // curr_map.tile_size, curr_map.bounds[0][1] // curr_map.tile_size - 1)
                y = random.randint(curr_map.bounds[1][0] // curr_map.tile_size, curr_map.bounds[1][1] // curr_map.tile_size - 1)
                if self.is_valid_pos(curr_map, self.scale[curr][1], x, y):
                    break
                
            new_item_type = random.choice(self.item_list)
            curr_map.add_item(ITEM_TYPES[new_item_type], x, y)
            
            # TODO - usunąć printa
            print(f"added new item map:{self.scale[curr][1]}; x: {x}, y: {y}")
            
            
                
    # nie może być na niewchodzącym kafelku, drzwiach, ludziku, już istniejącym przedmiocie    
    def is_valid_pos(self, tilemap, map_name, x, y):  
        item_rect = pygame.Rect(x * tilemap.tile_size, y * tilemap.tile_size, tilemap.tile_size, tilemap.tile_size)
        player_rect = self.player.rect()
        if item_rect.colliderect(player_rect):
            return False
        
        for loc, _, _ in MAP_CHANGE_TILES.get(map_name, ()):
            door_rect = pygame.Rect(loc[0] * tilemap.tile_size, loc[1] * tilemap.tile_size, tilemap.tile_size, tilemap.tile_size)
            if item_rect.colliderect(door_rect):
                return False
        
        tile = tilemap.tilemap.get(str(x) + ';' + str(y))
        if tile is None: return False
        
        if tile['type'] in PHYSICS_TILES.keys() and tile['variant'] in PHYSICS_TILES[tile['type']]:
            return False
        
        if tilemap.items.get(str(x) + ";" + str(y)) is not None:
            return False
        
        return True    
        
        
        
        
    # def show_item(self, item):
    #     self.display.blit(pygame.transform.scale(item.img, (item.big_size, item.big_size)), ((self.display.get_width() - item.big_size) // 2, (self.display.get_height() - item.big_size) // 2))
        
    #     font = pygame.font.SysFont(None, 25)
    #     text = "New item found!"
    #     img = font.render(text, True, (0, 0, 0))
    #     text_rect = img.get_rect(center=(self.display.get_width()//2, (self.display.get_height() + item.big_size * 4 // 3) // 2))
        
    #     self.display.blit(img, text_rect)
        
    #     self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
    #     pygame.display.update()