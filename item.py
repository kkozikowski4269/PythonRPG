class Item:
    def __init__(self):
        self.name = None
        self.description = None

    def use(self, target):
        pass

    def __str__(self):
        return self.name


class HealthPotion(Item):
    def __init__(self, heal_amount):
        super().__init__()
        self.heal_amount = heal_amount

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.name == other.name and self.heal_amount == other.heal_amount

    def __lt__(self, other):
        return self.heal_amount < other.heal_amount

    def __hash__(self):
        return hash(self.name) + hash(self.heal_amount)

    def use(self, target):
        if (target.hp + self.heal_amount) >= target.max_hp:
            target.hp = target.max_hp
        else:
            target.hp += self.heal_amount


class Elixir(Item):
    def __init__(self):
        super().__init__()
        self.heal_percentage = 0.5

    def __hash__(self):
        return hash(self.name) + hash(self.heal_percentage)

    def use(self, target):
        target.hp += int((target.max_hp - target.hp) * 0.5)




class StatPotion(Item):
    def __init__(self, boost_amount, stat_type):
        super().__init__()
        self.boost_amount = boost_amount
        self.stat_type = stat_type

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.name == other.name and self.stat_type == other.stat_type and self.boost_amount == other.boost_amount

    def __lt__(self, other):
        return self.boost_amount < other.boost_amount

    def __hash__(self):
        return hash(self.name) + hash(self.boost_amount) + hash(self.stat_type)

    def use(self, target):
        if target.stat_mods[self.stat_type] < self.boost_amount:
            target.stat_mods[self.stat_type] = self.boost_amount


