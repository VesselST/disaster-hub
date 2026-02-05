#初始化shelter物件
class Shelter:
    def __init__(self, name, total_vessel, total_people, lon, lat):
        self.name = name
        self.total_vessel = total_vessel
        self.total_people = total_people
        self.lon = lon
        self.lat = lat