class Door:
    def __init__(self, symbol, dest_area_symbol=None):
        self.symbol = symbol
        self.x = None
        self.y = None
        self.dest_area_symbol = dest_area_symbol

    def has_player(self, player):
        if self.x == player.x and self.y == player.y:
            return True
        return False

    def use_door(self, player):
        next_area = player.current_location.areas[self.dest_area_symbol]
        other_symbol = None
        dx = 0
        dy = 0
        # check which door is being used so the players position can properly be set in the next area
        if self.symbol == 'u':
            other_symbol = 'd'
            dy = -1
        elif self.symbol == 'd':
            other_symbol = 'u'
            dy = 1
        elif self.symbol == 'l':
            other_symbol = 'r'
            dx = -1
        elif self.symbol == 'r':
            other_symbol = 'l'
            dx = 1

        x = next_area.doors[other_symbol].x+dx
        y = next_area.doors[other_symbol].y+dy
        player.current_area = next_area
        player.set_position(x, y)

    def set_destination(self, symbol):
        self.dest_area_symbol = symbol

    def set_position(self, x, y):
        self.x = x
        self.y = y
