from scripts.minigame import MiniGameStates, MiniGame
from scripts.utils import text_image
from random import randint
from time import time
import pygame

ROUND_TIME = 0.5

class MinigameSchoot(MiniGame):
    def __init__(self, surf):
        name = "MINIGAME"
        desc = "Click on the blue squares when they appear"
        super().__init__(desc, name, surf)

        self.square_size = 24
        self.rows = 5
        self.cols = 8
        self.right_offset = 80
        
        self.squares = []
        self.player_squares = []
        self.rand_squares(3)
        
        self.round_num = 0
        self.rounds = 3
        self.won_rounds = 0
        self.last_click = True

        self.cooldown = time()     # jak długo ma się wyświetlać wzór
        self.check_cooldown = time()
        self.do_we_check = False

        # self.buttons[MiniGameStates.WAIT] = self.buttons[MiniGameStates.PLAY]
        
    
    def rand_squares(self, n=10):
        cnt = 0
        while cnt < n:
            row = randint(0, self.rows - 1)
            col = randint(0, self.cols - 1)
            if (row, col) not in self.squares:
                self.squares.append((row, col))
                cnt += 1
                
                
    def check_answer(self, round_num):
        correct, wrong, missing = [], [], []
        if not self.player_squares:
            missing.append(self.squares[round_num])
        elif self.squares[round_num] == self.player_squares[0]:
            correct.append(self.squares[round_num])
        elif self.squares[round_num] != self.player_squares[0]:
            wrong.append(self.player_squares[0])
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
                            self.player_squares.append((row, col))
                    else:
                        self.last_click = False
        
        pygame.draw.rect(self.surf, (0, 0, 0), sq_background, self.border_width)
        
        
    def render_game(self, scale):
        curr_button = self.buttons.get(self.curr_state)
        if curr_button is not None:
            curr_button.render(self.surf, scale)
        
        if self.curr_state == MiniGameStates.START:
            self.draw_squares(scale, [])
            if self.buttons[MiniGameStates.START].is_clicked():
                self.cooldown = time() + 1
                self.curr_state = MiniGameStates.WAIT


        elif self.curr_state == MiniGameStates.WAIT:
            self.draw_squares(scale, [])
            if self.round_num > self.rounds - 1: # koniec minigry
                self.success = bool(self.won_rounds == self.rounds)
                self.curr_state = MiniGameStates.END
            if self.cooldown < time():
                self.cooldown = time() + ROUND_TIME
                self.curr_state = MiniGameStates.PLAY


        elif self.curr_state == MiniGameStates.PLAY:
            if not self.player_squares and self.cooldown >= time(): # runda trwa
                self.draw_squares(scale, [self.squares[self.round_num]], (3, 102, 252), True)
            else: # runda skończona
                if not self.do_we_check:
                    self.check_cooldown = time() + 1
                    self.do_we_check = True
                correct, wrong, missing = self.check_answer(self.round_num)
                self.draw_squares(scale, correct, 'green')
                self.draw_squares(scale, wrong, 'red')
                self.draw_squares(scale, missing, 'yellow')

                if self.check_cooldown < time(): # pora na rundę (koniec sprawdzania)
                    if self.player_squares and self.squares[self.round_num] == self.player_squares[0]:
                        self.won_rounds += 1
                    self.do_we_check = False
                    self.player_squares = []
                    self.cooldown = time() + ROUND_TIME
                    self.round_num += 1

            if self.round_num > self.rounds - 1: # koniec minigry
                self.success = bool(self.won_rounds == self.rounds)
                self.curr_state = MiniGameStates.END


        elif self.curr_state == MiniGameStates.END:
            won_rounds_txt = text_image(f"{self.won_rounds}/{self.rounds}", 90, "data/fonts/Retro.ttf")
            self.surf.blit(won_rounds_txt, (self.surf.get_width() // 12, self.surf.get_height() - 150))
            if self.buttons[MiniGameStates.END].is_clicked():
                self.finish = True
