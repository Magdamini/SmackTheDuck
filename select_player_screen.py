from game_states import GameStates
from select_screen import SelectScreen


class SelectPlayerScreen(SelectScreen):
    def __init__(self, display, game_state_manager):
        self.options_str = ["basic", "red", 'green']
        options = [f"player/{opt}/0;0.png" for opt in self.options_str]
        super().__init__(display, game_state_manager, options, GameStates.SELECT_ANIMAL, "player")


    def get_player(self):
        return self.options_str[self.curr_option]
    