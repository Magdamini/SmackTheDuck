import pygame
import sys

from time import time
from game_states import GameStates
from scripts.utils import Button, load_image, text_image, load_json
from scripts.sound_manager import SoundManager
from scripts.enemy import Enemy
from scripts.fighter_statictics import Stats
from random import randint

ATTACK_BUTTON_SIZE = [56*2, 14*2]
SMALL_BUTTON_SIZE = [28, 28]
FIGHTER_SIZE = [128, 128]


class BattleScreen():
    def __init__(self, display, game_state_manager, animal, backpack):
        self.display = display
        self.sound_manager = SoundManager()
        self.game_state_manager = game_state_manager
        self.animal = animal
        self.animal.battle_stats = self.animal.stats.copy()

        self.backpack = backpack
        self.show_backpack = False

        self.enemy = None
        self.get_rand_enemy()
        self.player_turn = bool(self.animal.stats[Stats.AGILITY] > self.enemy.stats[Stats.AGILITY])

        self.list_of_moves = list(animal.moves.keys())
        self.attack_buttons = {0: Button(10, self.display.get_height() - 2*ATTACK_BUTTON_SIZE[1] - 10, pygame.transform.scale(load_image(f"buttons/{self.list_of_moves[0]}.png"), (ATTACK_BUTTON_SIZE[0], ATTACK_BUTTON_SIZE[1]))),
                               1: Button(10 + ATTACK_BUTTON_SIZE[0] + 5, self.display.get_height() - 2*ATTACK_BUTTON_SIZE[1] - 10, pygame.transform.scale(load_image(f"buttons/{self.list_of_moves[1]}.png"), (ATTACK_BUTTON_SIZE[0], ATTACK_BUTTON_SIZE[1]))),
                               2: Button(10, self.display.get_height() - ATTACK_BUTTON_SIZE[1] - 5, pygame.transform.scale(load_image(f"buttons/{self.list_of_moves[2]}.png"), (ATTACK_BUTTON_SIZE[0], ATTACK_BUTTON_SIZE[1]))),
                               3: Button(10 + ATTACK_BUTTON_SIZE[0] + 5, self.display.get_height() - ATTACK_BUTTON_SIZE[1] - 5, pygame.transform.scale(load_image(f"buttons/{self.list_of_moves[3]}.png"), (ATTACK_BUTTON_SIZE[0], ATTACK_BUTTON_SIZE[1])))}
        
        self.player_buttons = {"info": Button(25 + 2*ATTACK_BUTTON_SIZE[0], self.display.get_height() - 2*ATTACK_BUTTON_SIZE[1] - 10, pygame.transform.scale(load_image(f"buttons/info.png"), (SMALL_BUTTON_SIZE[0], SMALL_BUTTON_SIZE[1]))),
                               "backpack": Button(25 + 2*ATTACK_BUTTON_SIZE[0] + 5 + SMALL_BUTTON_SIZE[0], self.display.get_height() - 2*ATTACK_BUTTON_SIZE[1] - 10, pygame.transform.scale(load_image(f"buttons/backpack.png"), (SMALL_BUTTON_SIZE[0], SMALL_BUTTON_SIZE[1]))),
                               "run": Button(25 + 2*ATTACK_BUTTON_SIZE[0], self.display.get_height() - ATTACK_BUTTON_SIZE[1] - 5, pygame.transform.scale(load_image(f"buttons/run.png"), (2*SMALL_BUTTON_SIZE[0] + 5, SMALL_BUTTON_SIZE[1])))}

        self.wait_button = Button(display.get_width() // 2 - 110, 130, load_image("buttons/wait.png"))

        self.width_battle = 100
        self.height_battle = 80
        self.border_width_battle = 2
        self.border_offset_battle = 4

        self.cooldown = time() + 1

        self.sound_manager.play_music("battle")


    def run(self):
        self.display.fill((155, 255, 155))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.show_backpack = False

        self.render_battle_statistics(self.display, self.animal.battle_stats, 5, 5)
        self.render_battle_statistics(self.display, self.enemy.battle_stats, self.display.get_width() // 2 + 20, 5)

        # self.display.blit(load_image("scenes/battle.png"), (0, 0))
        self.animal.render(self.display, int(self.display.get_width() * 0.05), 40, FIGHTER_SIZE[0], FIGHTER_SIZE[1])
        self.enemy.render(self.display, int(self.display.get_width() * 0.55), 40, FIGHTER_SIZE[0], FIGHTER_SIZE[1])

        if time() > self.cooldown:
            if self.player_turn:
                for button in self.attack_buttons.values():
                    button.render(self.display)

                for button in self.player_buttons.values():
                    button.render(self.display)

                self.render_extra_window()

                if not self.is_player_paused():
                    self.handle_attack_buttons()
                    self.handle_player_buttons()

            else:
                self.wait_button.render(self.display)
                if self.animal.battle_stats[Stats.LUCK] * 5 > randint(0, 99):
                    print("Player's luck")
                    player_won = self.enemy.perform_attack(self.enemy, list(self.enemy.moves.keys())[randint(0, len(self.enemy.moves.keys())-1)])
                    self.cooldown = time() + 1
                    if player_won:
                        self.animal.xp_gained = self.enemy.lvl
                        self.update_manager()
                        self.enemy = None
                        print("Player won")
                        return
                    else:
                        self.player_turn = not(self.player_turn)
                else:
                    enemy_won = self.enemy.perform_attack(self.animal, list(self.enemy.moves.keys())[randint(0, len(self.enemy.moves.keys())-1)])
                    self.cooldown = time() + 1
                    if enemy_won:
                        self.animal.xp_gained = -self.enemy.lvl
                        self.update_manager()
                        self.enemy = None
                        print("Enemy won")
                        return
                    else:
                        self.player_turn = not(self.player_turn)
        else:
            self.wait_button.render(self.display)

    
    def handle_attack_buttons(self):
        for num, button in self.attack_buttons.items():
            if button.is_clicked():
                if self.enemy.battle_stats[Stats.LUCK] * 5 > randint(0, 99):
                    print("Enemy's luck")
                    enemy_won = self.animal.perform_attack(self.animal, self.list_of_moves[num])
                    self.cooldown = time() + 1
                    if enemy_won:
                        self.animal.xp_gained = -self.enemy.lvl
                        self.update_manager()
                        self.enemy = None
                        print("Enemy won")
                        return
                    else:
                        self.player_turn = not(self.player_turn)
                else:
                    player_won = self.animal.perform_attack(self.enemy, self.list_of_moves[num])
                    self.cooldown = time() + 1
                    if player_won:
                        self.animal.xp_gained = self.enemy.lvl
                        self.update_manager()
                        self.enemy = None
                        print("Player won")
                        return
                    else:
                        self.player_turn = not(self.player_turn)
                        break
    

    def handle_player_buttons(self):
        for name, button in self.player_buttons.items():
            if button.is_clicked():
                if name == "run":
                    self.update_manager()
                if name == "backpack":
                    self.show_backpack = True
                

    def render_extra_window(self):
        if self.show_backpack:
            self.backpack.render(self.display, self.game_state_manager.scale)
            
            # What does this do? TODO
            # self.player.backpack.get_clicked_item(self.display, self.game_state_manager.scale)
            

    def is_player_paused(self):
        return self.show_backpack


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


    def update_manager(self, state=GameStates.MAP):
        self.sound_manager.stop_music()
        self.sound_manager.play_music("game")
        self.game_state_manager.set_state(state)
