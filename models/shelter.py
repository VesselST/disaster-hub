class Shelter:
    def __init__(self, name: str, capacity: int, current_ppl: int, lat: float = 0.0, lon: float = 0.0):
        self.name = name
        self.capacity = capacity
        self.current_ppl = current_ppl
        self.lat = lat
        self.lon = lon

    @property
    def load_percentage(self) -> float:
        if self.capacity <= 0:
            return 0.0
        return (self.current_ppl / self.capacity) * 100
