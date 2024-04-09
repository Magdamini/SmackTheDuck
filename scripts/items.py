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
        
class DuckLeg(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "03", "Duck Leg")
        
class RawMeat(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "04", "RawMeat")
        
class Shoes(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "05", "Shoes")
        
class Jacket(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "06", "Jacket")
        
class Blood(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "07", "Blood")
         
        
class SmallAggressionPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "09", "Small Aggression Potion")
        
class AggressionPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "10", "Aggression Potion")
        
class Flowers(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "11", "Flowers")
        
        
class Clover(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "12", "Clover")
        
class Stones(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "13", "Stones")
        
class Letter(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "14", "Letter")
        
class SmallAgilityPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "15", "Small Agility Potion")
        
class AgilityPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "16", "Agility Potion")
