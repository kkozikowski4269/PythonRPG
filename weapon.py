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

    def main_attack(self):
        return 2

    def alt_attack(self):
        return 20


class Hammer(Weapon):
    def __init__(self, power):
        super().__init__(power)
        self.name = 'Hammer'

    def main_attack(self):
        return 10

    def alt_attack(self):
        return 20


class Dagger(Weapon):
    def __init__(self, power):
        super().__init__(power)
        self.name = 'Dagger'

    def main_attack(self):
        return 10

    def alt_attack(self):
        return 20


class Staff(Weapon):
    def __init__(self, power):
        super().__init__(power)
        self.name = 'Staff'

    def main_attack(self):
        return 10

    def alt_attack(self):
        return 20
