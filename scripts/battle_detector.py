from random import randint
from scripts.fighter import Fighter
from game_states import GameStates

FIGHT_TILES = {'GrassBushes', }


class Battle_detector:
    def __init__(self, game_state_manager, player, tilemap):
        self.player = player
        self.tilemap = tilemap
        self.tile_loc = (self.player.pos[0] // self.tilemap.tile_size, self.player.pos[1] // self.tilemap.tile_size)
        self.previous_tile_loc = self.tile_loc
        self.game_state_manager = game_state_manager

    
    def battle_chances(self, chance_of_battle=20):
        rand_num = randint(0, 99)
        return rand_num < chance_of_battle
    

    def detect_battle(self):
        self.tile_loc = (self.player.pos[0] // self.tilemap.tile_size, self.player.pos[1] // self.tilemap.tile_size)
        if self.tile_loc != self.previous_tile_loc:
            self.previous_tile_loc = self.tile_loc
            check_loc = str(self.tile_loc[0]) + ';' + str(self.tile_loc[1])
            if check_loc in self.tilemap.tilemap and self.tilemap.tilemap[check_loc]['type'] in FIGHT_TILES and self.battle_chances():
                self.update_manager()
                return True
        return False


    def update_manager(self):
        self.game_state_manager.set_state(GameStates.BATTLE)
