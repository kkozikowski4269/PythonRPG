import player


class PlayerFactory:
    def get(self, class_type):
        if class_type == "1":
            player_type = player.Knight()
        elif class_type == "2":
            player_type = player.Warrior()
        elif class_type == "3":
            player_type = player.Wizard()
        elif class_type == "4":
            player_type = player.Rogue()
        else:
            player_type = None

        return player_type
