import json
import os

from area import Area
from location import Location
from states.game_states import *


class Game:
    def __init__(self):
        self.state = IntroState(self)
        self.save_file_name = None
        self.user_input = None
        self.player = None
        self.locations = {}

    def set_locations(self):
        for file in os.listdir('locations'):
            with open(f'locations/{file}', encoding='utf-8') as json_file:
                area_json = json.load(json_file)
                location = Location(name=file[:-5])
                for area in area_json:
                    location.add_area(Area(area))
                self.locations[location.name] = location

    def set_state(self, new_state):
        self.state = new_state

    def set_player(self, player_type):
        self.player = player_type

    def get_user_input(self):
        self.state.get_user_input()

    def display(self):
        self.state.display()

    def set_save_file_name(self, name):
        self.save_file_name = name

    def play(self):
        # room1 = Map(0, 0, "")
        # room1.create_map()
        # x = 3
        # for x in range(x,x+15):
        #     room1.layout[3][x] = 'P'
        #     room1.print_map()
        #     room1.layout[3][x] = ' '

        system('cls')
        while type(self.state) is not EndState:
            self.display()
            self.get_user_input()
            system('cls')
