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


def text_image(text, size, font="data/fonts/Retro.ttf", color=(0, 0, 0)):
    text_font = pygame.font.Font(font, size)
    return text_font.render(text, True, color)


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
        
        
        
class Button():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        
        self.img = img
        self.size = self.img.get_size()
        self.changed = False
        self.clicked = True
        

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        

    def render(self, surf, scale=2):
        pos = [p // scale for p in pygame.mouse.get_pos()]
        rect = pygame.Rect(self.x , self.y, self.size[0], self.size[1])

        if rect.collidepoint(pos):  # mouse over button
            if pygame.mouse.get_pressed()[0]: # left button pressed
                self.clicked = True
                
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
            self.changed = True
        
        surf.blit(self.img, (self.x, self.y))
    

    def is_clicked(self):
        return self.clicked and self.changed
    