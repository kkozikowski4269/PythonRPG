

class Area:
    DOORS = ('u', 'r', 'd', 'l')

    def __init__(self, area_json):
        self.width = area_json['x']
        self.height = area_json['y']
        self.name = area_json['name']
        self.image_path = area_json['image']
        self.layout = []
        self.create_area()

    def __str__(self):
        return "Area: " + self.name

    def create_area(self):
        with open(self.image_path, "r", encoding='utf-8') as file:
            for line in file.readlines():
                row = []
                for c in line:
                    if c in Area.DOORS:
                        c = ' '
                    if c != '\n':
                        row.append(c)
                self.layout.append(row)

    def print_area(self):
        for row in self.layout:
            print(*row, sep="")
