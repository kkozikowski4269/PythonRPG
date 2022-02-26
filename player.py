import json

from area import Area
from states.player_states import PlayerAliveState


class Player:
    def __init__(self):
        self.name = None
        self.hp = 20
        self.state = PlayerAliveState(self)
        self.current_location = "location1"
        self.current_area = None

    def set_state(self, new_state):
        self.state = new_state

    def check_health(self):
        self.state.check_health()

    def set_name(self, name):
        self.name = name

    def set_area(self, area):
        self.current_area = area


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

