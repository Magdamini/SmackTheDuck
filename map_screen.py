import pygame, sys

from battle_screen import BattleScreen
from game_states import GameStates
from scripts.sound_manager import SoundManager
from scripts.utils import load_images, Animation
from scripts.player import Player, PlayerActions
from scripts.camera import Camera
from scripts.battle_detector import Battle_detector
from scripts.map_handler import MapHandler
from scripts.item_collector import ItemCollector
from scripts.level_manager import LevelManager
from scripts.npc import NPCManager, DialogueWindow
from scripts.honk import Boss

class MapScreen:
    def __init__(self, display, game_state_manager, animal, player_type, game):
        self.display = display
        self.sound_manager = SoundManager()
        self.game_state_manager = game_state_manager
        self.game = game

        self.movement = [False, False, False, False]

        self.assets = {
            'Cave': load_images('tiles/Cave'),
            'CaveOutside': load_images('tiles/CaveOutside'),
            'CaveOutside00': load_images('tiles/CaveOutside/00'),
            'CaveOutside01': load_images('tiles/CaveOutside/01'),
            'CaveOutside02': load_images('tiles/CaveOutside/02'),
            'GrassFloor': load_images('tiles/GrassFloor'),
            'GrassGoose': load_images('tiles/GrassGoose'),
            'GrassTrees': load_images('tiles/GrassTrees'),
            'GrassTrees00': load_images('tiles/GrassTrees/00'),
            'GrassTrees01': load_images('tiles/GrassTrees/01'),
            'GrassBuildings': load_images('tiles/GrassBuildings'),
            'GrassBuildings00': load_images('tiles/GrassBuildings/00'),
            'GrassBuildings01': load_images('tiles/GrassBuildings/01'),
            'GrassBuildings02': load_images('tiles/GrassBuildings/02'),
            'GrassBuildings03': load_images('tiles/GrassBuildings/03'),
            'GrassBuildings04': load_images('tiles/GrassBuildings/04'),
            'GrassBushes': load_images('tiles/GrassBushes'),
            'GrassDecor': load_images('tiles/GrassDecor'),
            'GrassDecor00': load_images('tiles/GrassDecor/00'),
            'GrassDecor02': load_images('tiles/GrassDecor/02'),
            'GrassDecor03': load_images('tiles/GrassDecor/03'),
            'GrassIndoorDecor': load_images('tiles/GrassIndoorDecor'),
            'GrassIndoorDecor05': load_images('tiles/GrassIndoorDecor/05'),
            'GrassIndoorDecor06': load_images('tiles/GrassIndoorDecor/06'),
            'GrassIndoorDecor07': load_images('tiles/GrassIndoorDecor/07'),
            'GrassIndoorDecor08': load_images('tiles/GrassIndoorDecor/08'),
            'WaterFloor': load_images('tiles/WaterFloor'),
            'WaterCatwalk': load_images('tiles/WaterCatwalk'),
            'HouseFloor': load_images('tiles/HouseFloor'),
            'HouseIndoor': load_images('tiles/HouseIndoor'),
            'HouseIndoor00': load_images('tiles/HouseIndoor/00'),
            'HouseIndoor01': load_images('tiles/HouseIndoor/01'),
            'Items': load_images('tiles/Items'),
            
            'player/' + PlayerActions.STANDING.value: Animation(load_images(f'player/{player_type}/' + PlayerActions.STANDING.value)),
            'player/' + PlayerActions.UP.value: Animation(load_images(f'player/{player_type}/' + PlayerActions.UP.value)),
            'player/' + PlayerActions.DOWN.value: Animation(load_images(f'player/{player_type}/' + PlayerActions.DOWN.value)),
            'player/' + PlayerActions.RIGHT.value: Animation(load_images(f'player/{player_type}/' + PlayerActions.RIGHT.value)),
            'player/' + PlayerActions.LEFT.value: Animation(load_images(f'player/{player_type}/' + PlayerActions.LEFT.value))
        }
        
        self.player = Player(self, (150, 150), (16, 16))
        self.animal = animal
        
        self.map_handler = MapHandler(self, self.player)
        self.tilemap = self.map_handler.get_curr_map()
        
        self.camera = Camera(self.display, self.player, self.tilemap)
        self.item_collector = ItemCollector(self.player, self.map_handler.maps)
        self.level_manager = LevelManager(self.animal, self.item_collector)
        
        self.npc_manager = NPCManager("data/npc/npc_data.txt", self.map_handler)
        self.boss = Boss(self.map_handler.maps['5a'])

        self.battle_detector = Battle_detector(self.game_state_manager, self.player, self.tilemap)

        self.show_backpack = False
        self.show_animal_stats = False
        self.new_level_window = None
        self.dialogue_window = None

        self.had_battle = False

        # self.sound_manager.play_music("game")


    def run(self):
        # update player pos
        if not self.is_player_paused():
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
            self.map_handler.change_map(self.level_manager.level)
            self.camera.update()
        
        self.item_collector.collect_items(self.tilemap)
        
        # battle
        xp = 0
        if self.had_battle:
            xp = self.animal.xp_gained
            self.animal.xp_gained = 0
            self.had_battle = False

        if self.handle_battle():
            self.had_battle = True
        
        # update xp
        new_lvl = self.level_manager.update(xp, self.map_handler.maps)
        if new_lvl is not None:
            self.npc_manager.activate_npc(new_lvl.new_level)
            self.new_level_window = new_lvl


        # render
        self.display.fill((self.tilemap.tilemap["background_color"]["R"], self.tilemap.tilemap["background_color"]["G"], self.tilemap.tilemap["background_color"]["B"]))  

        self.tilemap.render(self.display, self.camera.pos)
        if self.map_handler.curr_map == "5a":
            self.boss.render_on_map(self.display, self.player, self.camera.pos)
        self.player.render(self.display, self.camera.pos)
        self.level_manager.render(self.display)
        
        
        
        # check npc
        npc = self.npc_manager.talk_with_npc(self.display, self.camera.pos, self.player, self.map_handler.curr_map)

        self.render_extra_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.movement[0] = True
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.movement[1] = True
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.movement[2] = True
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.movement[3] = True
                if event.key == pygame.K_LSHIFT:
                    self.player.running = True

                if event.key == pygame.K_b:
                    if not self.show_backpack and not self.is_player_paused():
                        self.show_backpack = True
                    elif self.show_backpack:
                        self.show_backpack = False
                        
                if event.key == pygame.K_v:
                    if not self.show_animal_stats and not self.is_player_paused():
                        self.show_animal_stats = True
                    elif self.show_animal_stats:
                        self.show_animal_stats = False
                        
                if event.key == pygame.K_t:
                    if self.dialogue_window is None and not self.is_player_paused() and npc is not None:
                        self.dialogue_window = DialogueWindow(npc, self.player.backpack, self.animal)
                 
                # TODO walka z bossem       
                if event.key == pygame.K_f:
                    if not self.is_player_paused() and self.boss.touch_player:
                        print("walka z bossem")
                        
                if event.key == pygame.K_q:
                    self.show_backpack = False
                    self.show_animal_stats = False
                    self.active_npc = None
                    
                if event.key == pygame.K_x:
                    if not self.is_player_paused():
                        xp = 5 * self.level_manager.level
                        print(f"+{xp} Xp")
                        new_lvl = self.level_manager.update(xp, self.map_handler.maps)
                        if new_lvl is not None:
                            self.npc_manager.activate_npc(new_lvl.new_level)
                            self.new_level_window = new_lvl
                
                if event.key == pygame.K_ESCAPE:
                    self.game_state_manager.set_state(GameStates.END)
                
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.movement[0] = False
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.movement[1] = False
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.movement[2] = False
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.movement[3] = False
                if event.key == pygame.K_LSHIFT:
                    self.player.running = False
        
    
    def render_extra_window(self):
        if self.new_level_window is not None:
            self.new_level_window.render(self.display, self.game_state_manager.scale)
            if self.new_level_window.is_finished():
                self.new_level_window = None
                
        elif self.show_backpack:
            self.player.backpack.render(self.display, self.game_state_manager.scale, True)
            
            # TODO - do usunięcia -> możesz zobaczyć jak działa branie przedmiotów
            # self.player.backpack.get_clicked_item(self.display, self.game_state_manager.scale)
            
        elif self.show_animal_stats:
            self.animal.render_statistics(self.display)
            
        if self.dialogue_window is not None:
            self.dialogue_window.render_dialogue(self.display, self.game_state_manager.scale)
            if self.dialogue_window.dialogue_end():
                self.dialogue_window = None


    def is_player_paused(self):
        return self.show_backpack or self.show_animal_stats or self.new_level_window is not None or self.dialogue_window is not None


    def handle_battle(self):
        if self.battle_detector.detect_battle():
            # self.sound_manager.stop_music()
            self.game.states[GameStates.BATTLE] = BattleScreen(self.display, self.game_state_manager, self.animal, self.player.backpack)
            self.battle_detector.update_manager()
            self.movement = [False, False, False, False]
            return True
        return False
