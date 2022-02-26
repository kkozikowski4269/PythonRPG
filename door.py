class Door:
    def __init__(self, src_area, dest_area):
        self.src_area = src_area
        self.dest_area = dest_area

    def use_door(self, player):
        player.set_area(self.dest_area)