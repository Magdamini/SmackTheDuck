import pygame,sys

from scripts.utils import load_images, Animation
from scripts.player import Player, PlayerActions
from scripts.camera import Camera
from scripts.battle_detector import Battle_detector
from scripts.fighter import FightingPlayer
from scripts.map_handler import MapHandler
from scripts.item_collector import ItemCollector
from scripts.level_manager import LevelManager

class MapScreen:
    def __init__(self, display, game_state_manager, animal, player_type):
        self.display = display
        self.game_state_manager = game_state_manager        

        self.movement = [False, False, False, False]
        self.show_items = []

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

        self.fighting_player = FightingPlayer(["Ogłuszacz", "Lowkick", "Rzut ala precel", "Kijem między oczy"], 3)
        self.battle_detector = Battle_detector(self.player, self.fighting_player, self.tilemap)


    def run(self):
        # update player pos
        if not self.show_items:
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
            self.map_handler.change_map()
            self.camera.update()
        
        # battle
        self.item_collector.collect_items(self.tilemap)
        self.battle_detector.detect_battle()
        # xp = battle_result
        xp = 0
        
        # update xp
        new_lvl_window = self.level_manager.update(xp)
        if new_lvl_window is not None:
            self.show_items.append(new_lvl_window)
            
        
        # render
        self.display.fill((self.tilemap.tilemap["background_color"]["R"], self.tilemap.tilemap["background_color"]["G"], self.tilemap.tilemap["background_color"]["B"]))  

        
        self.tilemap.render(self.display, self.camera.pos)
        self.player.render(self.display, self.camera.pos)
        self.level_manager.render(self.display)
        
        
        for item in self.show_items:
            item.render(self.display)
            if item != self.player.backpack:
                if item.is_finished():
                    self.show_items.remove(item)
            
            # TODO - do usunięcia -> możesz zobaczyć jak działa branie przedmiotów
            if item == self.player.backpack:
                item.get_clicked_item(self.display, self.game_state_manager.scale)

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
                    if self.player.backpack in self.show_items:
                        self.show_items.remove(self.player.backpack)
                    else:
                        self.show_items.append(self.player.backpack)
                        
                if event.key == pygame.K_q:
                    self.show_items = []
                    self.item_collector.new_random_items(3)
                    
                if event.key == pygame.K_x:
                    print("+1 Xp")
                    new_lvl_window = self.level_manager.update(1)
                    if new_lvl_window is not None:
                        self.show_items.append(new_lvl_window)
                
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
                    

                  

