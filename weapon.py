class Weapon:
    def __init__(self):
        self.name = None
        self.power = 0
        self.level = 0
        self.primary_type = None
        self.secondary_type = None

    def main_attack(self):
        return 2

    def alt_attack(self):
        return 20


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.name = 'Sword'

    def main_attack(self):
        return 2

    def alt_attack(self):
        return 20


class Hammer(Weapon):
    def __init__(self):
        super().__init__()
        self.name = 'Hammer'

    def main_attack(self):
        return 10

    def alt_attack(self):
        return 20


class Dagger(Weapon):
    def __init__(self):
        super().__init__()
        self.name = 'Dagger'

    def main_attack(self):
        return 10

    def alt_attack(self):
        return 20


class Staff(Weapon):
    def __init__(self):
        super().__init__()
        self.name = 'Staff'

    def main_attack(self):
        return 10

    def alt_attack(self):
        return 20
