import json
import os

from area import Area
from location import Location
from save_manager import SaveManager
from states.game_states import *


class Game:

    def __init__(self):
        self.state = IntroState(self)
        self.save_file_name = None
        self.player = None
        self.locations = {}
        self.save_manager = SaveManager('save_files/')
        self.volume = 1


    def set_locations(self):
        for file in os.listdir('locations'):
            with open(f'locations/{file}', encoding='utf-8') as json_file:
                area_json_file = json.load(json_file)
                location = Location(name=file[:-5])

                for area_json in area_json_file:
                    new_area = Area(area_json)
                    location.add_area(new_area)

                self.locations[location.name] = location

    def get_user_input(self):
        self.state.get_user_input()

    def display(self):
        self.state.display()

    def play(self):
        system('cls')
        util.set_volume(self.volume)
        while type(self.state) is not EndState:
            self.display()
            self.get_user_input()
            system('cls')

