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
            'GrassFloor': load_images('tiles/GrassFloor'),
            'Water': load_images('tiles/Water'),
            
            'player/' + PlayerActions.STANDING.value: Animation(load_images('player/' + PlayerActions.STANDING.value)),
            'player/' + PlayerActions.UP.value: Animation(load_images('player/' + PlayerActions.UP.value)),
            'player/' + PlayerActions.DOWN.value: Animation(load_images('player/' + PlayerActions.DOWN.value)),
            'player/' + PlayerActions.RIGHT.value: Animation(load_images('player/' + PlayerActions.RIGHT.value)),
            'player/' + PlayerActions.LEFT.value: Animation(load_images('player/' + PlayerActions.LEFT.value))
        }

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self)
        self.tilemap.load('map.json')


    def run(self):
        while True:
            self.display.fill((0, 171, 65))

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
