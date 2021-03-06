import msvcrt
import random
import re
from enum import Enum
from os import system
from time import sleep


import util
from factories.player_factory import PlayerFactory
from item import HealthPotion
from util import get_image


class RunningInputs(Enum):
    w = 'up'
    a = 'left'
    s = 'down'
    d = 'right'


"""
========================================================================================================================
INTRO STATE (MAIN MENU)
========================================================================================================================
"""


class IntroState:
    def __init__(self, game):
        self.game = game
        util.play_music('title_song.wav')

    def get_user_input(self):
        choice = input('>>>')
        if choice == '1':
            self.game.state = NewGameState(self.game)
        elif choice == '2':
            self.game.state = LoadGameState(self.game)
        elif choice == '3':
            self.game.state = DeleteGameState(self.game)
        elif choice == '4':
            self.game.state = SettingsState(self.game)
        elif choice == '5':
            self.game.state = EndState(self.game)
        system('cls')

    def display(self):
        print(get_image('images/menu/title_screen.txt'))
        print(get_image('images/menu/main_menu.txt'))


"""
========================================================================================================================
NEW GAME STATE
========================================================================================================================
"""


class NewGameState:
    def __init__(self, game):
        self.game = game
        self.game.set_locations()
        self.game.save_manager.get_save_files()

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
                self.game.hud.location = self.game.player.current_location
                self.game.hud.area = self.game.player.current_area
                self.game.player.current_area.enter(self.game.player, self.game.player.x, self.game.player.y)
                file_name = f'{self.game.save_file_name}.bin'
                self.game.save_manager.save_game(self.game, file_name)
                self.loading_bar(0.35, 'Creating character...')
                print(util.get_image(f'images/player/{player_type.type.lower()}.txt'))
                print(f'Welcome {self.game.player.name}!')
                input('Press enter to continue...')
                self.game.state = RunningState(self.game)
                self.game.hud.update_map()

    def display(self):
        if self.game.save_file_name is None:
            pass
        else:
            print(get_image('images/menu/character_choice_menu.txt'))

    def create_player_name(self):
        player_name = ''

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

    # lower s == faster speed
    def loading_bar(self, s, loading_msg, char="|"):
        print(loading_msg)
        for i in range(51):
            speed = random.uniform(0, s)
            print("0%|" + str(char * i).ljust(50) + "|" + str(i * 2) + "%\r", end="")
            sleep(speed)  # make loading bar move at a random/jumpy pace
        print()


"""
========================================================================================================================
LOAD GAME STATE
========================================================================================================================
"""


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
                file_name = f'{user_input}.bin'
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
            print('\n\t(Enter "exit" to go back)')

    # setting attributes individually for now because reassigning game wasn't working
    def set_game_attrs(self, game_load):
        self.game.state = game_load.state
        self.game.save_file_name = game_load.save_file_name
        self.game.player = game_load.player
        self.game.locations = game_load.locations
        self.game.volume = game_load.volume
        self.game.hud = game_load.hud
        util.set_volume(self.game.volume)


"""
========================================================================================================================
SETTINGS GAME STATE
========================================================================================================================
"""


class SettingsState:
    def __init__(self, game):
        self.game = game
        self.border = '================'
        self.previous_state = game.state

    def get_user_input(self):
        user_input = input('>>>')
        if user_input == 'exit':
            self.game.state = self.previous_state
        elif user_input == '1':
            self.game.state = SetVolumeState(self.game)
        elif user_input == '2':
            self.game.state = SetSFXVolumeState(self.game)

    def display(self):
        print(util.get_image('images/menu/settings/settings.txt'))
        print('\n\t(Enter "exit" to go back)')


"""
========================================================================================================================
SET VOLUME GAME STATE
========================================================================================================================
"""


class SetVolumeState:
    def __init__(self, game):
        self.game = game
        self.border = '================'
        self.previous_state = game.state

    def get_user_input(self):
        user_input = input('>>>')
        if user_input == 'exit':
            self.game.state = self.previous_state
        elif re.match('[0-9]', user_input):
            util.set_volume(int(user_input))
            self.game.volume = int(user_input)

    def display(self):
        print(util.get_image('images/menu/settings/volume.txt').replace('-', str(util.get_volume())))
        print('\n\t(Enter "exit" to go back)')


class SetSFXVolumeState:
    def __init__(self, game):
        self.game = game
        self.border = '================'
        self.previous_state = game.state

    def get_user_input(self):
        user_input = input('>>>')
        if user_input == 'exit':
            self.game.state = self.previous_state
        elif re.match('[0-9]', user_input):
            util.set_sfx_volume(int(user_input))
            self.game.sfx_volume = int(user_input)

    def display(self):
        print(util.get_image('images/menu/settings/sfx_volume.txt').replace('-', str(util.get_sfx_volume())))
        print('\n\t(Enter "exit" to go back)')


