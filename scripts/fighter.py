import pygame
from time import sleep
from random import randint

class Fighter:
    def __init__(self, name, moves, level):
        self.name = name
        self.moves = moves

        self.level = level
        self.health = randint(8*level, 11*level)
        self.attack = randint(2*level, 3*level)
        self.defence = randint(level, int(level*1.5))
        self.critical_dmg = randint(0, 10)
        self.agility = randint(level, int(level*1.5))
        self.luck = randint(0, 10)


    def print_fight_beginning(self, other):
        print("You have encounterd".upper(), other.name)

        print(f"\n{self.name} WITH LEVEL: {self.level}")
        print("HEALTH:", self.health)
        print("ATTACK:", self.attack)
        print("DEFENCE:", self.defence)
        print("CRITICAL_DMG:", f"{self.critical_dmg}%")
        print("AGILITY:", self.agility)
        print("LUCK:", f"{self.luck}%")

        print("\n-- FIGHTS WITH --")

        print(f"\n{other.name} WITH LEVEL: {other.level}")
        print("HEALTH:", other.health)
        print("ATTACK:", other.attack)
        print("DEFENCE:", other.defence)
        print("CRITICAL_DMG:", f"{other.critical_dmg}%")
        print("AGILITY:", other.agility)
        print("LUCK:", f"{other.luck}%")

        sleep(2)


    def print_health(self, other):
        print(f"\n{self.name} HEALTH: {self.health}")
        print(f"{other.name} HEALTH: {other.health}")


    def perform_attack(self, other):
        other.health -= self.attack
        sleep(1)


    def fight(self, other):
        self.print_fight_beginning(other)
        fighters = [self, other] if self.agility > other.agility else [other, self]

        while self.health > 0 and other.health > 0:
            for i in range(len(fighters)):
                if isinstance(fighters[i], FightingPlayer):
                    fighters[i].perform_player_attack(fighters[i-1])
                else:
                    fighters[i].perform_attack(fighters[i-1])
                fighters[i-1].print_health(fighters[i])
                sleep(1)
                if fighters[i-1].health < 1:
                    print(f"\n \n{fighters[i].name} WON")
                    break
    

class FightingPlayer(Fighter):
    def __init__(self, moves, level=1):
        super().__init__("Gracz", moves, level)


    def key_down(self, event):
        # if event.key == pygame.K_1:
        #     return 1
        # if event.key == pygame.K_2:
        #     return 2
        # if event.key == pygame.K_3:
        #     return 3
        # if event.key == pygame.K_4:
        #     return 4
        pass
    

    def perform_player_attack(self, other):
        print("\n\n -- YOUR TURN -- \n")
        for i, move in enumerate(self.moves):
            print(f"{i+1}. ", move)
        # chosen_move = self.moves[self.key_down()]
        index_move = int(input("\nPick your move: "))
        chosen_move = self.moves[index_move-1]
        print("\nYou used ", chosen_move)
        other.health -= self.attack
        sleep(1)
