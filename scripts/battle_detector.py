from random import randint
from scripts.fighter import Fighter
from game_states import GameStates


class Battle_detector:
    def __init__(self, game_state_manager, player, tilemap):
        self.player = player
        self.tilemap = tilemap
        self.battle_tile_loc = None
        self.previous_battle_tile_loc = None
        self.game_state_manager = game_state_manager

    
    def battle_chances(self, chance_of_battle=4):
        rand_num = randint(0, 99)
        return rand_num < chance_of_battle
    

    def detect_battle(self): # TODO polish this
        self.battle_tile_loc = (int((self.player.pos[0] + self.player.size[0] // 2) // self.tilemap.tile_size), int((self.player.pos[1] + self.player.size[1] // 2) // self.tilemap.tile_size))
        player_rect = self.player.rect()
        for rect in self.tilemap.battle_rects_around(self.player.pos):
            if player_rect.colliderect(rect) and self.battle_tile_loc != self.previous_battle_tile_loc and self.battle_chances():
                self.previous_battle_tile_loc = self.battle_tile_loc
                return True
        self.previous_battle_tile_loc = self.battle_tile_loc
        return False


    def update_manager(self):
        self.game_state_manager.set_state(GameStates.BATTLE)
