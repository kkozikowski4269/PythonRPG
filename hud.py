class HUD:
    def __init__(self, game):
        self.game = game
        self.location = None
        self.area = None
        self.minimap = [['  ', '  ', '  ', '  ', '  ', '  ', '  '],
                        ['  ', '  ', '  ', '  ', '  ', '  ', '  '],
                        ['  ', '  ', '  ', '  ', '  ', '  ', '  '],
                        ['  ', '  ', '  ', '  ', '  ', '  ', '  '],
                        ['  ', '  ', '  ', '  ', '  ', '  ', '  ']]

    def print_map(self):
        print('=========================================\n'
              f'|{self.location.name.center(39)}|\n'
              f'|{self.area.name.center(39)}|\n'
              '=========================================')
        for i, x in enumerate(self.minimap):
            print('|', end='')
            for y in x:
                print(y, end='')

            print('|', end='')
            if i == 0:
                print(f'  {self.game.player.name}'.ljust(24) + '|')
            elif i == 1:
                print(f'  Class: {self.game.player.type}'.ljust(24) + '|')
            elif i == 2:
                print(f'  Weapon: {self.game.player.weapon.name} ({self.game.player.weapon.power})'.ljust(24) + '|')
            elif i == 3:
                print(f'  HP: {self.game.player.hp}/{self.game.player.max_hp}'.ljust(24) + '|')
            elif i == 4:
                print(f'  Level: {self.game.player.level} xp: {self.game.player.xp}/{self.game.player.xp_to_level}'.ljust(24) + '|')
            else:
                print(''.ljust(24) + '|')
        print('=========================================\n'
              '| Move: w/a/s/d                         |\n'
              '| Pause: m                              |\n'
              '=========================================')

    def update_map(self):
        if not self.area.visited:
            x = self.area.x
            y = self.area.y
            self.minimap[y][x] = self.area.symbol
