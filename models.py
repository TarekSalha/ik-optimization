from dataclasses import dataclass, field
from itertools import count
import enum
import sys
import params as pr

class Level(enum.Enum):
    L0 = 0
    L1 = 1
    L2 = 2
    L3 = 3
    L4 = 4
    L5 = 5
    L6 = 6
    L7 = 7
    L8 = 8
    L9 = 9
    L10 = 10
    L11 = 11
    L12 = 12
    L13 = 13
    L14 = 14
    L15 = 15
    L16 = 16
    L17 = 17
    L18 = 18
    L19 = 19
    L20 = 20

class Action(enum.Enum):
    UpgradeFortress = 0
    UpgradeGoldMine = 1
    UpgradeStoneMine = 2
    UpgradeWoodMine = 3
    UpgradeGarrison = 4
    UpgradeHarbor = 5
    UpgradeWarehouse = 6
    BuildCargoShip = 7
    BuildFrigate = 8
    BuildStoneHurler = 9

@dataclass(frozen=True)
class Storage:
    gold: int
    stone: int
    wood: int

    def __add__(self, other):
        if not isinstance(other, Storage):
            return NotImplemented
        return Storage(
            gold=self.gold + other.gold,
            stone=self.stone + other.stone,
            wood=self.wood + other.wood
        )
    
    def __sub__(self, other):
        if not isinstance(other, Storage):
            return NotImplemented
        return Storage(
            gold=self.gold - other.gold,
            stone=self.stone - other.stone,
            wood=self.wood - other.wood
        )
    
    def __eq__(self, other):
        if not isinstance(other, Storage):
            return NotImplemented
        return (
            self.gold == other.gold and
            self.stone == other.stone and
            self.wood == other.wood
        )
    
    def __repr__(self):
        return f"Storage(gold={self.gold}, stone={self.stone}, wood={self.wood})"
    
    def __hash__(self):
        return hash((self.gold, self.stone, self.wood))

@dataclass(frozen=True)
class State:
    id: int = field(default_factory=count().__next__, init=False)
    storage: Storage
    gold_mine_level: Level
    wood_mine_level: Level
    stone_mine_level: Level
    fortress_level: Level
    harbor_level: Level
    garrison_level: Level
    warehouse_level: Level
    num_frigates: int
    num_cargo_ships: int
    num_stone_hurler: int
    current_duration: int
    
    @property
    def is_final_state(self) -> bool:
        return (
            self.num_stone_hurler >= pr.max_number_stone_hurler and
            self.num_frigates >= 1 and
            self.num_cargo_ships >= 1
        )
