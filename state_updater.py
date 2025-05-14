import models as md
import params as pr
from cost_calculator import calculate_added_production_while_operation, calculate_storage_capacity, calculate_upgrade_costs, calculate_upgrade_time, calculate_wait_time

def mine_diff_is_in_range(state: md.State) -> bool:
    """Checks if the difference between the highest and lowest mine levels is within the allowed range."""
    return (max(state.gold_mine_level.value, state.stone_mine_level.value, state.wood_mine_level.value) - min(state.gold_mine_level.value, state.stone_mine_level.value, state.wood_mine_level.value)) < pr.max_diff_level_mines

def is_finished_with_mines(state: md.State) -> bool:
    """Checks if the mines are finished based on the current levels of garrison, fortress, and harbor."""
    return state.garrison_level.value >= 1 or state.fortress_level.value >= 2 or state.harbor_level.value >= 1

def enough_storage_available_for_upgrade(state: md.State, costs: md.Storage) -> bool:
    """Checks if there is enough storage available for the upgrade costs."""
    max_storage_capacity = calculate_storage_capacity(state.warehouse_level)
    return (
        costs.gold <= max_storage_capacity and
        costs.stone <= max_storage_capacity and
        costs.wood <= max_storage_capacity
    )

##### --- Strategy Functions --- #####

### Units
# Cargo Ship
def is_possible_build_cargo_ship(state: md.State) -> bool:
    """Checks if the construction of a cargo ship is possible."""
    return (
        enough_storage_available_for_upgrade(state, md.Storage(pr.base_costs_cargo_ship_gold, pr.base_costs_cargo_ship_stone, pr.base_costs_cargo_ship_wood)) and
        state.harbor_level.value >= 1 and
        state.num_cargo_ships < 1 #and
        #state.num_stone_hurler >= pr.max_number_stone_hurler
    )

def update_state_build_cargo_ship(state: md.State) -> md.State:
    """Updates the state after building a cargo ship."""
    base_costs = md.Storage(pr.base_costs_cargo_ship_gold, pr.base_costs_cargo_ship_stone, pr.base_costs_cargo_ship_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=md.Level.L0)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_cargo_ship, level=md.Level.L0, facility_level=state.harbor_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=state.wood_mine_level,
        fortress_level=state.fortress_level,
        harbor_level=state.harbor_level,
        garrison_level=state.garrison_level,
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships + 1,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

# Frigate
def is_possible_build_frigate(state: md.State) -> bool:
    """Checks if the construction of a frigate is possible."""
    return (
        enough_storage_available_for_upgrade(state, md.Storage(pr.base_costs_fregate_gold, pr.base_costs_fregate_stone, pr.base_costs_fregate_wood)) and
        state.harbor_level.value >= 1 and
        state.num_frigates < 1 and
        state.num_cargo_ships >= 1 #and
        #state.num_stone_hurler >= pr.max_number_stone_hurler
    )

def update_state_build_frigate(state: md.State) -> md.State:
    """Updates the state after building a frigate."""
    base_costs = md.Storage(pr.base_costs_fregate_gold, pr.base_costs_fregate_stone, pr.base_costs_fregate_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=md.Level.L0)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_fregate, level=md.Level.L0, facility_level=state.harbor_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=state.wood_mine_level,
        fortress_level=state.fortress_level,
        harbor_level=state.harbor_level,
        garrison_level=state.garrison_level,
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates + 1,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

# Stone Hurler
def is_possible_build_stone_hurler(state: md.State) -> bool:
    """Checks if the construction of a stone hurler is possible."""
    return (
        enough_storage_available_for_upgrade(state, md.Storage(pr.base_costs_stone_hurler_gold, pr.base_costs_stone_hurler_stone, pr.base_costs_stone_hurler_wood)) and
        state.garrison_level.value >= 1 and
        state.num_stone_hurler < pr.max_number_stone_hurler
    )

def update_state_build_stone_hurler(state: md.State) -> md.State:
    """Updates the state after building a stone hurler."""
    base_costs = md.Storage(pr.base_costs_stone_hurler_gold, pr.base_costs_stone_hurler_stone, pr.base_costs_stone_hurler_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=md.Level.L0)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_stone_hurler, level=md.Level.L0, facility_level=state.garrison_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=state.wood_mine_level,
        fortress_level=state.fortress_level,
        harbor_level=state.harbor_level,
        garrison_level=state.garrison_level,
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler + 1,
        current_duration=new_duration
    )

