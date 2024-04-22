from game_states import GameStates
from select_screen import SelectScreen
from map_screen import MapScreen
from scripts.animal import Animal

class SelectAnimalScreen(SelectScreen):
    def __init__(self, display, game_state_manager, game):
        self.options_str = ["animals/cat.png", "animals/dog.png"]
        self.animal_stats = [(11, 2, 1, 1, 2, 3), (11, 3, 2, 2, 1, 1)]
        self.game = game
        super().__init__(display, game_state_manager, self.options_str, GameStates.MAP, "animal", size=128)
        
    
    def update_manager(self):
        if super().update_manager():
            animal_img = self.options_str[self.curr_option]
            animal = Animal(animal_img, 8, 2, 1, 1, 1, 1)
            player = self.game.select_player_screen.get_player()
            self.game.states[GameStates.MAP] = MapScreen(self.display, self.game_state_manager, animal, player)
            # walka
            
            
# Stats.HEALTH: health,
# Stats.ATTACK: attack,
# Stats.DEFENCE: defence,
# Stats.CRITICAL_DMG: critical_dmg,
# Stats.AGILITY: agility,
# Stats.LUCK: luck
    