"""
========================================================================================================================
DELETE GAME STATE
========================================================================================================================
"""


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
                file_name = user_input
                self.game.save_manager.delete_game(file_name)

    def display(self):
        print(util.get_image('images/menu/delete_game_heading.txt'))
        if len(self.game.save_manager.save_names) == 0:
            print('\tThere are no saved games.')
            print('\n\t(Press enter to continue.)')
        else:
            print(f'\n\n\tSaved Games:\n\t{self.border}')
            for name in self.game.save_manager.save_names:
                print(f'\t{name}')
            print('\n\t(Enter "exit" to go back)')


"""
========================================================================================================================
RUNNING STATE
========================================================================================================================
"""


class RunningState:

    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        util.play_music('main_song.wav')

    def get_user_input(self):
        # get keyboard input
        user_input = msvcrt.getch().decode()
        # ----------------------------------------
        # temporary quit key
        # if user_input == 'p':
        #     self.game.state = EndState(self.game)
        # ----------------------------------------
        if user_input == 'm':
            self.game.state = MenuState(self.game)
        try:
            self.check_events(user_input)
        except KeyError:
            pass

    def display(self):
        self.game.hud.print_hud()
        self.player.current_area.print_area()

    def check_events(self, user_input):
        self.player.move(RunningInputs[user_input].value)
        self.player.notify_observers(self.game)


"""
========================================================================================================================
MENU STATE (OUT OF BATTLE MENU)
========================================================================================================================
"""


class MenuState:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        util.play_music('menu_song.wav')

    def get_user_input(self):
        user_input = input('>>>')
        if user_input == '1':
            self.game.state = UseItemState(self.game)
        elif user_input == '2':
            self.game.state = SelectWeaponState(self.game)
        elif user_input == '3':
            file_name = f'{self.game.save_file_name}.bin'
            self.game.save_manager.save_game(self.game, file_name)
            input('Game saved! (Enter to continue)')
        elif user_input == '4':
            self.game.state = SettingsState(self.game)
        elif user_input == '5':
            self.game.state = RunningState(self.game)
        elif user_input == '6':
            self.game.state = IntroState(self.game)
            self.game.reset()

    def display(self):
        print('\t\t(Paused)\n')
        print(f'\tName: {self.player.name}')
        print(f'\tClass: {self.player.type}')
        print(f'\tWeapon: {self.player.weapon.name}')
        print(f'\n\tHp: {self.player.hp}/{self.player.max_hp}')
        print(f'\tStrength: {self.player.strength}')
        print(f'\tDexterity: {self.player.dexterity}')
        print(f'\tWisdom: {self.player.wisdom}')
        print(f'\tDefense: {self.player.defense}')
        print(f'\tS Defense: {self.player.special_defense}')
        print(f'\tSpeed: {self.player.speed}\n')
        print(util.get_image('images/menu/pause_menu.txt'))


class SelectWeaponState:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.previous_state = game.state

    def get_user_input(self):
        user_input = input('>>>')
        if user_input.lower() == 'exit':
            self.game.state = self.previous_state
        elif re.match('[1-9]+', user_input):
            if int(user_input) - 1 < len(self.player.weapon_inventory):
                if self.player.weapon_inventory[int(user_input) - 1] is self.player.weapon:
                    input(f'This weapon is already equipped!\n(Enter to continue)')
                else:
                    self.player.weapon = self.player.weapon_inventory[int(user_input) - 1]
                    input(f'You have equipped: {self.player.weapon.name}\n(Enter to continue)')

    def display(self):
        print(f'\tCurrent weapon: {self.player.weapon.name}\n')
        print('\tWeapons:\n')
        self.player.weapon_inventory.sort()
        for i, weapon in enumerate(self.player.weapon_inventory):
            to_print = f'\t{i + 1}) {weapon.name} - Power: {weapon.power}'
            if weapon is self.player.weapon:
                to_print += ' (Equipped)'
            print(to_print)
        print('\n\t(Enter "exit" to go back)')


class UseItemState:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.previous_state = game.state
        self.item_types = list(set(self.player.item_inventory))

    def get_user_input(self):
        user_input = input('>>>')
        if user_input.lower() == 'exit':
            self.game.state = self.previous_state
        elif re.match('[1-9]+', user_input):
            if int(user_input) - 1 < len(self.item_types):
                item_index = self.player.item_inventory.index(self.item_types[int(user_input) - 1])
                if self.player.item_inventory[item_index].__class__ == HealthPotion:
                    self.player.item_inventory[item_index].use(self.player)
                    input(f'You use the {self.player.item_inventory[item_index]}')
                    del self.player.item_inventory[item_index]
                    self.game.state = self.previous_state
                else:
                    input(f'This item can only be used in battle')

    def display(self):
        print('\tInventory:\n')
        for i, item in enumerate(self.item_types):
            print(f'\t{i + 1}) (x{self.player.item_inventory.count(item)}) {item.name} - {item.description}')
        print('\n\t(Enter "exit" to go back)')


