import pygame
import sys

from game_states import GameStates
from scripts.utils import load_image, text_image


class EndScreen:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.title = text_image(
            "Thank you \n for playing our game", 20, "data/fonts/Retro.ttf"
        )
        self.subtitle = text_image(
            "Credits \n Magdalena Pabisz - everything \n Olgierd Smyka - everything as well",
            10,
            "data/fonts/Retro.ttf",
        )

    def run(self):
        self.display.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    self.update_manager()

        self.render_title()

    def get_player(self):
        return self.options_str[self.curr_option]

    def update_manager(self):
        self.game_state_manager.set_state(GameStates.MAP)
        return True

    def render_title(self):
        self.display.blit(
            self.title,
            (self.display.get_width() // 2 - self.title.get_width() // 2, 50),
        )
        self.display.blit(
            self.subtitle,
            (
                self.display.get_width() // 2 - self.subtitle.get_width() // 2,
                70 + self.title.get_height(),
            ),
        )
