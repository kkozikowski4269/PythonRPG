class EnemySpawnedState:
    def __init__(self, enemy):
        self.enemy = enemy
        self.enemy.set_icon('E')

    def check_health(self):
        if self.enemy.hp <= 0:
            self.enemy.set_state(EnemyUnspawnedState(self.enemy))


class EnemyUnspawnedState:
    def __init__(self, enemy):
        self.enemy = enemy
        self.enemy.set_icon(' ')

    def check_health(self):
        pass