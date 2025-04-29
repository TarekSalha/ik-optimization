import models as md
import params as pr
from cost_calculator import calculate_upgrade_costs

def is_possible_action(state: md.State, action: md.Action) -> bool:
    is_finished_with_mines = state.garrison_level.value >= 1 or state.fortress_level.value >= 2 or state.harbor_level.value >= 1
    is_finished_with_facilities = state.garrison_level.value >= 1 and state.fortress_level.value >= 5 and state.harbor_level.value >= 1
    mine_diff_is_in_range = (max(state.gold_mine_level.value, state.stone_mine_level.value, state.wood_mine_level.value) - min(state.gold_mine_level.value, state.stone_mine_level.value, state.wood_mine_level.value)) < 3

    # units
    if action == md.Action.BuildCargoShip:
        return state.fortress_level.value >= 5 and state.harbor_level.value >= 1 and state.num_cargo_ships < 1 and is_finished_with_mines and is_finished_with_facilities and state.num_stone_hurler >= pr.max_number_stone_hurler
    if action == md.Action.BuildFrigate:
        return state.fortress_level.value >= 5 and state.harbor_level.value >= 1 and state.num_frigates < 1 and is_finished_with_mines and is_finished_with_facilities and state.num_cargo_ships >= 1 and state.num_stone_hurler >= pr.max_number_stone_hurler
    if action == md.Action.BuildStoneHurler:
        return state.fortress_level.value >= 1 and state.garrison_level.value >= 1 and state.num_stone_hurler < pr.max_number_stone_hurler and is_finished_with_mines and is_finished_with_facilities
    
    # mines
    if action == md.Action.UpgradeGoldMine:
        return state.fortress_level.value >= 1 and state.gold_mine_level.value < pr.max_level_mines and not is_finished_with_mines and mine_diff_is_in_range
    if action == md.Action.UpgradeStoneMine:
        return state.fortress_level.value >= 1 and state.stone_mine_level.value < pr.max_level_mines and not is_finished_with_mines and mine_diff_is_in_range
    if action == md.Action.UpgradeWoodMine:
        return state.fortress_level.value >= 1 and state.wood_mine_level.value < pr.max_level_mines and not is_finished_with_mines and mine_diff_is_in_range
    
    # facilities
    if action == md.Action.UpgradeFortress:
        return state.fortress_level.value < 5 and is_finished_with_mines
    if action == md.Action.UpgradeGarrison:
        return state.fortress_level.value >= 1 and state.garrison_level.value < 1
    if action == md.Action.UpgradeHarbour: 
        return state.fortress_level.value >= 5 and state.harbor_level.value < 1
    if action == md.Action.UpgradeWarehouse:
        return state.fortress_level.value >= 1 and state.warehouse_level.value < 0

def update_storage(storage: md.Storage, required_resources: md.Storage) -> md.Storage:
    return md.Storage(
        gold = storage.gold - required_resources.gold,
        stone = storage.stone - required_resources.stone,
        wood = storage.wood - required_resources.wood
    )

# def calculate_wait_time(state: State, action: Action, params: GameParameters) -> int:
#     gold_rate = params.prod_gold * (1 + 0.1 * state.gold_mine_level)
#     wood_rate = params.prod_wood * (1 + 0.1 * state.wood_mine_level)
#     stone_rate = params.prod_stone * (1 + 0.1 * state.stone_mine_level)

#     gold_needed = max(action.required_gold - state.gold, 0)
#     wood_needed = max(action.required_wood - state.wood, 0)
#     stone_needed = max(action.required_stone - state.stone, 0)

#     time_gold = gold_needed / max(gold_rate, 1e-6)
#     time_wood = wood_needed / max(wood_rate, 1e-6)
#     time_stone = stone_needed / max(stone_rate, 1e-6)

#     wait_time = max(time_gold, time_wood, time_stone)

#     return int(wait_time)

