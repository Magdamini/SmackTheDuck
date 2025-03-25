import pygame
import sys

from time import time
from game_states import GameStates
from scripts.utils import Button, load_image, text_image, load_json
from scripts.sound_manager import SoundManager
from scripts.enemy import Enemy
from scripts.animal import Animal
from scripts.fighter_statictics import Stats
from scripts.items import Stones
from random import randint, sample

# from scripts.minigame_squares import MinigameSquares
# from scripts.minigame_shoot import MinigameShoot

ATTACK_BUTTON_SIZE = [56 * 2, 14 * 2]
SMALL_BUTTON_SIZE = [28, 28]
FIGHTER_SIZE = [128, 128]
LUCK_CONVERSION_RATE = 2.5
AGILITY_CONVERSION_RATE = 5
BASIC_CHANCE_TO_RUN_AWAY = 33


class BattleScreen:
    def __init__(
        self,
        display,
        game_state_manager,
        animal,
        backpack,
        background_img="scenes/battle_background.png",
    ):
        self.display = display
        self.sound_manager = SoundManager()
        self.game_state_manager = game_state_manager
        self.animal = animal
        self.animal.battle_stats = self.animal.stats.copy()
        self.background_img = background_img

        self.backpack = backpack
        self.show_backpack = False

        self.minigame = None
        self.minigame_used = False
        self.minigame_success = False

        self.enemy = None
        self.get_rand_enemy()
        self.player_turn = bool(
            self.animal.stats[Stats.AGILITY] > self.enemy.stats[Stats.AGILITY]
        )

        self.list_of_moves = list(animal.moves.keys())
        self.attack_buttons = {
            0: Button(
                10,
                self.display.get_height() - 2 * ATTACK_BUTTON_SIZE[1] - 10,
                pygame.transform.scale(
                    load_image(f"buttons/{self.list_of_moves[0]}.png"),
                    (ATTACK_BUTTON_SIZE[0], ATTACK_BUTTON_SIZE[1]),
                ),
            ),
            1: Button(
                10 + ATTACK_BUTTON_SIZE[0] + 5,
                self.display.get_height() - 2 * ATTACK_BUTTON_SIZE[1] - 10,
                pygame.transform.scale(
                    load_image(f"buttons/{self.list_of_moves[1]}.png"),
                    (ATTACK_BUTTON_SIZE[0], ATTACK_BUTTON_SIZE[1]),
                ),
            ),
            2: Button(
                10,
                self.display.get_height() - ATTACK_BUTTON_SIZE[1] - 5,
                pygame.transform.scale(
                    load_image(f"buttons/{self.list_of_moves[2]}.png"),
                    (ATTACK_BUTTON_SIZE[0], ATTACK_BUTTON_SIZE[1]),
                ),
            ),
            3: Button(
                10 + ATTACK_BUTTON_SIZE[0] + 5,
                self.display.get_height() - ATTACK_BUTTON_SIZE[1] - 5,
                pygame.transform.scale(
                    load_image(f"buttons/{self.list_of_moves[3]}.png"),
                    (ATTACK_BUTTON_SIZE[0], ATTACK_BUTTON_SIZE[1]),
                ),
            ),
        }

        self.player_buttons = {
            "minigame": Button(
                25 + 2 * ATTACK_BUTTON_SIZE[0],
                self.display.get_height() - 2 * ATTACK_BUTTON_SIZE[1] - 10,
                pygame.transform.scale(
                    load_image(f"buttons/minigame.png"),
                    (SMALL_BUTTON_SIZE[0], SMALL_BUTTON_SIZE[1]),
                ),
            ),
            "backpack": Button(
                25 + 2 * ATTACK_BUTTON_SIZE[0] + 5 + SMALL_BUTTON_SIZE[0],
                self.display.get_height() - 2 * ATTACK_BUTTON_SIZE[1] - 10,
                pygame.transform.scale(
                    load_image(f"buttons/backpack.png"),
                    (SMALL_BUTTON_SIZE[0], SMALL_BUTTON_SIZE[1]),
                ),
            ),
            "run": Button(
                25 + 2 * ATTACK_BUTTON_SIZE[0],
                self.display.get_height() - ATTACK_BUTTON_SIZE[1] - 5,
                pygame.transform.scale(
                    load_image(f"buttons/run.png"),
                    (2 * SMALL_BUTTON_SIZE[0] + 5, SMALL_BUTTON_SIZE[1]),
                ),
            ),
        }

        self.show_more_buttons = {
            "show_more_animal": Button(
                123,
                5,
                pygame.transform.scale(load_image(f"buttons/show_more.png"), (20, 38)),
            ),
            "show_more_enemy": Button(
                self.display.get_width() // 2 + 138,
                5,
                pygame.transform.scale(load_image(f"buttons/show_more.png"), (20, 38)),
            ),
        }
        self.show_more_info_is_clicked = False

        self.info_message = {
            "enemy_turn": load_image("messages/enemy_turn.png"),
            "player_won": load_image("messages/player_won.png"),
            "enemy_won": load_image("messages/enemy_won.png"),
            "player_got_lucky": load_image("messages/player_got_lucky.png"),
            "enemy_got_lucky": load_image("messages/enemy_got_lucky.png"),
            "fight": load_image("messages/fight.png"),
            "running_away_failed": load_image("messages/running_away_failed.png"),
        }
        self.printed_message = self.info_message["fight"]

        self.cooldown = time() + 1
        self.fainted = False
        self.rotate_angl = 0  # TODO delete in the future if Magda won't like the fainted animation xdddd
        self.dmg_text = None
        self.dmg_text_cooldown = time()
        self.player_got_dmg_delt = True

        # self.sound_manager.play_music("battle")

    def run(self):
        self.display.fill((155, 255, 155))
        self.display.blit(load_image(self.background_img), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.show_backpack = False

        self.animal.render_battle_statistics(self.display, 5, 5)
        self.enemy.render_battle_statistics(
            self.display, self.display.get_width() // 2 + 20, 5
        )

        if self.animal.battle_stats[Stats.HEALTH] > 0:
            self.animal.render(
                self.display,
                int(self.display.get_width() * 0.05),
                40,
                FIGHTER_SIZE[0],
                FIGHTER_SIZE[1],
            )
        if self.enemy.battle_stats[Stats.HEALTH] > 0:
            self.enemy.render(
                self.display,
                int(self.display.get_width() * 0.55),
                40,
                FIGHTER_SIZE[0],
                FIGHTER_SIZE[1],
            )

        for button in self.show_more_buttons.values():
            button.render(self.display)
        if not self.is_player_paused():
            self.show_more_info_is_clicked = self.handle_show_more_buttons()

        if time() > self.cooldown:
            if self.fainted:  # battle ended
                self.update_manager()
                self.enemy = None
                return

            if self.player_turn:
                for button in self.attack_buttons.values():
                    button.render(self.display)

                for button in self.player_buttons.values():
                    button.render(self.display)

                self.render_extra_window()

                if self.show_more_info_is_clicked:
                    return

                if not self.is_player_paused():
                    self.handle_player_buttons()
                    self.handle_attack_buttons()

            else:  # enemy's turn
                self.printed_message = self.info_message["enemy_turn"]
                self.display.blit(
                    self.printed_message,
                    (10, self.display.get_height() - 2 * ATTACK_BUTTON_SIZE[1] - 10),
                )
                if self.animal.battle_stats[
                    Stats.LUCK
                ] * LUCK_CONVERSION_RATE > randint(
                    0, 99
                ):  # enemy will hit himself due to player's luck
                    print("Player's luck")
                    self.dmg_text = self.enemy.perform_attack(
                        self.enemy,
                        list(self.enemy.moves.keys())[
                            randint(0, len(self.enemy.moves.keys()) - 1)
                        ],
                    )
                    self.player_got_dmg_delt = False
                    self.do_cooldown()
                    if self.enemy.battle_stats[Stats.HEALTH] < 1:  # player won
                        self.player_won()
                    else:
                        self.player_turn = not (self.player_turn)
                else:
                    self.dmg_text = self.enemy.perform_attack(
                        self.animal,
                        list(self.enemy.moves.keys())[
                            randint(0, len(self.enemy.moves.keys()) - 1)
                        ],
                    )
                    self.player_got_dmg_delt = True
                    self.do_cooldown()
                    if self.animal.battle_stats[Stats.HEALTH] < 1:  # enemy won
                        self.enemy_won()
                    else:
                        self.player_turn = not (self.player_turn)
        else:  # wait while cooldown
            self.display.blit(
                self.printed_message,
                (10, self.display.get_height() - 2 * ATTACK_BUTTON_SIZE[1] - 10),
            )
            if self.fainted:
                self.sb_fainted()

        if time() < self.dmg_text_cooldown:  # showing dmg delt to sb
            if self.player_got_dmg_delt:
                self.display.blit(
                    self.dmg_text, (int(self.display.get_width() * 0.25), 80)
                )
            else:
                self.display.blit(
                    self.dmg_text, (int(self.display.get_width() * 0.75), 80)
                )

    def handle_attack_buttons(self):
        for num, button in self.attack_buttons.items():
            if button.is_clicked() and time() > self.cooldown:
                if self.enemy.battle_stats[Stats.LUCK] * LUCK_CONVERSION_RATE > randint(
                    0, 99
                ):  # animal will hit himself due to enemy's luck
                    print("Enemy's luck")
                    self.dmg_text = self.animal.perform_attack(
                        self.animal, self.list_of_moves[num]
                    )
                    self.player_got_dmg_delt = True
                    self.do_cooldown()
                    self.printed_message = self.info_message["enemy_turn"]
                    if self.animal.battle_stats[Stats.HEALTH] < 1:  # enemy won
                        self.enemy_won()
                    else:
                        self.player_turn = not (self.player_turn)
                else:
                    self.dmg_text = self.animal.perform_attack(
                        self.enemy, self.list_of_moves[num], self.minigame_success
                    )
                    self.minigame_success = False
                    self.player_got_dmg_delt = False
                    self.do_cooldown()
                    self.printed_message = self.info_message["enemy_turn"]
                    if self.enemy.battle_stats[Stats.HEALTH] < 1:  # player won
                        self.player_won()
                    else:
                        self.player_turn = not (self.player_turn)
                return

    def handle_player_buttons(self):
        for name, button in self.player_buttons.items():
            if button.is_clicked():
                if name == "run":
                    if BASIC_CHANCE_TO_RUN_AWAY + self.animal.battle_stats[
                        Stats.AGILITY
                    ] * AGILITY_CONVERSION_RATE > randint(0, 99):
                        self.update_manager()
                    else:
                        self.printed_message = self.info_message["running_away_failed"]
                        print("Running away failed")
                        self.cooldown = time() + 1
                        self.player_turn = not (self.player_turn)
                if name == "backpack":
                    self.show_backpack = True
                if name == "minigame" and not self.minigame_used:
                    self.minigame = self.animal.minigame(self.display)
                    self.minigame_used = True

    def handle_show_more_buttons(self):
        for name, button in self.show_more_buttons.items():
            if button.is_clicked():
                if name == "show_more_animal":
                    self.animal.render_other_battle_statistics(self.display, 5, 5)
                if name == "show_more_enemy":
                    self.enemy.render_other_battle_statistics(
                        self.display, self.display.get_width() // 2 + 20, 5
                    )
                return True
        return False

    def player_won(self):
        self.animal.xp_gained = self.enemy.lvl
        self.printed_message = self.info_message["player_won"]
        self.fainted = True
        print("Player won")

    def enemy_won(self):
        self.animal.xp_gained = -self.enemy.lvl
        self.printed_message = self.info_message["enemy_won"]
        self.fainted = True
        print("Enemy won")

    def sb_fainted(self):
        self.rotate_angl += 10
        if self.animal.battle_stats[Stats.HEALTH] < 1:
            self.display.blit(
                pygame.transform.rotate(self.animal.img, self.rotate_angl),
                (int(self.display.get_width() * 0.05), 40),
            )
        elif self.enemy.battle_stats[Stats.HEALTH] < 1:
            self.display.blit(
                pygame.transform.rotate(self.enemy.img, self.rotate_angl),
                (int(self.display.get_width() * 0.55), 40),
            )

    def render_extra_window(self):
        if self.show_backpack:
            item_clicked = self.backpack.render(
                self.display, self.game_state_manager.scale, get_item=True
            )
            if item_clicked:
                print(item_clicked)
                if isinstance(item_clicked, Stones):
                    item_clicked.use(self.enemy)
                else:
                    item_clicked.use(self.animal)

        # do testowania minigierki
        elif self.minigame is not None:
            self.minigame.render(self.game_state_manager.scale)
            finished, success = self.minigame.is_finished()
            if finished:
                self.player_buttons["run"].changed = (
                    False  # niefortunnie ostatnim zdarzeniem jest kliknięcie tuż nad run i liczy to jako run XD
                )
                self.player_buttons["backpack"].changed = False
                self.minigame = None
                self.minigame_success = success

    def do_cooldown(self):
        self.dmg_text_cooldown = time() + 0.5
        self.cooldown = time() + 1

    def is_player_paused(self):
        return self.show_backpack or self.minigame is not None

    def get_rand_enemy(self):
        enemies_data = load_json("data/maps/enemies.json")
        rand_enemy_img = list(enemies_data.keys())[
            randint(0, len(list(enemies_data.keys())) - 1)
        ]
        rand_enemy_moves = enemies_data[rand_enemy_img]
        level = randint(self.animal.lvl - 1, self.animal.lvl + 1)
        if level == 0:
            level = 1

        health = randint(4 * level + 5, 5 * level + 5)
        attack = (
            randint(3 * level - 5, 4 * level - 5)
            if level > 2
            else randint(2, 4) if level > 1 else randint(1, 2)
        )
        defence = randint(1 * level, 3 * level) if level > 1 else randint(1, 2)

        extra_stats_sum = 2 * level - 2 if level > 5 else level + 2
        extra_stats = (
            [0] + sorted(sample(range(0, extra_stats_sum + 1), 2)) + [extra_stats_sum]
        )
        critical_dmg = extra_stats[1] - extra_stats[0]
        agility = extra_stats[2] - extra_stats[1]
        luck = extra_stats[3] - extra_stats[2]

        self.enemy = Enemy(
            rand_enemy_img,
            health,
            attack,
            defence,
            critical_dmg,
            agility,
            luck,
            rand_enemy_moves,
            level=level,
        )
        self.enemy.battle_stats = self.enemy.stats.copy()

    def update_manager(self, state=GameStates.MAP):
        # self.sound_manager.stop_music()
        # self.sound_manager.play_music("game")
        self.game_state_manager.set_state(state)


# Pomysł: Gdy player ma big_critical_dmg (z minigierki) zmienia się jego wygląd na taki szybki i niebezpieczny >:))
