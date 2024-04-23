import pygame

from scripts.fighter import Fighter


class Enemy(Fighter):
    def __init__(self, img, health, attack, defence, critical_dmg, agility, luck, moves, level=1):
        super().__init__(img, health, attack, defence, critical_dmg, agility, luck, moves, level)

# {"enemies/gadwall.png": {"Z dzioba": 1},
# "Gęś": {"Z dzioba": 1},
# "Kaczka Krzyżówka": {"Z dzioba": 1},
# "Bezpłetwiec": {"Z dzioba": 1},
# "Wodniczka": {"Z dzioba": 1}}
