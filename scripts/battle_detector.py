from random import randint
from scripts.fighter import Fighter
import pygame

FIGHT_TILES = {'GrassBushes', }


class Battle_detector:
    def __init__(self, player, fighting_player, tilemap):
        self.player = player
        self.tilemap = tilemap
        self.tile_loc = (self.player.pos[0] // self.tilemap.tile_size, self.player.pos[1] // self.tilemap.tile_size)
        self.previous_tile_loc = self.tile_loc
        self.fighting_player = fighting_player
        self.enemies = [Fighter("Kaczka Dzika", ["Z dzioba"], randint(fighting_player.level-1, fighting_player.level+1)),
                        Fighter("Gęś", ["Z dzioba"], randint(fighting_player.level-1, fighting_player.level+1)),
                        Fighter("Kaczka Krzyżówka", ["Z dzioba"], randint(fighting_player.level-1, fighting_player.level+1)),
                        Fighter("Bezpłetwiec", ["Z dzioba"], randint(fighting_player.level-1, fighting_player.level+1)),
                        Fighter("Wodniczka", ["Z dzioba"], randint(fighting_player.level-1, fighting_player.level+1))]
        
    
    def battle_chances(self, chance_of_battle=0):
        rand_num = randint(0, 99)
        return rand_num < chance_of_battle
    

    def detect_battle(self):
        self.tile_loc = (self.player.pos[0] // self.tilemap.tile_size, self.player.pos[1] // self.tilemap.tile_size)
        if self.tile_loc != self.previous_tile_loc:
            self.previous_tile_loc = self.tile_loc
            check_loc = str(self.tile_loc[0]) + ';' + str(self.tile_loc[1])
            if check_loc in self.tilemap.tilemap and self.tilemap.tilemap[check_loc]['type'] in FIGHT_TILES and self.battle_chances():
                print("\n !!!-- BATTLE DETECTED --!!! ")
                self.fighting_player.fight(self.enemies[randint(0, len(self.enemies)-1)])
