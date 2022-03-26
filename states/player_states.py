class PlayerAliveState:
    def __init__(self, player):
        self.player = player

    def check_health(self):
        if self.player.hp <= 0:
            self.player.state = PlayerDeadState(self.player)

    def is_alive(self):
        return True


class PlayerDeadState:
    def __init__(self, player):
        self.player = player

    def check_health(self):
        return 0

    def is_alive(self):
        return False

