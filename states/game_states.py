from os import system
from player import Knight
from player_factory import PlayerFactory
from states.player_states import PlayerDeadState
from util import get_image


class IntroState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        choice = input(">>>")
        if choice == "1":
            self.game.set_save_file_name(self.create_player_name())
            self.game.set_state(NewGameState(self.game))
        elif choice == "2":
            self.game.set_state(LoadGameState(self.game))
        elif choice == "5":
            self.game.set_state(EndState(self.game))
        system('cls')

    def display(self):
        print(get_image("images/menu/title_screen.txt"))
        print(get_image("images/menu/main_menu.txt"))

    def create_player_name(self):
        player_name = ""
        while len(player_name) < 1 or len(player_name) > 20:
            player_name = input("Enter your name: ")
            if len(player_name) < 1:
                print("Name cannot be blank.")
                input("\n\nPress enter to continue.")
            elif len(player_name) > 20:
                print("Name cannot be longer than 20 characters.")
                input("\n\nPress enter to continue.")
        return player_name


class NewGameState:
    def __init__(self, game):
        self.game = game
        self.game.set_locations()

    def get_user_input(self):
        player_factory = PlayerFactory()
        self.game.user_input = input(">>>")
        player_type = player_factory.get(self.game.user_input)
        if player_type is not None:
            self.game.set_player(player_type)
            self.game.player.set_name(self.game.save_file_name)
            self.game.player.set_area(self.game.locations['location1'].areas['A2'])
            self.game.set_state(RunningState(self.game))

    def display(self):
        print(get_image("images/menu/character_choice_menu.txt"))


class LoadGameState:
    def __init__(self, game):
        self.game = game
        self.border = "================"

    def get_user_input(self):
        self.game.user_input = input(">>>")
        if self.game.user_input == "Kevin":
            self.game.set_state(RunningState(self.game))
            self.game.set_player(Knight())
        system('cls')

    def display(self):
        system('cls')
        print(f"\n\n\tSaved Games:\n\t{self.border}")
        print(f"\tKevin\n\t{self.border}")


class DeleteGameState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        self.game.user_input = input(">>>")

    def display(self):
        print("In delete state")


class RunningState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        self.game.player.check_health()
        if type(self.game.player.state) is PlayerDeadState:
            self.game.set_state(EndState(self.game))
        else:
            self.game.user_input = input(">>>")
            self.game.player.hp -= 10


    def display(self):
        self.game.player.current_area.print_area()

class MenuState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        pass

    def display(self):
        print("In menu state")



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
