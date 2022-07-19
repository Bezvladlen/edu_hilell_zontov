import random

class Unit:
    def __init__(self, name, health=100, power=1, agility=1, intellect=1):
        self.name = name
        self.health = health
        self.power = power
        self.agility = agility
        self.intellect = intellect

    def get_name(self):
        return self.name

    def get_damage(self):
        self.health = int(self.health - self.health * random.randrange(1, 21)/100)
        if self.health < 0:
            self.health = 0

    def healing(self):
        self.health = int(self.health + self.health * random.randrange(1, 21)/100)
        if self.health > 100:
            self.health = 100

    def __repr__(self):
        return f"({self.name}, {self.health}, {self.power}, {self.agility}, {self.intellect})"


class Mage(Unit):
    def __init__(self, name, health=100, power=1, agility=1, intellect=1):
        super().__init__(name=name, health=health, power=power, agility=agility, intellect=intellect)
        self.mage_type = random.choice(["Fire", "Air", "Water"])

    def get_level_up(self):
        self.intellect += int(self.intellect < 10)

    def __str__(self):
        str_unit = super().__str__()
        return f"{str_unit}, Mage type - {self.mage_type}"


class Archer(Unit):
    def __init__(self, name, health=100, power=1, agility=1, intellect=1):
        super().__init__(name=name, health=health, power=power, agility=agility, intellect=intellect)
        self.bow_type = random.choice(["Bow", "Crossbow", "Sling"])

    def get_level_up(self):
        self.intellect += int(self.agility < 10)

    def __str__(self):
        str_unit = super().__str__()
        return f"{str_unit}, Bow type - {self.bow_type}"


class Knight(Unit):
    def __init__(self, name, health=100, power=1, agility=1, intellect=1):
        super().__init__(name=name, health=health, power=power, agility=agility, intellect=intellect)
        self.weapon_type = random.choice(["Sword", "Ax", "Pike"])

    def get_level_up(self):
        self.intellect += int(self.power < 10)

    def __str__(self):
        str_unit = super().__str__()
        return f"{str_unit}, Weapon type - {self.weapon_type}"
