import pygame
from enum import Enum
from scripts.backpack import Backpack

class PlayerActions(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
    STANDING = 'standing'
    

# TODO Dziedziczenie z fighter?
class Player:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.running = False
        self.backpack = Backpack()
        
        self.action = PlayerActions.UP
        self.update_action(PlayerActions.STANDING)


    def rect(self):
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0] - 2, self.size[1] // 2)
        rect.center = (self.pos[0]  + self.size[0] // 2, self.pos[1] + 3 * self.size[1] // 4)
        return rect
    

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.animation = self.game.assets["player/" + self.action.value]  
            self.animation.set_start_state()
                

    def update(self, tilemap, movement=(0, 0)):
        frame_movement = (movement[0], movement[1])
        
        is_running = 1
        if self.running: is_running = 2     # setting running speed

        self.pos[0] += frame_movement[0] * is_running
        entity_rect = self.rect()
        for rect in tilemap.forbidden_rects(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x - 1

        self.pos[1] += frame_movement[1] * is_running
        entity_rect = self.rect()
        for rect in tilemap.forbidden_rects(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                self.pos[1] = entity_rect.y - self.size[1] // 2
             
        new_action = PlayerActions.STANDING   
        if movement[0] > 0: new_action = PlayerActions.RIGHT
        elif movement[0] < 0: new_action = PlayerActions.LEFT
        
        if movement[1] > 0: new_action = PlayerActions.DOWN
        elif movement[1] < 0: new_action = PlayerActions.UP
                
        self.update_action(new_action)
        self.animation.update()


    def render(self, surf, offset=(0,0)):
        surf.blit(self.animation.get_img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    