import random

from states.enemy_states import EnemyUnspawnedState
from states.game_states import BattleState
from weapon import Sword, Staff


class Enemy:
    def __init__(self):
        self.type = self.__class__.__name__
        self.state = EnemyUnspawnedState(self)
        self.x = 0
        self.y = 0
        self.x_spawn = 0
        self.y_spawn = 0
        self.max_hp = 10
        self.hp = self.max_hp
        self.strength = 1
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 1
        self.special_defense = 1
        self.speed = 1
        self.area = None
        self.location = None
        self.icon = 'E'
        self.image = None
        self.battle_music = None
        self.inventory = []
        self.weapon_inventory = []

    def __str__(self):
        return self.icon

    def set_icon(self, icon):
        if type(icon) == str:
            self.icon = icon[0]

    def set_spawn_position(self, x, y):
        self.x_spawn = x
        self.y_spawn = y
        self.x = x
        self.y = y

    def reset_position(self):
        self.x = self.x_spawn
        self.y = self.y_spawn

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def clear_position(self):
        self.area.layout[self.y][self.x] = ' '

    def move(self):
        choice = random.randint(0, 4)
        dx = 0
        dy = 0
        if choice == 0:
            dy = 0
            dx = 0
        elif choice == 1:
            dy = -1
        elif choice == 2:
            dy = 1
        elif choice == 3:
            dx = -1
        elif choice == 4:
            dx = 1
        else:
            dy = 0
            dx = 0
        # check for wall collision
        next_space = self.area.layout[self.y + dy][self.x + dx]
        if next_space not in self.area.WALLS:
            self.clear_position()
            self.set_position(self.x + dx, self.y + dy)
            for door in self.area.doors.values():
                if self.is_colliding(door):
                    self.set_position(self.x + (-1 * dx), self.y + (-1 * dy))
            self.area.layout[self.y][self.x] = self

    def is_colliding(self, obj2):
        if self.x == obj2.x and self.y == obj2.y:
            return True
        return False

    def check_health(self):
        self.state.check_health()

    def is_alive(self):
        return self.state.is_alive()

    def attack(self):
        pass

    def observe_player(self, player, game):
        if self.state.is_alive():
            if self.is_colliding(player):
                game.state = BattleState(game, self)
            else:
                self.move()
                if self.is_colliding(player):
                    game.state = BattleState(game, self)

    def main_attack(self):
        return 1

    def alt_attack(self):
        return 2

    def fill_inventories(self):
        pass


class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.type = self.__class__.__name__
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.weapon_inventory = []

    def fill_inventories(self):
        self.weapon_drops = [None, Sword(1), Sword(2), Sword(3), Staff(1)]
        self.weapon_inventory = random.choices(self.weapon_drops, [50, 25, 10, 2, 13], k=1)



class Spider(Enemy):
    def __init__(self):
        super().__init__()
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.speed = 5


class Rat(Enemy):
    def __init__(self):
        super().__init__()
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.speed = 5


class Minotaur(Enemy):
    def __init__(self):
        super().__init__()
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.speed = 5


class Knight(Enemy):
    def __init__(self):
        super().__init__()
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.speed = 5


class Gargoyl(Enemy):
    def __init__(self):
        super().__init__()
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.speed = 5


class Demon(Enemy):
    def __init__(self):
        super().__init__()
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.speed = 5


class Dragon(Enemy):
    def __init__(self):
        super().__init__()
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.speed = 5
