import random

from door import Door
# from states.game_states import BattleState
from factories.enemy_factory import EnemyFactory
from states.enemy_states import EnemySpawnedState, EnemyUnspawnedState


class Area:
    # list of UTF-8 symbols used for map layout
    WALLS = [chr(c) for c in range(0x2550, 0x256C + 1)]
    DOOR_SYMBOLS = ('u', 'r', 'd', 'l')

    def __init__(self, area_json):
        self.width = area_json['x']
        self.height = area_json['y']
        self.name = area_json['name']
        self.code = area_json['code']
        self.image_path = area_json['image']
        self.layout = []
        self.doors = {}
        self.area_json = area_json
        self.unspawned_enemies = []
        self.spawned_enemies = []
        self.enemies = []
        self.create_area()

    def __str__(self):
        return "Area: " + self.name

    # read area layout from text file and convert into a 2d array
    def create_area(self):
        for door in self.area_json['doors']:
            symbol = next(iter(door))
            destination = door[symbol]
            new_door = Door(symbol, destination)
            self.doors[symbol] = new_door

        with open(self.image_path, "r", encoding='utf-8') as file:
            for y, line in enumerate(file.readlines()):
                row = []
                for x, c in enumerate(line):
                    if c in Area.DOOR_SYMBOLS:
                        self.doors[c].set_position(x, y)
                        c = ' '
                    elif c == 'E':
                        enemy = self.create_random_strong_enemy()
                        enemy.set_spawn_position(x, y)
                        c = ' '
                    elif c == 'e':
                        enemy = self.create_random_weak_enemy()
                        enemy.set_spawn_position(x, y)
                        c = ' '
                    elif c in EnemyFactory.ALL_ENEMY_TYPES:
                        enemy = self.create_enemy(c)
                        enemy.set_spawn_position(x, y)
                        c = ' '
                    if c != '\n':
                        row.append(c)
                self.layout.append(row)
        file.close()

    def set_doors(self):
        for door in self.area_json['doors']:
            symbol = next(iter(door))
            destination = door[symbol]
            new_door = Door(symbol, destination)
            self.doors[symbol] = new_door

    # check if player is standing on a door space
    def check_doors(self, player):
        for door in self.doors.values():
            if player.is_colliding(door):
                self.leave(player)
                next_area_info = door.use_door(player)
                next_area = next_area_info[0]
                new_x_pos = next_area_info[1]
                new_y_pos = next_area_info[2]
                next_area.enter(player, new_x_pos, new_y_pos)

    def leave(self, player):
        self.despawn_enemies()
        player.clear_position()

    def enter(self, player, x, y):
        self.spawn_enemies()
        player.current_area = self
        player.set_position(x, y)

    def check_for_battle(self, player):
        for enemy in self.enemies:
            if enemy.is_alive() and player.is_colliding(enemy):
                return True, enemy
        return False, None

    def print_area(self):
        for row in self.layout:
            print(*row, sep="")

    def create_enemy(self, enemy_type):
        enemy_factory = EnemyFactory()
        enemy = enemy_factory.get(enemy_type)
        enemy.area = self
        self.enemies.append(enemy)
        return enemy

    def create_random_weak_enemy(self):
        enemy_factory = EnemyFactory()
        enemy = enemy_factory.get(random.choice(EnemyFactory.WEAK_ENEMY_TYPES))
        enemy.area = self
        self.enemies.append(enemy)
        return enemy

    def create_random_strong_enemy(self):
        enemy_factory = EnemyFactory()
        enemy = enemy_factory.get(random.choice(EnemyFactory.STRONG_ENEMY_TYPES))
        enemy.area = self
        self.enemies.append(enemy)
        return enemy

    def spawn_enemies(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                enemy.state = EnemySpawnedState(enemy)
            self.layout[enemy.y_spawn][enemy.x_spawn] = enemy

    def despawn_enemy(self, enemy):
        enemy.state = EnemyUnspawnedState(enemy)
        enemy.clear_position()
        enemy.reset_position()

    def despawn_enemies(self):
        for enemy in self.enemies:
            self.despawn_enemy(enemy)