### Mines
# Gold Mine
def is_possible_upgrade_gold_mine(state: md.State) -> bool:
    """Checks if the upgrade to the gold mine is possible."""
    return (
        enough_storage_available_for_upgrade(state, calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_gold_mine_gold, pr.base_costs_gold_mine_stone, pr.base_costs_gold_mine_wood), level=state.gold_mine_level)) and
        state.fortress_level.value >= 1 and
        state.gold_mine_level.value < pr.max_level_mines and
        not is_finished_with_mines(state) and
        mine_diff_is_in_range(state)
    )

def update_state_upgrade_gold_mine(state: md.State) -> md.State:
    """Updates the state after upgrading the gold mine."""
    base_costs = md.Storage(pr.base_costs_gold_mine_gold, pr.base_costs_gold_mine_stone, pr.base_costs_gold_mine_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=state.gold_mine_level)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_gold_mine, level=state.gold_mine_level, facility_level=state.fortress_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=md.Level(state.gold_mine_level.value + 1),
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=state.wood_mine_level,
        fortress_level=state.fortress_level,
        harbor_level=state.harbor_level,
        garrison_level=state.garrison_level,
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

# Stone Mine
def is_possible_upgrade_stone_mine(state: md.State) -> bool:
    """Checks if the upgrade to the stone mine is possible."""
    return (
        enough_storage_available_for_upgrade(state, calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_stone_mine_gold, pr.base_costs_stone_mine_stone, pr.base_costs_stone_mine_wood), level=state.stone_mine_level)) and
        state.fortress_level.value >= 1 and
        state.stone_mine_level.value < pr.max_level_mines and
        not is_finished_with_mines(state) and
        mine_diff_is_in_range(state)
    )

def update_state_upgrade_stone_mine(state: md.State) -> md.State:
    """Updates the state after upgrading the stone mine."""
    base_costs = md.Storage(pr.base_costs_stone_mine_gold, pr.base_costs_stone_mine_stone, pr.base_costs_stone_mine_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=state.stone_mine_level)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_stone_mine, level=state.stone_mine_level, facility_level=state.fortress_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=md.Level(state.stone_mine_level.value + 1),
        wood_mine_level=state.wood_mine_level,
        fortress_level=state.fortress_level,
        harbor_level=state.harbor_level,
        garrison_level=state.garrison_level,
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

# Wood Mine
def is_possible_upgrade_wood_mine(state: md.State) -> bool:
    """Checks if the upgrade to the wood mine is possible."""
    return (
        enough_storage_available_for_upgrade(state, calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_wood_mine_gold, pr.base_costs_wood_mine_stone, pr.base_costs_wood_mine_wood), level=state.wood_mine_level)) and
        state.fortress_level.value >= 1 and
        state.wood_mine_level.value < pr.max_level_mines and
        not is_finished_with_mines(state) and
        mine_diff_is_in_range(state)
    )

def update_state_upgrade_wood_mine(state: md.State) -> md.State:
    """Updates the state after upgrading the wood mine."""
    base_costs = md.Storage(pr.base_costs_wood_mine_gold, pr.base_costs_wood_mine_stone, pr.base_costs_wood_mine_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=state.wood_mine_level)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_wood_mine, level=state.wood_mine_level, facility_level=state.fortress_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=md.Level(state.wood_mine_level.value + 1),
        fortress_level=state.fortress_level,
        harbor_level=state.harbor_level,
        garrison_level=state.garrison_level,
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

### Facilities
# Fortress
def is_possible_upgrade_fortress(state: md.State) -> bool:
    """Checks if the upgrade to the fortress is possible."""
    return (
        enough_storage_available_for_upgrade(state, calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_fortress_gold, pr.base_costs_fortress_stone, pr.base_costs_fortress_wood), level=state.fortress_level)) and
        state.fortress_level.value < 5 and
        is_finished_with_mines(state)
    )

def update_state_upgrade_fortress(state: md.State) -> md.State:
    """Updates the state after upgrading the fortress."""
    base_costs = md.Storage(pr.base_costs_fortress_gold, pr.base_costs_fortress_stone, pr.base_costs_fortress_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=state.fortress_level)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_fortress, level=state.fortress_level, facility_level=state.fortress_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=state.wood_mine_level,
        fortress_level=md.Level(state.fortress_level.value + 1),
        harbor_level=state.harbor_level,
        garrison_level=state.garrison_level,
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

# Garrison
def is_possible_upgrade_garrison(state: md.State) -> bool:
    """Checks if the upgrade to the garrison is possible."""
    return (
        enough_storage_available_for_upgrade(state, calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_garrison_gold, pr.base_costs_garrison_stone, pr.base_costs_garrison_wood), level=state.garrison_level)) and
        state.fortress_level.value >= 1 and
        state.garrison_level.value < 1
    )

