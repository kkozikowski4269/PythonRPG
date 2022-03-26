import player
from weapon import Sword, Hammer, Staff, Dagger


class PlayerFactory:
    def get(self, class_type):
        if class_type == "1":
            player_type = player.Knight()
            weapon = Sword(1)
        elif class_type == "2":
            player_type = player.Warrior()
            weapon = Hammer(1)
        elif class_type == "3":
            player_type = player.Wizard()
            weapon = Staff(1)
        elif class_type == "4":
            player_type = player.Rogue()
            weapon = Dagger(1)
        else:
            player_type = None
            weapon = None

        if weapon is not None:
            player_type.weapon = weapon
            player_type.weapon_inventory.append(weapon)
            player_type.weapon_inventory.append(Hammer(1))

        return player_type
