from game_states import GameStates
from select_screen import SelectScreen
from map_screen import MapScreen
from scripts.animal import Animal

class SelectAnimalScreen(SelectScreen):
    def __init__(self, display, game_state_manager, game):
        self.options_str = ["animals/cat.png", "animals/17.png"]
        self.game = game
        super().__init__(display, game_state_manager, self.options_str, GameStates.MAP, "animal", size=64)
        
    
    def update_manager(self):
        if super().update_manager():
            animal_img = self.options_str[self.curr_option]
            animal = Animal(animal_img, 8, 2, 1, 1, 1, 1)
            player = self.game.select_player_screen.get_player()
            self.game.states[GameStates.MAP] = MapScreen(self.display, self.game_state_manager, animal, player)
            # walka
    