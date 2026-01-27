# models/shelter.py

class Shelter:
    def __init__(self, name: str, capacity: int, current_ppl: int):
        self.name = name
        self.capacity = capacity
        self.current_ppl = current_ppl

    @property
    def load_percentage(self) -> float:
        """計算負載比，確保不會除以零"""
        if self.capacity <= 0:
            return 0.0
        return self.current_ppl / self.capacity