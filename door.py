class Door:
    """
    symbol (u,l,d,r) indicates which direction the door is going
    dest_area_code indicates the code of the area the door attaches to
    """

    def __init__(self, symbol, dest_area_code=None):
        self.symbol = symbol
        self.x = None
        self.y = None
        self.dest_area_code = dest_area_code

    def has_player(self, player):
        if self.x == player.x and self.y == player.y:
            return True
        return False

    def use_door(self, player):
        next_area = player.current_location.areas[self.dest_area_code]
        other_symbol = None
        dx = 0
        dy = 0
        # check which door is being used so the players position can properly be set in the next area
        # ie if player goes through a door going up then they will be placed in the next area next to the
        # door going down in that area
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

        # set player's position in the next area
        x = next_area.doors[other_symbol].x + dx
        y = next_area.doors[other_symbol].y + dy
        player.current_area = next_area
        player.set_position(x, y)

    def set_destination(self, dest_area_code):
        self.dest_area_code = dest_area_code

    def set_position(self, x, y):
        self.x = x
        self.y = y
