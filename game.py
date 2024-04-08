import sys
import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.player import Player, PlayerActions
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):        
        pygame.init()

        pygame.display.set_caption('Best game ever made')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

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
            
            'player/' + PlayerActions.STANDING.value: Animation(load_images('player/' + PlayerActions.STANDING.value)),
            'player/' + PlayerActions.UP.value: Animation(load_images('player/' + PlayerActions.UP.value)),
            'player/' + PlayerActions.DOWN.value: Animation(load_images('player/' + PlayerActions.DOWN.value)),
            'player/' + PlayerActions.RIGHT.value: Animation(load_images('player/' + PlayerActions.RIGHT.value)),
            'player/' + PlayerActions.LEFT.value: Animation(load_images('player/' + PlayerActions.LEFT.value))
        }

        self.player = Player(self, (50, 50), (16, 16))

        self.tilemap = Tilemap(self)
        # self.tilemap.load('map.json')
        self.tilemap.load('data/maps/0.json')


    def run(self):
        while True:
            self.display.fill((self.tilemap.tilemap["background_color"]["R"], self.tilemap.tilemap["background_color"]["G"], self.tilemap.tilemap["background_color"]["B"]))  

            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
            self.player.render(self.display)

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
                    
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.movement[0] = False
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.movement[1] = False
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.movement[2] = False
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.movement[3] = False
                    if event.key  == pygame.K_LSHIFT:
                        self.player.running = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().run()
