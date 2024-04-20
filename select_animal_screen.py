from game_states import GameStates
from select_screen import SelectScreen
from map_screen import MapScreen

class SelectAnimalScreen(SelectScreen):
    def __init__(self, display, game_state_manager, game):
        self.options_str = ["animals/cat.png", "animals/17.png"]
        self.game = game
        super().__init__(display, game_state_manager, self.options_str, GameStates.MAP, "animal", size=64)
        
    
    def update_manager(self):
        if super().update_manager():
            animal = self.options_str[self.curr_option]
            player = self.game.select_player_screen.get_player()
            self.game.states[GameStates.MAP] = MapScreen(self.display, self.game_state_manager, animal, player)
            # walka
    