import pygame
import sys

from time import time
from game_states import GameStates
from scripts.utils import Button, load_image, text_image, load_json
from scripts.enemy import Enemy
from scripts.fighter_statictics import Stats
from random import randint

BUTTON_SIZE = [56*2, 14*2]
FIGHTER_SIZE = [128, 128]


class BattleScreen():
    def __init__(self, display, game_state_manager, animal):
        self.display = display
        self.game_state_manager = game_state_manager
        self.animal = animal
        self.animal.battle_stats = self.animal.stats.copy()
        self.enemy = None
        self.get_rand_enemy()
        self.player_turn = bool(self.animal.stats[Stats.AGILITY] > self.enemy.stats[Stats.AGILITY])

        self.list_of_moves = list(animal.moves.keys())
        self.attack_buttons = {0: Button(display.get_width() // 2 - BUTTON_SIZE[0] -5, self.display.get_height() - 2*BUTTON_SIZE[1] - 10, pygame.transform.scale(load_image(f"buttons/{self.list_of_moves[0]}.png"), (BUTTON_SIZE[0], BUTTON_SIZE[1]))),
                               1: Button(display.get_width() // 2 +5, self.display.get_height() - 2*BUTTON_SIZE[1] - 10, pygame.transform.scale(load_image(f"buttons/{self.list_of_moves[1]}.png"), (BUTTON_SIZE[0], BUTTON_SIZE[1]))),
                               2: Button(display.get_width() // 2 - BUTTON_SIZE[0] -5, self.display.get_height() - BUTTON_SIZE[1] - 5, pygame.transform.scale(load_image(f"buttons/{self.list_of_moves[2]}.png"), (BUTTON_SIZE[0], BUTTON_SIZE[1]))),
                               3: Button(display.get_width() // 2 +5, self.display.get_height() - BUTTON_SIZE[1] - 5, pygame.transform.scale(load_image(f"buttons/{self.list_of_moves[3]}.png"), (BUTTON_SIZE[0], BUTTON_SIZE[1])))}
        
        self.wait_button = Button(display.get_width() // 2 - 110, 130, load_image("buttons/wait.png"))

        self.width_battle = 100
        self.height_battle = 80
        self.border_width_battle = 2
        self.border_offset_battle = 4

        self.cooldown = 0


    def run(self):
        self.display.fill((155, 255, 155))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.update_manager()

        self.render_battle_statistics(self.display, self.animal.battle_stats, 5, 5)
        self.render_battle_statistics(self.display, self.enemy.battle_stats, self.display.get_width() // 2 + 20, 5)

        # self.display.blit(load_image("scenes/battle.png"), (0, 0))
        self.animal.render(self.display, int(self.display.get_width() * 0.05), 40, FIGHTER_SIZE[0], FIGHTER_SIZE[1])
        self.enemy.render(self.display, int(self.display.get_width() * 0.55), 40, FIGHTER_SIZE[0], FIGHTER_SIZE[1])

        if time() > self.cooldown:
            if self.player_turn:
                for button in self.attack_buttons.values():
                    button.render(self.display)

                for num, button in self.attack_buttons.items():
                    if button.is_clicked():
                        player_won = self.animal.perform_attack(self.enemy, self.list_of_moves[num])
                        self.cooldown = time() + 1
                        if player_won:
                            self.animal.xp_gained = self.enemy.lvl
                            self.update_manager()
                            self.enemy = None
                            return
                        else:
                            self.player_turn = not(self.player_turn)
                            break

            else:
                self.wait_button.render(self.display)
                enemy_won = self.enemy.perform_attack(self.animal, list(self.enemy.moves.keys())[randint(0, len(self.enemy.moves.keys())-1)])
                self.cooldown = time() + 1
                if enemy_won:
                    self.animal.xp_gained = -self.enemy.lvl
                    self.update_manager()
                    self.enemy = None
                    return
                else:
                    self.player_turn = not(self.player_turn)
        else:
            self.wait_button.render(self.display)

    def update_manager(self, state=GameStates.MAP):
        self.game_state_manager.set_state(state)


    def get_rand_enemy(self):
        enemies_data = load_json("data/maps/enemies.json")
        rand_enemy_img = list(enemies_data.keys())[randint(0, len(list(enemies_data.keys()))-1)]
        rand_enemy_moves = enemies_data[rand_enemy_img]
        level = randint(self.animal.lvl-1, self.animal.lvl+1)
        if level == 0: level = 1
        health = randint(4*level, 5*level)
        attack = randint(2, 3*level)
        defence = randint(0, 2*level)
        critical_dmg = randint(0, 2)
        agility = randint(0, level)
        luck = randint(0, 2)
        self.enemy = Enemy(rand_enemy_img, health, attack, defence, critical_dmg, agility, luck, rand_enemy_moves, level=level)
        self.enemy.battle_stats = self.enemy.stats.copy()


    def render_battle_statistics(self, surf, stats, x, y):
        background = pygame.Rect(x, y, self.width_battle, self.height_battle)
        # background.center = (surf.get_width() // 2, surf.get_height() // 2)
        pygame.draw.rect(surf, (255, 255, 255), background) 
        pygame.draw.rect(surf, (0, 0, 0),  background, self.border_width_battle)
        curr_y = background.y + self.border_offset_battle
        
        left = background.x + self.border_offset_battle
        
        text_font = pygame.font.Font("data/fonts/Retro.ttf", size=10)
        for stat, val in stats.items():
            stat_text = text_font.render(f"{stat.value}: {val}", True, "black")
            surf.blit(stat_text, (left, curr_y))
            curr_y += 3 + stat_text.get_height()
