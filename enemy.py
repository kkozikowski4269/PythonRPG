import random

import factories.potion_factory
import util
from states.enemy_states import EnemyUnspawnedState
from states.game_states import BattleState, VictoryState, BattleEndState
from weapon import Sword, Staff, Hammer, Dagger
from factories import potion_factory


class Enemy:
    def __init__(self, level):
        self.type = self.__class__.__name__
        self.state = EnemyUnspawnedState(self)
        self.level = level
        self.xp = 0
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
            # prevent enemies from trying to move through door spaces
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

    def observe_player(self, player, game):
        if self.is_colliding(player):
            game.state = BattleState(game, self)
        else:
            self.move()
            if self.is_colliding(player):
                game.state = BattleState(game, self)

    def main_attack(self):
        return int(random.randrange(0, max([self.strength, self.dexterity, self.wisdom])*2))

    def alt_attack(self):
        return int(random.randrange(0, max([self.strength, self.dexterity, self.wisdom])*4))

    def fill_inventories(self):
        pass

    def attack(self):
        util.play_sound_effect('enemy_hit_sound.wav')
        damage = random.choices([self.main_attack(), self.alt_attack()], [75, 25], k=1)
        return int(damage[0])

    # scale enemy stats with their level
    def scale_stats(self):
        self.max_hp = self.max_hp * self.level
        self.strength = self.strength * self.level
        self.dexterity = self.dexterity * self.level
        self.wisdom = self.wisdom * self.level
        self.defense = self.defense * self.level
        self.special_defense = self.special_defense * self.level

    def on_defeat(self, game):
        game.state = BattleEndState(game, self)


class Skeleton(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.type = self.__class__.__name__
        self.max_hp = 10
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 1
        self.xp = 5*level
        self.weapon_inventory = []

    # temporary solution to giving enemies items to drop on defeat
    def fill_inventories(self):
        self.weapon_drops = [None, Sword(1), Sword(2), Sword(4), Dagger(3)]
        self.weapon_inventory = random.choices(self.weapon_drops, [50, 25, 10, 2, 13], k=1)
        self.inventory = random.choices([None, potion_factory.get('health', 'small'),
                                         potion_factory.get_random('small'),
                                         potion_factory.get_random('medium')],
                                        [40, 30, 20, 10], k=1)


class Spider(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.max_hp = 12
        self.hp = self.max_hp
        self.strength = 3
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 1
        self.special_defense = 1
        self.xp = 5*level
        self.speed = 7

    def fill_inventories(self):
        self.weapon_drops = [None, Dagger(1), Sword(2)]
        self.weapon_inventory = random.choices(self.weapon_drops, [50, 25, 25], k=1)
        self.inventory = random.choices(
            [None, potion_factory.get('health', 'small'), potion_factory.get_random('small')],
            [40, 35, 25], k=1)


class Rat(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.max_hp = 10
        self.hp = self.max_hp
        self.strength = 2
        self.dexterity = 1
        self.wisdom = 1
        self.defense = 2
        self.special_defense = 2
        self.xp = 5*level
        self.speed = 5

    def fill_inventories(self):
        self.weapon_drops = [None, Sword(1), Dagger(2), Hammer(3),]
        self.weapon_inventory = random.choices(self.weapon_drops, [50, 25, 15, 10], k=1)
        self.inventory = random.choices(
            [None, potion_factory.get('health', 'small'), potion_factory.get_random('small')],
            [40, 35, 25], k=1)


class Minotaur(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.max_hp = 35
        self.hp = self.max_hp
        self.strength = 8
        self.dexterity = 4
        self.wisdom = 1
        self.defense = 7
        self.special_defense = 3
        self.speed = 5
        self.xp = 11*level

    def fill_inventories(self):
        self.weapon_drops = [None, Hammer(4), Hammer(6)]
        self.weapon_inventory = random.choices(self.weapon_drops, [50, 35, 15], k=1)
        self.inventory = random.choices(
            [None, potion_factory.get('health', random.choice(['medium', 'large'])), potion_factory.get_random('large')],
            [30, 55, 15], k=2)


class Knight(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.max_hp = 30
        self.hp = self.max_hp
        self.strength = 5
        self.dexterity = 5
        self.wisdom = 3
        self.defense = 5
        self.special_defense = 4
        self.speed = 7
        self.xp = 11*level

    def fill_inventories(self):
        self.weapon_drops = [None, Sword(4), Sword(5), Sword(7), Dagger(6)]
        self.weapon_inventory = random.choices(self.weapon_drops, [30, 25, 15, 10, 20], k=1)
        self.inventory = random.choices(
            [None, potion_factory.get('health', random.choice(['medium', 'large'])),
             potion_factory.get_random('medium')],
            [30, 55, 15], k=2)


class Gargoyle(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.max_hp = 50
        self.hp = self.max_hp
        self.strength = 8
        self.dexterity = 3
        self.wisdom = 1
        self.defense = 10
        self.special_defense = 4
        self.speed = 3
        self.xp = 15*level

    def fill_inventories(self):
        self.weapon_drops = [None, Hammer(random.randint(5, 8)), Sword(random.randint(5, 8)), Dagger(random.randint(5, 8))]
        self.weapon_inventory = random.choices(self.weapon_drops, [52, 16, 16, 16], k=1)
        self.inventory = random.choices(
            [None, potion_factory.get('health', random.choice(['medium', 'large'])),
             potion_factory.get_random(random.choice(['medium', 'large']))],
            [30, 55, 15], k=2)


class Demon(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.max_hp = 40
        self.hp = self.max_hp
        self.strength = 6
        self.dexterity = 4
        self.wisdom = 8
        self.defense = 2
        self.special_defense = 7
        self.speed = 6
        self.xp = 15*level

    def fill_inventories(self):
        self.weapon_drops = [Sword(random.randint(1, 11)), Hammer(random.randint(1, 11)), Dagger(random.randint(1, 11))]
        self.weapon_inventory = random.choices(self.weapon_drops, [33, 33, 33], k=1)
        self.inventory = random.choices(
            [None, potion_factory.get('health', random.choice(['medium', 'large'])),
             potion_factory.get_random(random.choice(['medium', 'large']))],
            [30, 55, 15], k=2)


class Dragon(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.max_hp = 150
        self.hp = self.max_hp
        self.strength = 11
        self.dexterity = 8
        self.wisdom = 8
        self.defense = 10
        self.special_defense = 10
        self.speed = 9
        # self.xp = 30*level

    def on_defeat(self, game):
        game.state = VictoryState(game)
