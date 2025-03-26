import pygame
import sys

from game_states import GameStates
from scripts.utils import load_image, text_image


class StartScreen:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.next_state = GameStates.SELECT_PLAYER
        self.subtitle = text_image("Use any key to start", 10, "data/fonts/Retro.ttf")

    def run(self):
        self.display.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.update_manager()

        self.display.blit(load_image("scenes/opening_screen.png"), (0, 0))
        self.render_title()

    def update_manager(self):
        self.game_state_manager.set_state(self.next_state)
        return True

    def render_title(self):
        self.display.blit(
            self.subtitle,
            (
                self.display.get_width() // 2 - self.subtitle.get_width() // 2,
                self.display.get_height() - 40,
            ),
        )
