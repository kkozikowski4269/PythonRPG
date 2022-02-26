import json

from area import Area
from states.player_states import PlayerAliveState, PlayerDeadState


class Player:
    def __init__(self):
        self.name = None
        self.hp = 20
        self.state = PlayerAliveState(self)
        self.current_location = "location1"
        self.current_area = None
        self.x = 0
        self.y = 0

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
        print(self.current_area.layout[self.y+dy][self.x+dx])
        if self.current_area.layout[self.y+dy][self.x+dx] not in Area.WALLS:
            self.clear_position()
            self.set_position(self.x+dx, self.y+dy)


    def __str__(self):
        return 'P'


class Knight(Player):
    def __init__(self):
        super().__init__()


class Warrior(Player):
    def __init__(self):
        super().__init__()


class Wizard(Player):
    def __init__(self):
        super().__init__()


class Rogue(Player):
    def __init__(self):
        super().__init__()

