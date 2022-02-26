class PlayerAliveState:
    def __init__(self, player):
        self.player = player

    def check_health(self):
        if self.player.hp <= 0:
            self.player.set_state(PlayerDeadState(self.player))


class PlayerDeadState:
    def __init__(self, player):
        self.player = player

    def check_health(self):
        pass
