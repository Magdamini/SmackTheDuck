from scripts.minigame import MiniGameStates, MiniGame
from scripts.utils import Button, load_image
from random import randint
import pygame

SUBMIT_BUTTON_SIZE = [size * 2 for size in (34, 14)]

class MinigameSquares(MiniGame):
    def __init__(self, surf):
        name = "MINIGAME"
        desc = "Remember the positions of the blue\n squares and them click on them"
        super().__init__(desc, name, surf)
        
        self.buttons[MiniGameStates.PLAY] = Button(self.background.right - SUBMIT_BUTTON_SIZE[0] - self.button_offset, self.background.bottom - SUBMIT_BUTTON_SIZE[1] - self.button_offset,
                                                pygame.transform.scale(load_image("buttons/submit.png"), (SUBMIT_BUTTON_SIZE[0], SUBMIT_BUTTON_SIZE[1])))
        
        
        print(self.buttons)
        self.square_size = 24
        self.rows = 5
        self.cols = 8
        self.right_offset = 80
        
        self.squares = []
        self.player_squares = []
        self.rand_squares(8)
        self.verified_answer = None
        
        self.last_click = True
        self.curr_frame = 0
        self.max_animation_frame = 25       # jak długo ma się wyświetlać wzór
        
    
    def rand_squares(self, n=10):
        cnt = 0
        while cnt < n:
            row = randint(0, self.rows - 1)
            col = randint(0, self.cols - 1)
            if (row, col) not in self.squares:
                self.squares.append((row, col))
                cnt += 1
                
                
    def check_answer(self):
        correct, wrong, missing = [], [], []
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                if pos in self.squares and pos in self.player_squares:
                    correct.append(pos)
                elif pos in self.squares and pos not in self.player_squares:
                    missing.append(pos)
                elif pos not in self.squares and pos in self.player_squares:
                    wrong.append(pos)
        return correct, wrong, missing
                
                
    def draw_squares(self, scale, sqrs, color=(255, 255, 255), click=False):
        sq_background = pygame.Rect(0, 0, self.square_size * self.cols, self.square_size * self.rows)
        sq_background.centerx = self.background.left + (self.width - self.right_offset) // 2
        sq_background.bottom = self.background.bottom - 2 * self.border_offset
        pygame.draw.rect(self.surf, (0, 0, 0),  sq_background, self.border_width)
        
        for row in range(self.rows):
            for col in range(self.cols):
                curr_spot = pygame.Rect(0, 0, self.square_size, self.square_size)
                curr_spot.x = sq_background.x + col * self.square_size 
                curr_spot.y = sq_background.y + row * self.square_size
                
                if (row, col) in sqrs:
                    pygame.draw.rect(self.surf, color, curr_spot)
                
                pygame.draw.rect(self.surf, (0, 0, 0), curr_spot, self.border_width // 2)
                
                pos = [p // scale for p in pygame.mouse.get_pos()]
                if click and curr_spot.collidepoint(pos):
                    if pygame.mouse.get_pressed()[0]:
                        if not self.last_click:
                            self.last_click = True
                            if (row, col) not in sqrs:
                                sqrs.append((row, col))
                            else:
                                sqrs.remove((row, col))
                    else:
                        self.last_click = False
        
        pygame.draw.rect(self.surf, (0, 0, 0),  sq_background, self.border_width)
        
        
    def render_game(self, scale):
        curr_button = self.buttons.get(self.curr_state)
        if curr_button is not None: curr_button.render(self.surf, scale)
        
        if self.curr_state == MiniGameStates.START:
            self.draw_squares(scale, self.player_squares)
            if self.buttons[MiniGameStates.START].is_clicked():
                self.curr_state = MiniGameStates.WAIT
                
        elif self.curr_state == MiniGameStates.WAIT:
            self.curr_frame += 1
            self.draw_squares(scale, self.squares, (3, 102, 252))
            if self.max_animation_frame < self.curr_frame:
                self.curr_state = MiniGameStates.PLAY
        
        elif self.curr_state == MiniGameStates.PLAY:
            self.draw_squares(scale, self.player_squares, (3, 181, 252), True)
            
            if self.buttons[MiniGameStates.PLAY].is_clicked():
                correct, wrong, missing = self.check_answer()
                self.success = bool(len(correct) == len(self.squares))
                self.verified_answer = correct, wrong, missing
                self.curr_state = MiniGameStates.END
                
        elif self.curr_state == MiniGameStates.END:
            correct, wrong, missing = self.verified_answer
            self.draw_squares(scale, correct, 'green')
            self.draw_squares(scale, wrong, 'red')
            self.draw_squares(scale, missing, 'yellow')
            if self.buttons[MiniGameStates.END].is_clicked():
                self.finish = True