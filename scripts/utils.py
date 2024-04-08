import os
import pygame
import json

BASE_IMG_PATH = 'data/images/'


def load_json(path):
    file = open(path, 'r')
    data = json.load(file)
    file.close()
    return data


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        if os.path.isfile(BASE_IMG_PATH + path + '/' + img_name) and img_name.lower().endswith('.png'):
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
        
        