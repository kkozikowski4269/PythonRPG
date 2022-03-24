class Weapon:
    def __init__(self):
        self.name = None
        self.power = 0
        self.primary_type = None
        self.secondary_type = None


class Sword(Weapon):
    def __init__(self):
        super.__init__()
