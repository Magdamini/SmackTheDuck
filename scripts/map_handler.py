from scripts.tilemap import Tilemap
import pygame
# (16, -32)
MAP_CHANGE_TILES = {"0": [((9, 14), "1", (16, -24))],
                    "1": [((1, -3.5), "0", (144, 208)), ((68.5, -8), "2", (8, 128))],
                    "2": [((-0.5, 8), "1", (1080, -128)), ((77.5, 29), "3", (8, 176))],
                    "3": [((-0.5, 11), "2", (1224, 464)), ((129.5, 11), "4", (-40, 160))],
                    "4": [((-3.5, 10), "3", (2056, 176)), ((39.5, 11), "5", (8, 352)), ((13, 4.5), "5a", (160, 280))],
                    "5": [((-0.5, 22), "4", (616, 176))],
                    "5a": [((10, 18.5), "4", (208, 88))]}


class MapHandler():
    def __init__(self, game, player):
        self.game = game
        self.maps = {}
        for i in range(6):
            self.maps[str(i)] = Tilemap(game)
            self.maps[str(i)].load(f'data/maps/{i}.json')
        self.maps["5a"] = Tilemap(game)
        self.maps["5a"].load('data/maps/5a.json')
        
        
        self.curr_map = "0"
        self.player = player
        
    def get_curr_map(self):
        return self.maps[self.curr_map]
    
    def change_map(self):
        tile_size = self.get_curr_map().tile_size
        player_rect = self.player.rect()
        
        for loc, new_map, new_pos in MAP_CHANGE_TILES.get(self.curr_map, ()):
            door_rect = pygame.Rect(loc[0] * tile_size, loc[1] * tile_size, tile_size, tile_size)
            
            print(door_rect, player_rect)
            if player_rect.colliderect(door_rect):
                self.curr_map = new_map
                self.player.pos = list(new_pos)
                self.game.tilemap = self.get_curr_map()
                self.game.camera.set_map(self.get_curr_map())

            