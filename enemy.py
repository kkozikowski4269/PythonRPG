import random

from states.enemy_states import EnemySpawnedState, EnemyUnspawnedState


class Enemy:
    def __init__(self):
        self.state = EnemyUnspawnedState(self)
        self.x = 0
        self.y = 0
        self.x_spawn = 0
        self.y_spawn = 0
        self.hp = 10
        self.area = None
        self.location = None
        self.icon = 'E'

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
                    self.set_position(self.x + (-1*dx), self.y + (-1*dy))
            self.area.layout[self.y][self.x] = self

    def is_colliding(self, obj2):
        if self.x == obj2.x and self.y == obj2.y:
            return True
        return False

    def is_alive(self):
        return type(self.state) == EnemySpawnedState
