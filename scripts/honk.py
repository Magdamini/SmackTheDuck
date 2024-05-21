from scripts.enemy import Enemy
from scripts.utils import text_image, load_image
import pygame

# TODO dać statsy i moves bo nie wiem co to xd
MOVES = {"attack": [1, 0, 0]}


class Boss(Enemy):
    def __init__(self, map):
        img = "NPC/Basic/honk.png"
        super().__init__(img, 12, 10, 10, 1, 1, 1, MOVES, 15)
        
        map.boss = self
        
        self.pos = (125, 90)
        self.size = 80
        self.name = "Honk"
        self.map_img = pygame.transform.scale(load_image(img), (self.size, self.size))
        self.touch_player = False
        
    
    def rect(self):
        offset = 5
        rect = pygame.Rect(0, 0, self.size + 2 * offset, self.size + 2 * offset)
        rect.center = (self.pos[0] + self.size // 2, self.pos[1] + self.size // 2)
        return rect
        
        
    def render_on_map(self, surf, player, offset=(0, 0)):
        surf.blit(self.map_img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        if player.rect().colliderect(self.rect()):
            talk_text = text_image("[F] - Fight", 10, color=(255, 255, 255))
            rect = pygame.Rect(0, self.pos[1] - offset[1], talk_text.get_width(), talk_text.get_height())
            rect.centerx = self.pos[0] - offset[0] + self.size // 2

            rect.y += talk_text.get_height() + self.size
            surf.blit(talk_text, (rect.x, rect.y))
            self.touch_player = True
        else:
            self.touch_player = False
