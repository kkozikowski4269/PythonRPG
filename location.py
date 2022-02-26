class Location:
    def __init__(self, name):
        self.name = name
        self.starting_area = None
        self.areas = {}

    def add_area(self, new_area):
        self.areas[new_area.name] = new_area
