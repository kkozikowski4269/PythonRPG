import json
import os

from area import Area
from location import Location
from states.game_states import *


class Game:

    def __init__(self):
        self.state = IntroState(self)
        self.save_file_name = None
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

    def get_user_input(self):
        self.state.get_user_input()

    def display(self):
        self.state.display()

    def play(self):
        system('cls')
        while type(self.state) is not EndState:
            self.display()
            self.get_user_input()
            system('cls')

