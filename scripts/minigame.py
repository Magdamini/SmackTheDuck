from abc import ABC, abstractmethod
from scripts.utils import text_image, Button, load_image
from enum import Enum

import pygame


class MiniGameStates(Enum):
    START = 'start'
    WAIT = 'wait'
    PLAY = 'play'
    END = 'end'


START_BUTTON_SIZE = [size * 2 for size in (30, 14)]

EXIT_BUTTON_SIZE = [size * 2 for size in (22, 14)]

class MiniGame(ABC):
    def __init__(self, desc, name, surf):
        super().__init__()
        self.desc = desc
        self.name = name
        self.surf = surf
        self.finish = False
        self.start = False
        self.success = None
        self.curr_state = MiniGameStates.START
        
        # draw
        self.width = 300
        self.height = 220
        self.border_width = 2
        self.border_offset = 10
        self.font_size = 10
        self.header_height = 30
        
        
        self.background = pygame.Rect(0, 0, self.width, self.height)
        self.background.center = (surf.get_width() // 2, surf.get_height() // 2)
        
        # buttons
        
        self.button_offset = 5
        self.buttons = {MiniGameStates.START: Button(self.background.right - START_BUTTON_SIZE[0] - self.button_offset, self.background.bottom - START_BUTTON_SIZE[1] - self.button_offset,
                                                pygame.transform.scale(load_image("buttons/start.png"), (START_BUTTON_SIZE[0], START_BUTTON_SIZE[1]))),
                        MiniGameStates.END: Button(self.background.right - EXIT_BUTTON_SIZE[0] - self.button_offset, self.background.bottom - EXIT_BUTTON_SIZE[1] - self.button_offset,
                                                pygame.transform.scale(load_image("buttons/exit.png"), (EXIT_BUTTON_SIZE[0], EXIT_BUTTON_SIZE[1])))
                   }
        
    def render_background(self):
        pygame.draw.rect(self.surf, (255, 255, 255), self.background) 
        pygame.draw.rect(self.surf, (0, 0, 0),  self.background, self.border_width)
        
    # zwraca gdzie w lini y jesteś
    def render_header(self):
        name_text = text_image(self.name, 16)
        rect = name_text.get_rect()
        rect.center = (self.background.centerx, self.background.y + self.header_height // 2)
        self.surf.blit(name_text, (rect.x, rect.y))
        
        line_offset = 3
        line_y = self.background.y + self.header_height
        pygame.draw.line(self.surf, (0, 0, 0), (self.background.x + self.border_offset - line_offset, line_y), (self.background.right - self.border_offset + line_offset, line_y))
        
        
        desc_text = text_image(self.desc, self.font_size)
        rect = desc_text.get_rect()
        rect.centerx = self.background.centerx
        rect.y = self.background.y + self.header_height + 3
        self.surf.blit(desc_text, (rect.x, rect.y))
        
        return rect.bottom
    
    # zwraca czy już koniec i czy się wygrało
    def is_finished(self):
        return self.finish, self.success
        
    
    def render(self, scale):
        self.render_background()
        curr_y = self.render_header()
        self.render_game(scale)
    
    
    @abstractmethod
    def render_game(self, scale):
        pass
    
        
    