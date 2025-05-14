import logging
import sys

class GlobalStateManager:
    _instance = None
    _lowest_known_duration:int = sys.maxsize

    @classmethod
    def get_global_state(cls) -> 'GlobalStateManager':
        """Singleton method to get the global state manager instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def update_lowest_known_duration(self, duration:int) -> None:
        """Update the lowest known duration if the new duration is lower."""
        if duration < self._lowest_known_duration:
            logging.debug(f"Updating lowest known duration from {self._lowest_known_duration} to {duration}")
            self._lowest_known_duration = duration

    def get_lowest_known_duration(self) -> int:
        """Get the lowest known duration."""
        return self._lowest_known_duration