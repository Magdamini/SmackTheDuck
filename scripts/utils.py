import os
import pygame

BASE_IMG_PATH = 'data/images/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images


class Animation:
    def __init__(self, images, duration=5):
        self.images = images
        self.duration = duration
        self.frame = 0
        
    def set_start_state(self):
        self.frame = 0
        
    def update(self):
        self.frame = (self.frame + 1) % (self.duration * len(self.images))
    
    def get_img(self):
        return self.images[int(self.frame / self.duration)]
        
        