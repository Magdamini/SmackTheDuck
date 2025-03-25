from scripts.utils import load_image
from scripts.fighter_statictics import Stats


class Item:
    def __init__(self, x, y, img, name):
        self.x = x
        self.y = y
        self.img_name = img
        self.img = load_image(f"tiles/Items/{img}.png")
        self.name = name
        self.desc = ""

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.img, (self.x - offset[0], self.y - offset[1]))

    def use(self, fighter, battle_stat, how_much):
        fighter.battle_stats[battle_stat] += how_much


# TODO check names
class Plaster(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "00", "Plaster")
        self.desc = "+3 to Health"

    def use(self, fighter):
        how_much = min(
            3, fighter.stats[Stats.HEALTH] - fighter.battle_stats[Stats.HEALTH]
        )
        super().use(fighter, Stats.HEALTH, how_much)


class Bandage(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "01", "Bandage")
        self.desc = "+10 to Health"

    def use(self, fighter):
        how_much = min(
            10, fighter.stats[Stats.HEALTH] - fighter.battle_stats[Stats.HEALTH]
        )
        super().use(fighter, Stats.HEALTH, how_much)


class MedicalKit(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "02", "Medical Kit")
        self.desc = "Heals from all injuries"

    def use(self, fighter):
        super().use(
            fighter,
            Stats.HEALTH,
            fighter.stats[Stats.HEALTH] - fighter.battle_stats[Stats.HEALTH],
        )


class DuckLeg(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "03", "Duck Leg")
        self.desc = "+2 to Attack"

    def use(self, fighter):
        super().use(fighter, Stats.ATTACK, 2)


class RawMeat(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "04", "Raw Meat")
        self.desc = "+5 to Attack"

    def use(self, fighter):
        super().use(fighter, Stats.ATTACK, 5)


class Shoes(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "05", "Shoes")
        self.desc = "+2 to Defence"

    def use(self, fighter):
        super().use(fighter, Stats.DEFENCE, 2)


class Jacket(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "06", "Jacket")
        self.desc = "+5 to Defence"

    def use(self, fighter):
        super().use(fighter, Stats.DEFENCE, 5)


class Blood(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "07", "Blood")
        self.desc = "+1 to Critical Dmg"

    def use(self, fighter):
        super().use(fighter, Stats.CRITICAL_DMG, 1)


class SmallAggressionPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "09", "Small Aggression Potion")
        self.desc = "+3 to Critical Dmg"

    def use(self, fighter):
        super().use(fighter, Stats.CRITICAL_DMG, 3)


class AggressionPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "10", "Aggression Potion")
        self.desc = "+5 to Critical Dmg"

    def use(self, fighter):
        super().use(fighter, Stats.CRITICAL_DMG, 5)


class Flowers(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "11", "Flowers")
        self.desc = "+2 to Luck"

    def use(self, fighter):
        super().use(fighter, Stats.LUCK, 2)


class Clover(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "12", "Clover")
        self.desc = "+5 to Luck"

    def use(self, fighter):
        super().use(fighter, Stats.LUCK, 5)


class Stones(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "13", "Stones")
        self.desc = "Deals 1 dmg to an enemy"

    def use(self, fighter):
        fighter.battle_stats[Stats.HEALTH] -= 1


class Letter(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "14", "Letter")


class SmallAgilityPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "15", "Small Agility Potion")
        self.desc = "+2 to Agility"

    def use(self, fighter):
        super().use(fighter, Stats.AGILITY, 2)


class AgilityPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "16", "Agility Potion")
        self.desc = "+5 to Agility"

    def use(self, fighter):
        super().use(fighter, Stats.AGILITY, 5)
