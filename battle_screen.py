import pygame
import sys

from time import sleep
from game_states import GameStates
from scripts.utils import Button, load_image, text_image, load_json
from scripts.enemy import Enemy
from scripts.fighter_statictics import Stats
from random import randint

BUTTON_SIZE = [100, 50]


class BattleScreen():
    def __init__(self, display, game_state_manager, animal):
        self.display = display
        self.game_state_manager = game_state_manager
        self.animal = animal
        self.enemy = None

        self.get_rand_enemy()

        self.player_turn = bool(self.animal.stats[Stats.AGILITY] > self.enemy.stats[Stats.AGILITY])

        self.attack_buttons = {"move_1": Button(display.get_width() // 2 - BUTTON_SIZE[0] -5, 120, load_image("buttons/move_1.png")), #text_image("move 1", 10)),
                               "move_2": Button(display.get_width() // 2 +5, 120, load_image("buttons/move_2.png")), #text_image("move 2", 10)),
                               "move_3": Button(display.get_width() // 2 - BUTTON_SIZE[0] -5, 180, load_image("buttons/move_3.png")), #text_image("move 3", 10)),
                               "move_4": Button(display.get_width() // 2 +5, 180, load_image("buttons/move_4.png"))} #text_image("move 4", 10))}
        
        self.wait_button = Button(display.get_width() // 2 - BUTTON_SIZE[0] -5, 120, load_image("buttons/wait.png"))
                        

    def run(self):
        self.display.fill((155, 255, 155))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.update_manager()

        # self.display.blit(load_image("scenes/battle.png"), (0, 0))
        self.animal.render(self.display, int(self.display.get_width() * 0.2), 20)
        self.enemy.render(self.display, int(self.display.get_width() * 0.6), 20)

        if self.player_turn:
            for button in self.attack_buttons.values():
                button.render(self.display)

            for name, button in self.attack_buttons.items():
                if button.is_clicked():
                    player_won = self.animal.perform_attack(self.enemy, name)
                    if player_won:
                        sleep(2)
                        self.update_manager()
                        return
                    sleep(2)
        else:
            self.wait_button.render(self.display)
            enemy_won = self.enemy.perform_attack(self.animal, list(self.enemy.moves.keys())[randint(0, len(self.enemy.moves.keys())-1)])
            if enemy_won:
                sleep(2)
                self.update_manager()


    def update_manager(self, state=GameStates.MAP):
        self.game_state_manager.set_state(state)


    def get_rand_enemy(self):
        enemies_data = load_json("data/maps/enemies.json")
        rand_enemy_name = list(enemies_data.keys())[randint(0, len(enemies_data.keys())-1)]
        rand_enemy_moves = enemies_data[rand_enemy_name]
        self.enemy = Enemy('enemies/Gadwall.png', rand_enemy_name, 1, 1, 1, 1, 1, 1, rand_enemy_moves, level=1)
