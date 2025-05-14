import math
import models as md
import params as pr

def calculate_upgrade_costs(base_costs: md.Storage, level: md.Level) -> md.Storage:
    """Berechnet die Rohstoffkosten für ein Upgrade auf (level + 1)."""
    factor = 1.25 ** level.value
    resulting_costs = md.Storage(
        gold=math.floor(base_costs.gold * factor),
        stone=math.floor(base_costs.stone * factor),
        wood=math.floor(base_costs.wood * factor),
    )
    return resulting_costs

def calculate_upgrade_time(base_time_sec: int, level: md.Level, facility_level: md.Level) -> int:
    """Berechnet die Bauzeit in Sekunden für ein Upgrade auf (level + 1)."""
    facility_reduction = 1 - 0.005 * (1.25 ** facility_level.value)
    time = base_time_sec * (1.25 ** level.value) * facility_reduction
    return math.floor(time)

def calculate_production_per_hour(base_production: float, level: md.Level) -> float:
    """Berechnet die Produktion pro Stunde für ein Gebäude mit gegebener Stufe."""
    return base_production * (1.25 ** level.value)

def calculate_storage_capacity(warehouse_level: md.Level) -> int:
    """Berechnet die maximale Lagerkapazität für einen bestimmten Speicherlevel."""
    return math.floor(pr.initial_warehouse_capacity * (1.25 ** warehouse_level.value))

def calculate_added_production_while_operation(state: md.State, operation_time: int) -> md.Storage:
    """Berechnet die zusätzlichen Ressourcen, die während des Upgrades oder währnd des Wartens produziert werden."""
    return md.Storage(
        gold = int(calculate_production_per_hour(base_production=pr.initial_rate_gold, level=state.gold_mine_level) * operation_time // 3600),
        stone = int(calculate_production_per_hour(base_production=pr.initial_rate_stone, level=state.stone_mine_level) * operation_time // 3600),
        wood = int(calculate_production_per_hour(base_production=pr.initial_rate_wood, level=state.wood_mine_level) * operation_time // 3600)
    )

def calculate_wait_time(current_state: md.State, next_costs: md.Storage) -> int:
    """Berechnet die Wartezeit in Sekunden, bis genügend Ressourcen für ein Upgrade vorhanden sind."""
    if next_costs <= current_state.storage:
        return 0
    else:
        production_time_missing_gold = (next_costs.gold - current_state.storage.gold)/calculate_production_per_hour(base_production=pr.initial_rate_gold, level=current_state.gold_mine_level) * 3600
        production_time_missing_stone = (next_costs.stone - current_state.storage.stone)/calculate_production_per_hour(base_production=pr.initial_rate_stone, level=current_state.stone_mine_level) * 3600
        production_time_missing_wood = (next_costs.wood - current_state.storage.wood)/calculate_production_per_hour(base_production=pr.initial_rate_wood, level=current_state.wood_mine_level) * 3600
        wait_time = max(production_time_missing_gold, production_time_missing_stone, production_time_missing_wood)
    return math.floor(wait_time)
