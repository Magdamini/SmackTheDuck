import pygame
import sys

from game_states import GameStates
from scripts.utils import load_image, text_image


class StoryScreen:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.next_state = GameStates.MAP
        self.story = """
You've just woke up in your house and
realised that your wife is gone! What
could happen to her? She was sick and
couldn't even feed her favorite ducks,
so how could she leave the house on her
own?! You know someone must have had a
hand in this. But who? At the same
moment you notice a few duck feathers
lying right next to the door..."""
        self.info = text_image(
            "[Press any key to continue]", 10, "data/fonts/Retro.ttf"
        )

        self.feathers = [
            load_image("/scenes/feather1.png"),
            load_image("/scenes/feather2.png"),
        ]

    def run(self):
        self.display.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.update_manager()

        y = self.render_story()
        self.render_line(y + 20)
        self.render_info()

    def render_story(self):
        curr_y = 20
        lines = self.story.split("\n")
        for line in lines:
            txt = text_image(line, 10)
            rect = txt.get_rect()
            rect.centerx = self.display.get_width() // 2
            rect.y = curr_y
            curr_y += txt.get_height()
            self.display.blit(txt, (rect.x, rect.y))

        return curr_y

    def render_line(self, y):
        size = 20
        offset = size - 16
        n = self.display.get_width() // size
        left = (self.display.get_width() - n * size) // 2 + offset // 2
        for i in range(n):
            f = self.feathers[i % len(self.feathers)]
            self.display.blit(f, (left, y))
            left += size

    def update_manager(self):
        self.game_state_manager.set_state(self.next_state)
        return True

    def render_info(self):
        self.display.blit(
            self.info,
            (
                self.display.get_width() // 2 - self.info.get_width() // 2,
                self.display.get_height() - 30,
            ),
        )
