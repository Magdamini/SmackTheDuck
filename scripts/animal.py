import pygame

from scripts.utils import load_image

class Animal:
    def __init__(self, img, size=64, level=1):
        self.img = pygame.transform.scale(load_image(img), (size, size))
        self.lvl = level
        
        
    def render(self, surf, x, y):
        surf.blit(self.img, (x, y))
        
        
    