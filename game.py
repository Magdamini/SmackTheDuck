import pygame
from start_screen import StartScreen
from select_player_screen import SelectPlayerScreen
from select_animal_screen import SelectAnimalScreen
from end_screen import EndScreen
# from map_screen import MapScreen
# from battle_screen import BattleScreen
from game_states import GameStates


class Game:
    def __init__(self):        
        pygame.init()

        pygame.display.set_caption('Best game ever made')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.game_state_manager = GameStateManager(GameStates.START)
        # self.map_screen = MapScreen(self.display, self.game_state_manager, "animals/11.png", "basic")
        # self.battle_screen = BattleScreen(self.display, self.game_state_manager)
        self.start_screen = StartScreen(self.display, self.game_state_manager)
        self.select_player_screen = SelectPlayerScreen(self.display, self.game_state_manager)
        self.select_animal_screen = SelectAnimalScreen(self.display, self.game_state_manager, self)
        self.end_screen = EndScreen(self.display, self.game_state_manager)
        
        # trzeba pilnować żeby w każdym stanie był 'exit'
        self.states = {GameStates.START: self.start_screen,
                       GameStates.SELECT_PLAYER: self.select_player_screen,
                    #   GameStates.BATTLE: self.battle_screen,
                    #   GameStates.MAP: self.map_screen,
                       GameStates.SELECT_ANIMAL: self.select_animal_screen,
                       GameStates.END: self.end_screen}
        
        
    def run(self):
        while True:    
            self.states[self.game_state_manager.get_state()].run()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            
            
class GameStateManager:
    def __init__(self, start_state):
        self.curr_state = start_state
        self.scale = 2
        

    def get_state(self):
        return self.curr_state
    

    def set_state(self, state):
        self.curr_state = state        


if __name__ == '__main__':
    Game().run()