def update_state_upgrade_garrison(state: md.State) -> md.State:
    """Updates the state after upgrading the garrison."""
    base_costs = md.Storage(pr.base_costs_garrison_gold, pr.base_costs_garrison_stone, pr.base_costs_garrison_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=state.garrison_level)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_garrison, level=state.garrison_level, facility_level=state.fortress_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=state.wood_mine_level,
        fortress_level=state.fortress_level,
        harbor_level=state.harbor_level,
        garrison_level=md.Level(state.garrison_level.value + 1),
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

# Harbor
def is_possible_upgrade_harbor(state: md.State) -> bool:
    """Checks if the upgrade to the harbor is possible."""
    return (
        enough_storage_available_for_upgrade(state, calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_harbor_gold, pr.base_costs_harbor_stone, pr.base_costs_harbor_wood), level=state.harbor_level)) and
        state.fortress_level.value >= 5 and
        state.harbor_level.value < 1
    )

def update_state_upgrade_harbor(state: md.State) -> md.State:
    """Updates the state after upgrading the harbor."""
    base_costs = md.Storage(pr.base_costs_harbor_gold, pr.base_costs_harbor_stone, pr.base_costs_harbor_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=state.harbor_level)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_harbor, level=state.harbor_level, facility_level=state.fortress_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=state.wood_mine_level,
        fortress_level=state.fortress_level,
        harbor_level=md.Level(state.harbor_level.value + 1),
        garrison_level=state.garrison_level,
        warehouse_level=state.warehouse_level,
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

# Warehouse
def is_possible_upgrade_warehouse(state: md.State) -> bool:
    """Checks if the upgrade to the warehouse is possible."""
    max_storage_capacity = calculate_storage_capacity(state.warehouse_level)
    costs_stone_hurler = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_stone_hurler_gold, pr.base_costs_stone_hurler_stone, pr.base_costs_stone_hurler_wood), level=md.Level.L0)
    costs_frigate = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_fregate_gold, pr.base_costs_fregate_stone, pr.base_costs_fregate_wood), level=md.Level.L0)
    costs_cargo_ship = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_cargo_ship_gold, pr.base_costs_cargo_ship_stone, pr.base_costs_cargo_ship_wood), level=md.Level.L0)
    costs_gold_mine = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_gold_mine_gold, pr.base_costs_gold_mine_stone, pr.base_costs_gold_mine_wood), level=state.gold_mine_level)
    costs_stone_mine = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_stone_mine_gold, pr.base_costs_stone_mine_stone, pr.base_costs_stone_mine_wood), level=state.stone_mine_level)
    costs_wood_mine = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_wood_mine_gold, pr.base_costs_wood_mine_stone, pr.base_costs_wood_mine_wood), level=state.wood_mine_level)
    costs_fortress = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_fortress_gold, pr.base_costs_fortress_stone, pr.base_costs_fortress_wood), level=state.fortress_level)
    costs_garrison = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_garrison_gold, pr.base_costs_garrison_stone, pr.base_costs_garrison_wood), level=state.garrison_level)
    costs_harbor = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_harbor_gold, pr.base_costs_harbor_stone, pr.base_costs_harbor_wood), level=state.harbor_level)
    costs_warehouse = calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_warehouse_gold, pr.base_costs_warehouse_stone, pr.base_costs_warehouse_wood), level=state.warehouse_level)
    any_costs_are_above_capacity = max(
        costs_stone_hurler.gold,
        costs_frigate.gold,
        costs_cargo_ship.gold,
        costs_gold_mine.gold,
        costs_stone_mine.gold,
        costs_wood_mine.gold,
        costs_fortress.gold,
        costs_garrison.gold,
        costs_harbor.gold,
        costs_warehouse.gold
    ) > max_storage_capacity or max(
        costs_stone_hurler.stone,
        costs_frigate.stone,
        costs_cargo_ship.stone,
        costs_gold_mine.stone,
        costs_stone_mine.stone,
        costs_wood_mine.stone,
        costs_fortress.stone,
        costs_garrison.stone,
        costs_harbor.stone,
        costs_warehouse.stone
    ) > max_storage_capacity or max(
        costs_stone_hurler.wood,
        costs_frigate.wood,
        costs_cargo_ship.wood,
        costs_gold_mine.wood,
        costs_stone_mine.wood,
        costs_wood_mine.wood,
        costs_fortress.wood,
        costs_garrison.wood,
        costs_harbor.wood,
        costs_warehouse.wood
    ) > max_storage_capacity

    return (
        enough_storage_available_for_upgrade(state, calculate_upgrade_costs(base_costs=md.Storage(pr.base_costs_warehouse_gold, pr.base_costs_warehouse_stone, pr.base_costs_warehouse_wood), level=state.warehouse_level)) and
        state.fortress_level.value >= 1 and
        state.warehouse_level.value < pr.max_level_warehouse and
        any_costs_are_above_capacity
    )

