class EnemySpawnedState:
    def __init__(self, enemy):
        self.enemy = enemy
        self.enemy.set_icon('E')
        self.enemy.hp = self.enemy.max_hp
        self.enemy.fill_inventories()

    def check_health(self):
        if self.enemy.hp <= 0:
            self.enemy.state = EnemyUnspawnedState(self.enemy)

    def is_alive(self):
        return True


class EnemyUnspawnedState:
    def __init__(self, enemy):
        self.enemy = enemy
        self.enemy.set_icon(' ')

    def check_health(self):
        return 0

    def is_alive(self):
        return False
