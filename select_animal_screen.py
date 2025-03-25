import pygame

from game_states import GameStates
from select_screen import SelectScreen
from map_screen import MapScreen
from scripts.animal import Animal
from scripts.minigame_squares import MinigameSquares
from scripts.minigame_shoot import MinigameSchoot
from scripts.utils import text_image

# [*attack, -defence, -stats]
MOVES = {
    "animals/cat.png": {
        "bite": [1, 0, 0],
        "hiss": [0, 0, 1],
        "jump_attack": [0.8, 2, 0],
        "scratch": [0.6, 7, 0],
    },
    "animals/dog.png": {
        "bite": [1.2, 0, 0],
        "bark": [0, 0, 1],
        "jump_attack": [0.8, 2, 0],
        "trample": [0.5, 10, 0],
    },
}


class SelectAnimalScreen(SelectScreen):
    def __init__(self, display, game_state_manager, game):
        self.options_str = ["animals/cat.png", "animals/dog.png"]
        self.animal_stats = [(8, 2, 1, 2, 2, 3), (11, 3, 2, 1, 1, 1)]
        super().__init__(
            display,
            game_state_manager,
            self.options_str,
            GameStates.STORY,
            "animal",
            size=128,
        )

        self.animals = []
        for i in range(len(self.options_str)):
            stats = self.animal_stats[i]
            animal = Animal(
                self.options_str[i],
                stats[0],
                stats[1],
                stats[2],
                stats[3],
                stats[4],
                stats[5],
                MOVES[self.options_str[i]],
                self.get_minigame(i),
            )
            self.animals.append(animal)

        self.game = game

        # draw
        self.border_offset = 10

    def get_minigame(self, i):
        minigames = {
            "animals/cat.png": MinigameSquares,
            "animals/dog.png": MinigameSchoot,
        }
        return minigames[self.options_str[i]]

    def update_manager(self):
        if super().update_manager():
            animal = self.animals[self.curr_option]
            player = self.game.select_player_screen.get_player()
            self.game.states[GameStates.MAP] = MapScreen(
                self.display, self.game_state_manager, animal, player, self.game
            )

    def render_character(self, character):
        self.display.blit(
            character,
            (
                self.display.get_width() // 4 - self.img_size // 2,
                self.display.get_height() // 2 - self.img_size // 2 - 10,
            ),
        )

    def render_desc(self, curr_y):
        title_text = text_image("Pet Statistics", 16)
        self.display.blit(
            title_text,
            (self.display.get_width() * 3 // 4 - title_text.get_width() // 2, curr_y),
        )
        left = self.display.get_width() // 2 + self.border_offset

        curr_y += 5 + title_text.get_height()

        line_offset = 3
        pygame.draw.line(
            self.display,
            (0, 0, 0),
            (left - line_offset, curr_y),
            (self.display.get_width() - self.border_offset + line_offset, curr_y),
        )
        curr_y += 4

        for stat, val in self.animals[self.curr_option].stats.items():
            stat_text = text_image(f"{stat.value}: {val}", 10)
            self.display.blit(stat_text, (left, curr_y))
            curr_y += 3 + stat_text.get_height()
