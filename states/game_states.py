import msvcrt
from enum import Enum
from os import system

import util
from player import Knight
from player_factory import PlayerFactory
from states.player_states import PlayerDeadState
from util import get_image


class RunningInputs(Enum):
    w = 'up'
    a = 'left'
    s = 'down'
    d = 'right'


class IntroState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        choice = input('>>>')
        if choice == '1':
            self.game.state = NewGameState(self.game)
        elif choice == '2':
            self.game.state = LoadGameState(self.game)
        elif choice == '3':
            self.game.state = DeleteGameState(self.game)
        elif choice == '5':
            self.game.state = EndState(self.game)
        system('cls')

    def display(self):
        print(get_image('images/menu/title_screen.txt'))
        print(get_image('images/menu/main_menu.txt'))

    def create_player_name(self):
        player_name = ""

        while len(player_name) < 1 or len(player_name) > 20:
            player_name = input('Enter your name: ')

            if len(player_name) < 1:
                print('Name cannot be blank.')
                input('\n\nPress enter to continue.')
            elif len(player_name) > 20:
                print('Name cannot be longer than 20 characters.')
                input('\n\nPress enter to continue.')

        return player_name


class NewGameState:
    def __init__(self, game):
        self.game = game
        self.game.set_locations()

    def get_user_input(self):
        if self.game.save_file_name is None:
            self.game.save_file_name = self.create_player_name()
        else:
            player_factory = PlayerFactory()
            user_input = input('>>>')
            player_type = player_factory.get(user_input)

            if player_type is not None:
                self.game.player = player_type
                self.game.player.name = self.game.save_file_name
                self.game.player.current_location = self.game.locations['location1']
                self.game.player.current_area = self.game.locations['location1'].areas['A2']
                self.game.player.set_position(1, 5)
                file_path = f'save_files/{self.game.save_file_name}.bin'
                self.game.save_manager.create_file(self.game, file_path)
                self.game.state = RunningState(self.game)

    def display(self):
        if self.game.save_file_name is None:
            pass
        else:
            print(get_image('images/menu/character_choice_menu.txt'))

    def create_player_name(self):
        player_name = ""

        while len(player_name) < 1 or len(player_name) > 20:
            player_name = input('Enter your name: ')

            if len(player_name) < 1:
                print('Name cannot be blank.')
                input('\n\nPress enter to continue.')
            elif len(player_name) > 20:
                print('Name cannot be longer than 20 characters.')
                input('\n\nPress enter to continue.')
            system('cls')

        return player_name


class LoadGameState:
    def __init__(self, game):
        self.game = game
        self.border = '================'

    def get_user_input(self):
        if len(self.game.save_manager.save_names) == 0:
            input()
            self.game.state = IntroState(self.game)
        else:
            user_input = input('>>>')
            if user_input == 'exit':
                self.game.state = IntroState(self.game)
            elif user_input in self.game.save_manager.save_names:
                file_name = f'save_files/{user_input}.bin'
                game_load = self.game.save_manager.load_game(file_name)
                self.set_game_attrs(game_load)
                self.game.state = RunningState(self.game)

    def display(self):
        print(util.get_image('images/menu/load_game_heading.txt'))
        if len(self.game.save_manager.save_names) == 0:
            print('\tThere are no saved games.')
            print('\n\t(Press enter to continue.)')
        else:
            print(f'\n\n\tSaved Games:\n\t{self.border}')
            for name in self.game.save_manager.save_names:
                print(f'\t{name}')
            print('\n\t(Enter "exit" to return to main menu)')

    # setting attributes individually for now because reassigning game wasn't working
    def set_game_attrs(self, game_load):
        self.game.state = game_load.state
        self.game.save_file_name = game_load.save_file_name
        self.game.player = game_load.player
        self.game.locations = game_load.locations

class DeleteGameState:
    def __init__(self, game):
        self.game = game
        self.border = '================'

    def get_user_input(self):
        if len(self.game.save_manager.save_names) == 0:
            input()
            self.game.state = IntroState(self.game)
        else:
            user_input = input('>>>')
            if user_input == 'exit':
                self.game.state = IntroState(self.game)
            elif user_input in self.game.save_manager.save_names:
                file_path = f'save_files/{user_input}.bin'
                self.game.save_manager.delete_game(user_input, file_path)

    def display(self):
        print(util.get_image('images/menu/delete_game_heading.txt'))
        if len(self.game.save_manager.save_names) == 0:
            print('\tThere are no saved games.')
            print('\n\t(Press enter to continue.)')
        else:
            print(f'\n\n\tSaved Games:\n\t{self.border}')
            for name in self.game.save_manager.save_names:
                print(f'\t{name}')
            print('\n\t(Enter "exit" to return to main menu)')


class RunningState:

    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        # get keyboard input
        user_input = msvcrt.getch().decode()
        # ----------------------------------------
        # temporary quit key
        if user_input == 'p':
            self.game.state = EndState(self.game)
        # ----------------------------------------
        if user_input == 'm':
            self.game.state = MenuState(self.game)
        try:
            # try to move player
            self.game.player.move(RunningInputs[user_input].value)
            self.game.player.current_area.check_doors(self.game.player)
        except KeyError:
            pass

    def display(self):
        self.game.player.current_area.print_area()
        print(self.game.state)


class MenuState:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player

    def get_user_input(self):
        user_input = msvcrt.getch().decode()
        if user_input == 'm':
            self.game.state = RunningState(self.game)
        if user_input == 'x':
            self.game.state = EndState(self.game)
        if user_input == 's':
            file_name = f'save_files/{self.game.save_file_name}.bin'
            self.game.save_manager.save_game(self.game, file_name)

    def display(self):
        print(self.game.player.name)
        print(type(self.game.player))
        print('Paused')
        print('Press m key to resume')
        print('Press s key to save')
        print('press x key to exit')


class BattleState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        pass

    def display(self):
        print("In battle state")


class BattleMenuState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        pass

    def display(self):
        print("In battle menu state")


class GameOverState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        pass

    def display(self):
        print("In game over state")


class VictoryState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        pass

    def display(self):
        print("In victory state")


class EndState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        pass

    def display(self):
        print("In end state")
