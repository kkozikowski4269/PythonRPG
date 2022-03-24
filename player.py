from states.player_states import PlayerAliveState, PlayerDeadState


class Player:
    def __init__(self):
        self.name = None
        self.state = PlayerAliveState(self)
        self.current_location = None
        self.current_area = None
        self.x = 0
        self.y = 0
        self.observers = []

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

    def notify_observers(self, game):
        for observer in self.observers:
            observer.do_action(self, game)

    def __str__(self):
        return 'P'


class Knight(Player):
    def __init__(self):
        super().__init__()
        self.hp = 200
        self.strength = 5
        self.wisdom = 5
        self.dexterity = 5
        self.defense = 5
        self.special_defense = 4


class Warrior(Player):
    def __init__(self):
        super().__init__()
        self.hp = 150
        self.strength = 13
        self.wisdom = 1
        self.dexterity = 1
        self.defense = 3
        self.special_defense = 1


class Wizard(Player):
    def __init__(self):
        super().__init__()
        self.hp = 150
        self.strength = 3
        self.wisdom = 10
        self.dexterity = 3
        self.defense = 3
        self.special_defense = 6


class Rogue(Player):
    def __init__(self):
        super().__init__()
        self.hp = 150
        self.strength = 3
        self.wisdom = 3
        self.dexterity = 10
        self.defense = 3
        self.special_defense = 2
