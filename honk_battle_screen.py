import pygame

from game_states import GameStates
from battle_screen import BattleScreen, AGILITY_CONVERSION_RATE
from scripts.utils import load_image
from scripts.fighter_statictics import Stats
from random import randint

BATTLE_IMG_SIZE = 64


class HonkBattleScreen(BattleScreen):
    def __init__(self, display, game_state_manager, animal, backpack, boss, game, first_phase):
        self.game = game
        self.boss = boss
        if first_phase:
            self.boss.img = pygame.transform.scale(load_image("honk/honk_basic.png"), (BATTLE_IMG_SIZE, BATTLE_IMG_SIZE))
        else:
            self.boss.img = pygame.transform.scale(load_image("NPC/Basic/honk.png"), (BATTLE_IMG_SIZE, BATTLE_IMG_SIZE))
        self.first_phase = first_phase
        super().__init__(display, game_state_manager, animal, backpack, background_img = "scenes/honk_battle_background.png")


    def get_rand_enemy(self):
        self.enemy = self.boss
        self.enemy.battle_stats = self.boss.stats.copy()


    def update_manager(self):
        if self.animal.battle_stats[Stats.HEALTH] < 1: # player przegrał z bossem
            super().update_manager()
        elif self.first_phase: # pokonano pierwszy stage bossa
            self.game.states[GameStates.BATTLE] = HonkBattleScreen(self.display, self.game_state_manager, self.animal, self.backpack, self.boss, self.game, False)
            super().update_manager(state=GameStates.BATTLE)
        elif not self.first_phase: # pokonano drugi stage bossa (pokonano bossa)
            super().update_manager(state=GameStates.END)


    def handle_player_buttons(self):
        for name, button in self.player_buttons.items():
            if button.is_clicked():
                if name == "run":
                    if 50 + self.animal.battle_stats[Stats.AGILITY] * AGILITY_CONVERSION_RATE > randint(0, 99):
                        super().update_manager()
                if name == "backpack":
                    self.show_backpack = True
                if name == "minigame" and not self.minigame_used:
                    self.minigame = self.animal.minigame(self.display)
                    self.minigame_used = True
