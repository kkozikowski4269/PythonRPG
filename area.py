from door import Door


class Area:
    WALLS = [chr(c) for c in range(0x2550, 0x256C+1)]
    DOOR_SYMBOLS = ('u', 'r', 'd', 'l')

    def __init__(self, area_json):
        self.width = area_json['x']
        self.height = area_json['y']
        self.name = area_json['name']
        self.code = area_json['code']
        self.image_path = area_json['image']
        self.layout = []
        self.doors = {}

    def __str__(self):
        return "Area: " + self.name

    def create_area(self):
        with open(self.image_path, "r", encoding='utf-8') as file:
            for y, line in enumerate(file.readlines()):
                row = []
                for x, c in enumerate(line):
                    if c in Area.DOOR_SYMBOLS:
                        self.doors[c].set_position(x, y)
                        c = ' '
                    if c != '\n':
                        row.append(c)
                self.layout.append(row)

    def check_doors(self, player):
        for door in self.doors.values():
            if door.has_player(player):
                player.clear_position()
                door.use_door(player)

    def print_area(self):
        for row in self.layout:
            print(*row, sep="")
