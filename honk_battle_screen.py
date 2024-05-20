import pygame
import sys

from time import time
from game_states import GameStates
from battle_screen import BattleScreen
from scripts.utils import Button, load_image, text_image, load_json
from scripts.sound_manager import SoundManager
from scripts.enemy import Enemy
from scripts.animal import Animal
from scripts.fighter_statictics import Stats
from scripts.items import Stones
from scripts.honk import Boss
from random import randint


class HonkBattleScreen(BattleScreen):
    def __init__(self, display, game_state_manager, animal, backpack, boss):
        self.boss = boss
        super().__init__(display, game_state_manager, animal, backpack)


    def get_rand_enemy(self):
        self.enemy = self.boss
        self.enemy.battle_stats = self.boss.stats.copy()