def update_state(state: md.State, action: md.Action) -> md.State:
    base_costs_fortress = md.Storage(pr.base_costs_fortress_gold, pr.base_costs_fortress_stone, pr.base_costs_fortress_wood)
    base_costs_garrison = md.Storage(pr.base_costs_garrison_gold, pr.base_costs_garrison_stone, pr.base_costs_garrison_wood)
    base_costs_warehouse = md.Storage(pr.base_costs_warehouse_gold, pr.base_costs_warehouse_stone, pr.base_costs_warehouse_wood)
    base_costs_harbour = md.Storage(pr.base_costs_harbour_gold, pr.base_costs_harbour_stone, pr.base_costs_harbour_wood)
    base_costs_goldmine = md.Storage(pr.base_costs_goldmine_gold, pr.base_costs_goldmine_stone, pr.base_costs_goldmine_wood)
    base_costs_stonemine = md.Storage(pr.base_costs_stonemine_gold, pr.base_costs_stonemine_stone, pr.base_costs_stonemine_wood)
    base_costs_woodmine = md.Storage(pr.base_costs_woodmine_gold, pr.base_costs_woodmine_stone, pr.base_costs_woodmine_wood)
    base_costs_stone_hurler = md.Storage(pr.base_costs_stone_hurler_gold, pr.base_costs_stone_hurler_stone, pr.base_costs_stone_hurler_wood)
    base_costs_fregate = md.Storage(pr.base_costs_fregate_gold, pr.base_costs_fregate_stone, pr.base_costs_fregate_wood)
    base_costs_cargo_ship = md.Storage(pr.base_costs_cargo_ship_gold, pr.base_costs_cargo_ship_stone, pr.base_costs_cargo_ship_wood)

    if action == md.Action.UpgradeFortress:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_fortress, level=state.fortress_level)),
            gold_mine_level=state.gold_mine_level,
            wood_mine_level=state.wood_mine_level,
            stone_mine_level=state.stone_mine_level,
            fortress_level=md.Level(state.fortress_level.value + 1),
            harbor_level=state.harbor_level,
            garrison_level=state.garrison_level,
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.UpgradeGarrison:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_garrison, level=state.garrison_level)),
            gold_mine_level=state.gold_mine_level,
            stone_mine_level=state.stone_mine_level,
            wood_mine_level=state.wood_mine_level,
            fortress_level=state.fortress_level,
            harbor_level=state.harbor_level,
            garrison_level=md.Level(state.garrison_level.value + 1),
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.UpgradeGoldMine:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_goldmine, level=state.gold_mine_level)),
            gold_mine_level=md.Level(state.gold_mine_level.value + 1),
            stone_mine_level=state.stone_mine_level,
            wood_mine_level=state.wood_mine_level,
            fortress_level=state.fortress_level,
            harbor_level=state.harbor_level,
            garrison_level=state.garrison_level,
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.UpgradeStoneMine:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_stonemine, level=state.stone_mine_level)),
            gold_mine_level=state.gold_mine_level,
            stone_mine_level=md.Level(state.stone_mine_level.value + 1),
            wood_mine_level=state.wood_mine_level,
            fortress_level=state.fortress_level,
            harbor_level=state.harbor_level,
            garrison_level=state.garrison_level,
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.UpgradeWoodMine:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_woodmine, level=state.wood_mine_level)),
            gold_mine_level=state.gold_mine_level,
            stone_mine_level=state.stone_mine_level,
            wood_mine_level=md.Level(state.wood_mine_level.value + 1),
            fortress_level=state.fortress_level,
            harbor_level=state.harbor_level,
            garrison_level=state.garrison_level,
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.UpgradeHarbour:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_harbour, level=state.harbor_level)),
            gold_mine_level=state.gold_mine_level,
            stone_mine_level=state.stone_mine_level,
            wood_mine_level=state.wood_mine_level,
            fortress_level=state.fortress_level,
            harbor_level=md.Level(state.harbor_level.value + 1),
            garrison_level=state.garrison_level,
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.UpgradeWarehouse:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_warehouse, level=state.warehouse_level)),
            gold_mine_level=state.gold_mine_level,
            stone_mine_level=state.stone_mine_level,
            wood_mine_level=state.wood_mine_level,
            fortress_level=state.fortress_level,
            harbor_level=state.harbor_level,
            garrison_level=state.garrison_level,
            warehouse_level=md.Level(state.warehouse_level.value + 1),
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.BuildCargoShip:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_cargo_ship, level=md.Level.L0)),
            gold_mine_level=state.gold_mine_level,
            stone_mine_level=state.stone_mine_level,
            wood_mine_level=state.wood_mine_level,
            fortress_level=state.fortress_level,
            harbor_level=state.harbor_level,
            garrison_level=state.garrison_level,
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships + 1,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.BuildFrigate:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_fregate, level=md.Level.L0)),
            gold_mine_level=state.gold_mine_level,
            stone_mine_level=state.stone_mine_level,
            wood_mine_level=state.wood_mine_level,
            fortress_level=state.fortress_level,
            harbor_level=state.harbor_level,
            garrison_level=state.garrison_level,
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates + 1,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler
        )
    
    if action == md.Action.BuildStoneHurler:
        return md.State(
            storage=update_storage(state.storage, calculate_upgrade_costs(base_costs=base_costs_stone_hurler, level=md.Level.L0)),
            gold_mine_level=state.gold_mine_level,
            stone_mine_level=state.stone_mine_level,
            wood_mine_level=state.wood_mine_level,
            fortress_level=state.fortress_level,
            harbor_level=state.harbor_level,
            garrison_level=state.garrison_level,
            warehouse_level=state.warehouse_level,
            num_frigates=state.num_frigates,
            num_cargo_ships=state.num_cargo_ships,
            num_stone_hurler=state.num_stone_hurler + 1
        )
    
    return state