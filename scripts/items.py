import pygame
from scripts.utils import load_image


class Item: 
    def __init__(self, x, y, img, name):
        self.x = x
        self.y = y
        self.img_name = img
        self.map_img = load_image(f'tiles/Items/{img}.png')
        self.img = self.map_img
        self.name = name

        
    def render(self, surf, offset=(0,0)):
        surf.blit(self.map_img, (self.x - offset[0], self.y - offset[1]))
        
    
  
# TODO check names        
class Plaster(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "00", "Plaster")
        
class Bandage(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "01", "Bandage")
        
class MedicalKit(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "02", "Medical Kit")
        
class todo1(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "03", "todo1")
        
class todo2(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "04", "todo2")
        
class Shoes(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "05", "Shoes")
        
class Jacket(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "06", "Jacket")
        
class Blood(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "07", "Blood")
        
class todo3(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "08", "todo3")
        
        
class SmallBottle1(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "09", "SmallBootle1")
        
class Bootle1(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "10", "Bootle1")
        
class Flowers(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "11", "Flowers")
        
        
class Clover(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "12", "Clover")
        
class todo4(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "13", "todo4")
        
class Letter(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "14", "Letter")
        
class SmallBottle2(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "15", "SmallBottle2")
        
class Bottle2(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "16", "Bottle2")
