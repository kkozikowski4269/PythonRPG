from states.player_states import PlayerAliveState, PlayerDeadState


class Player:
    def __init__(self):
        self.type = self.__class__.__name__
        self.name = None
        self.state = PlayerAliveState(self)
        self.current_location = None
        self.current_area = None
        self.x = 0
        self.y = 0
        self.observers = []
        self.weapon = None
        self.item_inventory = []
        self.weapon_inventory = []
        self.max_hp = 10
        self.hp = self.max_hp
        self.strength = 1
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 1
        self.special_defense = 1
        self.speed = 1
        self.xp = 0
        self.xp_to_level = 20
        self.level = 1
        self.stat_mods = {'strength': 0, 'wisdom': 0, 'dexterity': 0, 'defense': 0, 'special_defense': 0, 'speed': 0}

    def check_health(self):
        self.state.check_health()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.current_area.layout[self.y][self.x] = str(self)

    def clear_position(self):
        self.current_area.layout[self.y][self.x] = ' '

    def move(self, direction):
        dx = 0
        dy = 0
        if direction == 'up':
            dy = -1
        elif direction == 'down':
            dy = 1
        elif direction == 'left':
            dx = -1
        elif direction == 'right':
            dx = 1
        else:
            dy = 0
            dx = 0
        # check for wall collision
        next_space = self.current_area.layout[self.y+dy][self.x+dx]
        if next_space not in self.current_area.WALLS:
            self.clear_position()
            self.set_position(self.x+dx, self.y+dy)

    def is_colliding(self, obj2):
        if self.x == obj2.x and self.y == obj2.y:
            return True
        return False

    def is_alive(self):
        return self.state.is_alive()

    def get_stat(self, stat):
        if stat == 'strength':
            return self.strength + self.stat_mods['strength']
        elif stat == 'dexterity':
            return self.dexterity + self.stat_mods['dexterity']
        elif stat == 'wisdom':
            return self.wisdom + self.stat_mods['wisdom']
        elif stat == 'defense':
            return self.wisdom + self.stat_mods['defense']
        elif stat == 'special_defense':
            return self.wisdom + self.stat_mods['special_defense']
        elif stat == 'speed':
            return self.wisdom + self.stat_mods['speed']

    def reset_stat_mods(self):
        for stat in self.stat_mods.keys():
            self.stat_mods[stat] = 0

    def notify_observers(self, game):
        for observer in self.observers:
            observer.observe_player(self, game)

    def __str__(self):
        return 'P'

    def main_attack(self):
        damage = self.weapon.main_attack()
        if damage > 0:
            if self.weapon.secondary_type is not None:
                damage += (self.get_stat(self.weapon.secondary_type)*0.5) + (self.get_stat(self.weapon.primary_type)*0.75)
            else:
                damage += self.get_stat(self.weapon.primary_type)

        return int(damage)

    def alt_attack(self):
        damage = self.weapon.alt_attack()
        if damage > 0:
            if self.weapon.secondary_type is not None:
                damage += (self.get_stat(self.weapon.secondary_type) * 0.5) + (
                            self.get_stat(self.weapon.primary_type) * 0.75)
            else:
                damage += self.get_stat(self.weapon.primary_type)

        return damage

    def check_level_up(self, xp):
        self.xp += xp
        if self.xp >= self.xp_to_level:
            self.level += 1
            self.xp = self.xp % self.xp_to_level
            self.xp_to_level = int(self.xp_to_level + (self.xp_to_level*0.2))
            return True
        return False


class Knight(Player):
    def __init__(self):
        super().__init__()
        self.max_hp = 200
        self.hp = self.max_hp
        self.strength = 5
        self.wisdom = 5
        self.dexterity = 5
        self.defense = 5
        self.special_defense = 4
        self.speed = 5

# For testing
# class Knight(Player):
#     def __init__(self):
#         super().__init__()
#         self.max_hp = 2000
#         self.hp = self.max_hp
#         self.strength = 500
#         self.wisdom = 500
#         self.dexterity = 500
#         self.defense = 500
#         self.special_defense = 400
#         self.speed = 500


class Warrior(Player):
    def __init__(self):
        super().__init__()
        self.max_hp = 150
        self.hp = self.max_hp
        self.strength = 13
        self.wisdom = 1
        self.dexterity = 1
        self.defense = 3
        self.special_defense = 1
        self.speed = 5


class Wizard(Player):
    def __init__(self):
        super().__init__()
        self.max_hp = 150
        self.hp = self.max_hp
        self.strength = 3
        self.wisdom = 10
        self.dexterity = 3
        self.defense = 3
        self.special_defense = 6
        self.speed = 5


class Rogue(Player):
    def __init__(self):
        super().__init__()
        self.max_hp = 150
        self.hp = self.max_hp
        self.strength = 3
        self.wisdom = 3
        self.dexterity = 10
        self.defense = 2
        self.special_defense = 2
        self.speed = 7