"""
========================================================================================================================
BATTLE STATES
========================================================================================================================
"""


class BattleState:
    def __init__(self, game, enemy):
        self.game = game
        self.enemy = enemy
        self.player = self.game.player
        util.play_music(enemy.battle_music)

    def get_user_input(self):
        input()
        self.player.observers.remove(self.enemy)
        if self.enemy.speed > self.player.speed:
            self.game.state = EnemyTurnBattleState(self.game, self.enemy)
        elif self.enemy.speed < self.player.speed:
            self.game.state = PlayerTurnBattleState(self.game, self.enemy)
        else:
            self.game.state = random.choice(
                (EnemyTurnBattleState(self.game, self.enemy), PlayerTurnBattleState(self.game, self.enemy))
            )

    def display(self):
        print(f'You are attacked by: {self.enemy.type}')
        print(self.enemy.image)
        print('(Enter to continue)')


class EnemyTurnBattleState:
    def __init__(self, game, enemy):
        self.game = game
        self.player = self.game.player
        self.enemy = enemy

    def get_user_input(self):
        damage = self.enemy.attack()
        modified_damage = int(damage * (10 / (10 + self.player.defense)))
        print(f'{self.enemy.type} hits you for {modified_damage}')
        self.player.hp -= modified_damage
        input()
        self.player.check_health()
        if self.player.is_alive():
            self.game.state = PlayerTurnBattleState(self.game, self.enemy)
        else:
            self.game.state = GameOverState(self.game)

    def display(self):
        print(f'{self.enemy.type} HP: {self.enemy.hp}')
        print(self.enemy.image)
        print(f'{self.player.name} HP: {self.player.hp}')


class PlayerTurnBattleState:
    def __init__(self, game, enemy):
        self.game = game
        self.player = self.game.player
        self.enemy = enemy

    def get_user_input(self):
        choice = input('>>>')
        if choice not in ('1', '2', '3'):
            return

        damage = 0
        if choice == '1':
            damage = self.player.main_attack()
        elif choice == '2':
            damage = self.player.alt_attack()
        elif choice == '3':
            self.game.state = BattleMenuState(self.game)
            return
        modified_damage = int(damage * (10 / (10 + self.enemy.defense)))
        print(f'You hit the {self.enemy.type} for {modified_damage}')
        self.enemy.hp -= modified_damage
        input()
        self.enemy.check_health()
        if self.enemy.is_alive():
            self.game.state = EnemyTurnBattleState(self.game, self.enemy)
        else:
            self.enemy.on_defeat(self.game)

    def display(self):
        print(f'{self.enemy.type} HP: {self.enemy.hp}')
        # print(f'Strength: {self.enemy.strength}')
        # print(f'Wisdom: {self.enemy.wisdom}')
        # print(f'Dexterity: {self.enemy.dexterity}')
        # print(f'Defense: {self.enemy.defense}')
        # print(f'S Defense: {self.enemy.special_defense}')
        # print(f'Speed: {self.enemy.speed}')
        print(self.enemy.image)
        print(f'{self.player.name} HP: {self.player.hp}')
        print(f'1) Main attack\n2) Alt Attack\n3) Menu')


class BattleEndState:
    def __init__(self, game, enemy):
        self.game = game
        self.player = self.game.player
        self.enemy = enemy
        self.total_xp = 0

    def get_user_input(self):
        input('\t(Enter to continue)')
        self.player.reset_stat_mods()
        if self.player.check_level_up(self.total_xp):
            self.game.state = LevelUpState(self.game)
        else:
            self.game.state = RunningState(self.game)
            self.player.current_area.layout[self.player.y][self.player.x] = str(self.player)

    def display(self):
        bonus_xp = 0
        print(f'\tYou defeated the {self.enemy.type} and received:')
        for weapon in self.enemy.weapon_inventory:
            if weapon is not None:
                if weapon not in self.player.weapon_inventory:
                    print(f'\t{weapon.name} - Power: {weapon.power}')
                    self.player.weapon_inventory.append(weapon)
                else:  # convert duplicate weapons to extra xp so inventory doesn't fill up with useless items
                    bonus_xp = weapon.power
        for item in self.enemy.inventory:
            if item is not None:
                self.player.item_inventory.append(item)
                print(f'\t{item.name} - {item.description}')
        print(f'\t{self.enemy.xp + bonus_xp} xp')
        self.total_xp = self.enemy.xp + bonus_xp


