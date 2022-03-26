import player
from weapon import Sword, Hammer, Staff, Dagger


class PlayerFactory:
    def get(self, class_type):
        if class_type == "1":
            player_type = player.Knight()
            weapon = Sword()
        elif class_type == "2":
            player_type = player.Warrior()
            weapon = Hammer()
        elif class_type == "3":
            player_type = player.Wizard()
            weapon = Staff()
        elif class_type == "4":
            player_type = player.Rogue()
            weapon = Dagger()
        else:
            player_type = None
            weapon = None

        if weapon is not None:
            weapon.level = 1
            player_type.weapon = weapon
            player_type.weapon_inventory.append(weapon)

        return player_type