def update_state_upgrade_warehouse(state: md.State) -> md.State:
    """Updates the state after upgrading the warehouse."""
    base_costs = md.Storage(pr.base_costs_warehouse_gold, pr.base_costs_warehouse_stone, pr.base_costs_warehouse_wood)
    upgrade_costs = calculate_upgrade_costs(base_costs=base_costs, level=state.warehouse_level)
    upgrade_time = calculate_upgrade_time(base_time_sec=pr.base_time_warehouse, level=state.warehouse_level, facility_level=state.fortress_level)
    added_production = calculate_added_production_while_operation(state, upgrade_time)
    wait_time = calculate_wait_time(state, upgrade_costs)
    added_wait_production = calculate_added_production_while_operation(state, wait_time)
    new_duration = state.current_duration + upgrade_time + wait_time
    new_storage = state.storage - upgrade_costs + added_production + added_wait_production
    capped_storage = md.Storage(
        gold=min(new_storage.gold, calculate_storage_capacity(state.warehouse_level)),
        stone=min(new_storage.stone, calculate_storage_capacity(state.warehouse_level)),
        wood=min(new_storage.wood, calculate_storage_capacity(state.warehouse_level))
    )

    return md.State(
        storage=capped_storage,
        gold_mine_level=state.gold_mine_level,
        stone_mine_level=state.stone_mine_level,
        wood_mine_level=state.wood_mine_level,
        fortress_level=state.fortress_level,
        harbor_level=state.harbor_level,
        garrison_level=state.garrison_level,
        warehouse_level=md.Level(state.warehouse_level.value + 1),
        num_frigates=state.num_frigates,
        num_cargo_ships=state.num_cargo_ships,
        num_stone_hurler=state.num_stone_hurler,
        current_duration=new_duration
    )

### General
def is_possible_action(state: md.State, action: md.Action) -> bool:
    """Checks if the action is possible in the given state."""
    strategy = ACTION_STRATEGIES.get(action)
    if not strategy:
        raise ValueError(f"No strategy found for action: {action.name}")
    return strategy["is_possible"](state)

def update_state(state: md.State, action: md.Action) -> md.State:
    """Updates the state based on the action taken."""
    strategy = ACTION_STRATEGIES.get(action)
    if not strategy:
        raise ValueError(f"No strategy found for action: {action.name}")
    return strategy["update_state"](state)

# Define the action strategies in a dictionary for easy access
ACTION_STRATEGIES = {
        md.Action.BuildCargoShip: {
            "is_possible": is_possible_build_cargo_ship,
            "update_state": update_state_build_cargo_ship
        },
        md.Action.BuildFrigate: {
            "is_possible": is_possible_build_frigate,
            "update_state": update_state_build_frigate
        },
        md.Action.BuildStoneHurler: {
            "is_possible": is_possible_build_stone_hurler,
            "update_state": update_state_build_stone_hurler
        },
        md.Action.UpgradeGoldMine: {
            "is_possible": is_possible_upgrade_gold_mine,
            "update_state": update_state_upgrade_gold_mine
        },
        md.Action.UpgradeStoneMine: {
            "is_possible": is_possible_upgrade_stone_mine,
            "update_state": update_state_upgrade_stone_mine
        },
        md.Action.UpgradeWoodMine: {
            "is_possible": is_possible_upgrade_wood_mine,
            "update_state": update_state_upgrade_wood_mine
        },
        md.Action.UpgradeFortress: {
            "is_possible": is_possible_upgrade_fortress,
            "update_state": update_state_upgrade_fortress
        },
        md.Action.UpgradeGarrison: {
            "is_possible": is_possible_upgrade_garrison,
            "update_state": update_state_upgrade_garrison
        },
        md.Action.UpgradeHarbor: {
            "is_possible": is_possible_upgrade_harbor,
            "update_state": update_state_upgrade_harbor
        },
        md.Action.UpgradeWarehouse: {
            "is_possible": is_possible_upgrade_warehouse,
            "update_state": update_state_upgrade_warehouse
        }
    }