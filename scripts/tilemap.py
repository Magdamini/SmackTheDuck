import json

import pygame
from scripts.utils import load_json

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (0, 0)]
# TODO json for PHYSICS_TILES
PHYSICS_TILES = {'Cave': {1, 2, 3, 9, 10, 11, 12, 13, 14, 15},
                 'CaveOutside': {0, 1, 2, 3, 5, 6, 7, 8, 9, 10},
                 'CaveOutside00': {0, 1, 2, 3, 5}, # 4 - wejście
                 'CaveOutside01': {0, 1, 2, 3, 5}, # 4 - wejście
                 'CaveOutside02': {0, 1, 2, 3, 5}, # 4 - wejście
                 'GrassBuildings': {0, 1, 2, 3, 4},
                 'GrassBuildings00': {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19}, # 17 - wejście
                 'GrassBuildings01': {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},
                 'GrassBuildings02': {0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11}, 
                 'GrassBuildings03': {1, 3, 4, 5, 6, 7, 8},
                 'GrassBuildings04': {1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},
                 'GrassDecor': {0, 1, 2, 3, 4, 5, 6, 7, 8},
                 'GrassDecor00': {0, 1},
                 'GrassDecor02': {0, 1, 2, 3, 4, 5, 6, 7},
                 'GrassDecor03': {0, 1, 2, 3},
                 'GrassIndoorDecor': {0, 1, 2, 3, 4, 5, 6, 7, 8},
                 'GrassIndoorDecor05': {0, 1},
                 'GrassIndoorDecor06': {0, 1},
                 'GrassIndoorDecor07': {0, 1},
                 'GrassIndoorDecor08': {0, 1},
                 'GrassTrees': {0, 1},
                 'GrassTrees00': {0, 1, 2, 3},
                 'GrassTrees01': {1, 2, 4, 5, 6, 7, 8, 9, 10, 11},
                 'HouseFloor': {0, 1, 2, 3, 4, 5, 6, 7, 8}, # 21 - wejście
                 'HouseIndoor': {0, 1},
                 'HouseIndoor00': {0, 1, 2, 3},
                 'HouseIndoor01': {0, 1, 2, 3},
                 'WaterCatwalk': {2, 7, 8},
                 'WaterFloor': {0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13}}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.items = {}
        self.npc = {}
        self.bounds = None


    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    
    def rect_out_of_the_map(self, pos):
        outside_tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc not in self.tilemap:
                outside_tiles.append(pygame.Rect((tile_loc[0] + offset[0]) * self.tile_size, (tile_loc[1] + offset[1]) * self.tile_size, self.tile_size, self.tile_size))
        return outside_tiles
    

    def save(self, path):
        file = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size}, file)
        file.close


    def load(self, path):
        map_data = load_json(path)
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.bounds = self.get_bounds()
        
    def npc_rects(self, pos):
        npc_tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.npc:
                npc_tiles.append(pygame.Rect((tile_loc[0] + offset[0]) * self.tile_size, (tile_loc[1] + offset[1]) * self.tile_size, self.tile_size, self.tile_size))
        return npc_tiles


    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES.keys() and tile['variant'] in PHYSICS_TILES[tile['type']]:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
                
        return rects
    

    def forbidden_rects(self, pos):
        return self.physics_rects_around(pos) + self.rect_out_of_the_map(pos) + self.npc_rects(pos)


    def render(self, surf, offset=(0, 0)):
        for y in range(offset[1] // self.tile_size -4, (offset[1] + surf.get_height()) // self.tile_size + 4):
            for x in range(offset[0] // self.tile_size -4, (offset[0] + surf.get_width()) // self.tile_size + 4):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
                if loc in self.items:
                    self.items[loc].render(surf, offset)
                if loc in self.npc:
                    self.npc[loc].render(surf, offset)
        

    def get_bounds(self):
        inf = float('inf')
        left, right, up, down = inf, -inf, inf, -inf
        
        for key in self.tilemap:
            if key != 'background_color':
                x, y = self.tilemap[key]['pos']
                left = min(left, x)
                right = max(right, x)
                up = min(up, y)
                down = max(down, y)
        
        left *= self.tile_size
        right = (right + 1) * self.tile_size
        up *= self.tile_size
        down = (down + 1) * self.tile_size
        
        return [left, right], [up, down] 
    

    def add_item(self, item_type, x, y):
        new_item = item_type(x * self.tile_size, y * self.tile_size)
        self.items[str(x) + ";" + str(y)] = new_item


    def get_item(self, x, y):
        return self.items.pop(str(x) + ";" + str(y))
    
    def add_npc(self, npc):
        x, y = npc.pos
        self.npc[str(x // self.tile_size) + ";" + str(y // self.tile_size)] = npc
    

    def items_around(self, pos): 
        rects = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            x, y = tile_loc[0] + offset[0], tile_loc[1] + offset[1]
            check_loc = str(x) + ';' + str(y)
            if check_loc in self.items:
                rect = pygame.Rect(0, 0, self.tile_size // 2, 3 * self.tile_size // 4)
                rect.centerx = x * self.tile_size + self.tile_size // 2
                rect.bottom = y * self.tile_size + self.tile_size
                rects.append((x, y, rect))
        return rects
