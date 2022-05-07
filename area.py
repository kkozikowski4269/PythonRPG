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
        self.visited = False
        self.x = area_json['x']
        self.y = area_json['y']
        self.name = area_json['name']
        self.code = area_json['code']
        self.image_path = area_json['image']
        self.symbol = area_json['symbol']
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
                        enemy = self.create_random_strong_enemy(int(random.choice(self.area_json["enemy levels"])))
                        enemy.set_spawn_position(x, y)
                        c = ' '
                    elif c == 'e':
                        enemy = self.create_random_weak_enemy(int(random.choice(self.area_json["enemy levels"])))
                        enemy.set_spawn_position(x, y)
                        c = ' '
                    elif c in EnemyFactory.ALL_ENEMY_TYPES:
                        enemy = self.create_enemy(c, int(random.choice(self.area_json["enemy levels"])))
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

    def leave(self, player):
        self.despawn_enemies()
        player.observers.clear()
        player.clear_position()

    def enter(self, player, x, y):
        self.spawn_enemies()
        player.observers = self.enemies + list(self.doors.values())
        player.current_area = self
        player.set_position(x, y)

    def print_area(self):
        for row in self.layout:
            print(*row, sep="")

    def create_enemy(self, enemy_type, level):
        enemy_factory = EnemyFactory()
        enemy = enemy_factory.get(enemy_type, level)
        enemy.area = self
        self.enemies.append(enemy)
        return enemy

    def create_random_weak_enemy(self, level):
        enemy_factory = EnemyFactory()
        enemy = enemy_factory.get(random.choice(EnemyFactory.WEAK_ENEMY_TYPES), level)
        enemy.area = self
        self.enemies.append(enemy)
        return enemy

    def create_random_strong_enemy(self, level):
        enemy_factory = EnemyFactory()
        enemy = enemy_factory.get(random.choice(EnemyFactory.STRONG_ENEMY_TYPES), level)
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
