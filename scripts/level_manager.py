from random import randint
from scripts.fighter_statictics import Stats

MAX_LVL = 15


class LevelManager:
    def __init__(self, animal, item_collector, level=1):
        self.animal = animal
        self.item_collector = item_collector
        self.level = level
        self.xp = 0
        

    def xp_to_next_level(self, level):   
        return round( 0.04 * (level ** 3) + 0.8 * (level ** 2) + 2 * level) + 5
    
    
    def render(self, surf):
        pass
        # print(self.level)
        

    def update(self, xp):
        if self.level == MAX_LVL: return
        self.xp = max(0, self.xp + xp)
        if self.xp >= self.xp_to_next_level(self.level):
            self.level += 1
            
            if self.level == MAX_LVL: self.xp = self.xp_to_next_level(self.level)
            else: self.xp = 0
            
            new_items = 5
            
            self.item_collector.new_random_items(new_items)
            return NewLevelWindow(self.level, self.animal)
        

class NewLevelWindow:
    def __init__(self, new_level, animal):
        self.new_level = new_level
        self.animal = animal
        self.finish = False
        
    def render(self, surf):
        print(f"Level UP! {self.new_level - 1} -> {self.new_level}")
        rand_stats = self.random_stats()
        for stat, val in rand_stats:
            print(stat, val)
        i = int(input("Select stat to upgrade"))
        self.animal.stats[rand_stats[i][0]] += rand_stats[i][1]
        
        self.finish = True
        print(self.animal.stats)
        
    def random_stats(self):
        all_stats = list(self.animal.stats.keys())
        rand_stats = []
        for _ in range(3):
            i = randint(0, len(all_stats) - 1)
            stat = all_stats.pop(i)
            val = 0
            
            match stat:
                case Stats.HEALTH:
                    val = randint(8, 12)
                case Stats.ATTACK:
                    val = randint(2, 4)
                case Stats.DEFENCE:
                    val = randint(1, 3)
                case Stats.CRITICAL_DMG:
                    val = 1
                case Stats.AGILITY:
                    val = randint(1, 2)
                case Stats.LUCK:
                    val = 1
                    
            rand_stats.append((stat, val))
        return rand_stats
    
    def is_finished(self):
        return self.finish
                    
    #     self.health = randint(8*level, 11*level)
    #     self.attack = randint(2*level, 3*level)
    #     self.defence = randint(level, int(level*1.5))
    #     self.critical_dmg = randint(0, 10)
    #     self.agility = randint(level, int(level*1.5))
    #     self.luck = randint(0, 10)
