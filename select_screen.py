import pygame
import sys

from scripts.utils import Button, load_image, text_image

BUTTON_SIZE = [150, 60]

class SelectScreen:
    def __init__(self, display, game_state_manager, options, next_state, title, size=80):
        self.display = display
        self.game_state_manager = game_state_manager 
        self.img_size = size
        self.next_state = next_state
        self.title = text_image("SELECT " + title.upper(), 20, "data/fonts/Retro.ttf")
        self.subtitle = text_image("use arrows to change character", 10, "data/fonts/Retro.ttf")
        
        # TODO button
        self.button = Button(display.get_width() // 2 - BUTTON_SIZE[0] // 2, display.get_height() - BUTTON_SIZE[1] - 10, load_image("buttons/select.png"))
        
        self.options = {}
        i = 0
        for o in options:
            self.options[i] = pygame.transform.scale(load_image(o), (self.img_size, self.img_size))
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
        
        self.button.render(self.display)
        self.render_desc()
        self.display.blit(self.options[self.curr_option], (self.display.get_width() // 2 - self.img_size // 2, self.display.get_height() // 2 - self.img_size // 2))
        self.render_title()
        
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
            
    def render_desc(self):
        pass
    
    def get_selected_option(self):
        return self.options_str[self.curr_option]
    
    def render_title(self):
        self.display.blit(self.title, (self.display.get_width() // 2 - self.title.get_width() // 2, 10))
        self.display.blit(self.subtitle, (self.display.get_width() // 2 - self.subtitle.get_width() // 2, 15 + self.title.get_height()))