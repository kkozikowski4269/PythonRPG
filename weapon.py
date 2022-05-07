import random


class Weapon:
    def __init__(self, power):
        self.name = None
        self.power = power
        self.primary_type = None
        self.secondary_type = None

    def main_attack(self):
        return 2

    def alt_attack(self):
        return 20


class Sword(Weapon):
    def __init__(self, power):
        super().__init__(power)
        self.name = 'Sword'
        self.primary_type = 'strength'
        self.secondary_type = 'dexterity'

    def main_attack(self):
        return random.choices([0, random.choice([1, 2]), 4], [10, 80, 10], k=1)[0]

    def alt_attack(self):
        return random.choices([0, random.randrange(1, 4, 1), 8], [30, 55, 15], k=1)[0]


class Hammer(Weapon):
    def __init__(self, power):
        super().__init__(power)
        self.name = 'Hammer'
        self.primary_type = 'strength'

    def main_attack(self):
        return random.choices([0, 3], [20, 80], k=1)[0]

    def alt_attack(self):
        return random.choices([0, 6], [40, 60], k=1)[0]


class Dagger(Weapon):
    def __init__(self, power):
        super().__init__(power)
        self.name = 'Dagger'
        self.primary_type = 'dexterity'

    def main_attack(self):
        return random.choices([1, 2], [75, 25], k=1)[0]

    def alt_attack(self):
        return random.choices([0, 1, 2, 3, 4, 5], [20, 20, 20, 15, 15, 10], k=1)[0]


class Staff(Weapon):
    def __init__(self, power):
        super().__init__(power)
        self.name = 'Staff'
        self.primary_type = 'wisdom'

    def main_attack(self):
        return 10

    def alt_attack(self):
        return 20
