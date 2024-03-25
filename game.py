import sys

import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
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
            'player': load_image('player/0;0.png')
        }

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

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
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()