class LevelUpState:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.attribute_points = 3
        util.play_music('level_up_song.wav')

    def get_user_input(self):
        print('What would you like to level up?')
        choice = input('>>>')
        if choice == '1':
            self.player.max_hp += 20
        elif choice == '2':
            self.player.strength += 1
        elif choice == '3':
            self.player.wisdom += 1
        elif choice == '4':
            self.player.dexterity += 1
        elif choice == '5':
            self.player.defense += 1
        elif choice == '6':
            self.player.special_defense += 1
        elif choice == '7':
            self.player.speed += 1
        else:
            return

        self.attribute_points -= 1
        if self.attribute_points <= 0:
            self.game.state = RunningState(self.game)
            self.player.current_area.layout[self.player.y][self.player.x] = str(self.player)

    def display(self):
        print('Level Up!')
        print(f'You have {self.attribute_points} left')
        print(f'1) Max HP: {self.player.max_hp}')
        print(f'2) Strength: {self.player.strength}')
        print(f'3) Wisdom: {self.player.wisdom}')
        print(f'4) Dexterity: {self.player.dexterity}')
        print(f'5) Defense: {self.player.defense}')
        print(f'6) S Defense: {self.player.special_defense}')
        print(f'7) Speed: {self.player.speed}\n')


"""
========================================================================================================================
BATTLE MENU STATE (MENU WHILE IN BATTLE)
========================================================================================================================
"""


class BattleMenuState:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.previous_state = game.state

    def get_user_input(self):
        user_input = input('>>>')
        if user_input == '1':
            self.game.state = UseItemBattleState(self.game)
        elif user_input == '2':
            self.game.state = SelectWeaponState(self.game)
        elif user_input == '3':
            self.game.state = SettingsState(self.game)
        elif user_input == '4':
            self.game.state = self.previous_state

    def display(self):
        print(f'\t\tStats:')
        print(f'\tHp: {self.player.hp}/{self.player.max_hp}')
        print(f'\tStrength: {self.player.get_stat("strength")}')
        print(f'\tDexterity: {self.player.get_stat("dexterity")}')
        print(f'\tWisdom: {self.player.get_stat("wisdom")}')
        print(f'\tDefense: {self.player.get_stat("defense")}')
        print(f'\tS Defense: {self.player.get_stat("special_defense")}')
        print(f'\tSpeed: {self.player.get_stat("speed")}\n')
        print(util.get_image('images/menu/battle/battle_menu.txt'))


class UseItemBattleState:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.previous_state = game.state
        self.item_types = list(set(self.player.item_inventory))

    def get_user_input(self):
        user_input = input('>>>')
        if user_input.lower() == 'exit':
            self.game.state = self.previous_state
        elif re.match('[1-9]+', user_input):
            if int(user_input) - 1 < len(self.item_types):
                item_index = self.player.item_inventory.index(self.item_types[int(user_input) - 1])
                self.player.item_inventory[item_index].use(self.player)
                input(f'You use the {self.player.item_inventory[item_index]}')
                del self.player.item_inventory[item_index]
                self.game.state = self.previous_state

    def display(self):
        print('\tInventory:\n')
        for i, item in enumerate(self.item_types):
            print(f'\t{i + 1}) (x{self.player.item_inventory.count(item)}) {item.name} - {item.description}')
        print('\n\t(Enter "exit" to go back)')

"""
========================================================================================================================
GAME OVER STATE (GAME END - PLAYER LOSES)
========================================================================================================================
"""


class GameOverState:
    def __init__(self, game):
        util.play_sound_effect('gameover_sfx.wav')
        util.play_music('gameover_song.wav')
        self.game = game

    def get_user_input(self):
        input('Enter to continue')
        self.game.reset()
        self.game.state = IntroState(self.game)

    def display(self):
        print(util.get_image('images/menu/game_over_screen.txt'))


"""
========================================================================================================================
VICTORY STATE (GAME END - PLAYER WINS)
========================================================================================================================
"""


class VictoryState:
    def __init__(self, game):
        self.game = game
        util.play_music('win_song.wav')

    def get_user_input(self):
        input('Enter to continue')
        self.game.reset()

    def display(self):
        print(util.get_image('images/menu/victory_screen.txt'))


"""
========================================================================================================================
END STATE - EXITING THE CURRENT GAME
========================================================================================================================
"""


class EndState:
    def __init__(self, game):
        self.game = game

    def get_user_input(self):
        pass

    def display(self):
        print("In end state")
