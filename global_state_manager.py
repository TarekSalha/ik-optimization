import sys

class GlobalStateManager:
    _instance = None
    _lowest_known_duration:int = sys.maxsize

    @classmethod
    def get_global_state(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def update_lowest_known_duration(self, duration:int):
        self._lowest_known_duration = duration

    def get_lowest_known_duration(self):
        return self._lowest_known_duration