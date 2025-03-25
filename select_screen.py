import pygame
import sys

from scripts.utils import Button, load_image, text_image

PNG_SIZE = [35, 14]
BUTTON_SIZE = [size * 3 for size in PNG_SIZE]


class SelectScreen:
    def __init__(
        self, display, game_state_manager, options, next_state, title, size=128
    ):
        self.display = display
        self.game_state_manager = game_state_manager
        self.img_size = size
        self.next_state = next_state

        self.title = text_image("SELECT " + title.upper(), 20, "data/fonts/Retro.ttf")
        self.subtitle = text_image(
            "use arrows to change character", 10, "data/fonts/Retro.ttf"
        )

        self.button = Button(
            display.get_width() // 2 - BUTTON_SIZE[0] // 2,
            display.get_height() - BUTTON_SIZE[1] - 10,
            pygame.transform.scale(
                load_image("buttons/select.png"), (BUTTON_SIZE[0], BUTTON_SIZE[1])
            ),
        )

        self.options = {}
        i = 0
        for o in options:
            self.options[i] = pygame.transform.scale(
                load_image(o), (self.img_size, self.img_size)
            )
            i += 1

        self.curr_option = 0

        self.scroll = [False, False]

    def run(self):
        self.display.fill((250, 250, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.scroll[0] = True
                if event.key == pygame.K_RIGHT:
                    self.scroll[1] = True

        self.update()

        curr_y = 10

        curr_y = self.render_title(curr_y)
        self.render_desc(curr_y)
        self.render_character(self.options[self.curr_option])
        self.button.render(self.display)

        self.update_manager()
        self.scroll = [False, False]

    def update(self):
        if self.scroll[0]:
            self.curr_option = (self.curr_option + 1) % len(self.options)
        if self.scroll[1]:
            self.curr_option = (self.curr_option - 1) % len(self.options)

    def update_manager(self):
        if self.button.is_clicked():
            self.game_state_manager.set_state(self.next_state)
            return True
        return False

    def render_desc(self, curr_y):
        pass

    def render_character(self, character):
        self.display.blit(
            character,
            (
                self.display.get_width() // 2 - self.img_size // 2,
                self.display.get_height() // 2 - self.img_size // 2,
            ),
        )

    def get_selected_option(self):
        return self.options_str[self.curr_option]

    def render_title(self, curr_y):
        self.display.blit(
            self.title,
            (self.display.get_width() // 2 - self.title.get_width() // 2, curr_y),
        )
        curr_y += self.title.get_height() + 5
        self.display.blit(
            self.subtitle,
            (self.display.get_width() // 2 - self.subtitle.get_width() // 2, curr_y),
        )
        return curr_y + 20
