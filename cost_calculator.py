import math
import models

def calculate_upgrade_costs(base_costs: models.Storage, level: models.Level) -> models.Storage:
    """Berechnet die Rohstoffkosten für ein Upgrade auf (level + 1)."""
    factor = 1.25 ** level.value
    resulting_costs = models.Storage(
        gold=math.floor(base_costs.gold * factor),
        stone=math.floor(base_costs.stone * factor),
        wood=math.floor(base_costs.wood * factor),
    )
    return resulting_costs

def calculate_upgrade_time(base_time_sec: int, level: models.Level, facility_level: models.Level) -> int:
    """Berechnet die Bauzeit in Sekunden für ein Upgrade auf (level + 1)."""
    facility_reduction = 1 - 0.005 * (1.25 ** facility_level.value)
    time = base_time_sec * (1.25 ** level.value) * facility_reduction
    return math.floor(time)

def calculate_production_per_hour(base_production: float, level: models.Level) -> float:
    """Berechnet die Produktion pro Stunde für ein Gebäude mit gegebener Stufe."""
    return base_production * (1.25 ** level.value)

def calculate_storage_capacity(base_capacity: int, warehouse_level: models.Level) -> int:
    """Berechnet die maximale Lagerkapazität für einen bestimmten Speicherlevel."""
    return math.floor(base_capacity * (1.25 ** warehouse_level.value))

def calculate_wait_time(current_storage: models.Storage, next_costs: models.Storage) -> int:
    """Berechnet die Wartezeit in Sekunden, bis genügend Ressourcen für ein Upgrade vorhanden sind."""
    wait_time = 0
    for resource, cost in zip(current_storage, next_costs):
        if cost > current_storage[resource]:
            wait_time += (cost - current_storage[resource]) / models.resource_production_rate[resource]
    return math.floor(wait_time)

# def calculate_upgrade_costs_and_wait_time(base_costs: models.Storage, level: models.Level, current_storage: models.Storage, base_production: models.Storage, base_time_sec: int, fortress_level: models.Level) -> tuple[models.Storage, int, models.Storage]:
#     """Berechnet die Upgrade-Kosten, die Wartezeit bis genügend Rohstoffe vorhanden sind, und die verbleibenden Ressourcen nach dem Upgrade."""
#     # Berechne die Upgrade-Kosten
#     upgrade_costs = calculate_upgrade_costs(base_costs, level)
    
#     # Berechne die Wartezeit basierend auf dem aktuellen Speicher
#     wait_time = 0
#     updated_storage = models.Storage(
#         gold=current_storage.gold,
#         stone=current_storage.stone,
#         wood=current_storage.wood
#     )
    
#     for resource in ['gold', 'stone', 'wood']:
#         if getattr(upgrade_costs, resource) > getattr(updated_storage, resource):
#             resource_wait_time = (getattr(upgrade_costs, resource) - getattr(updated_storage, resource)) / getattr(base_production, resource)
#             wait_time = max(wait_time, resource_wait_time)
    
#     # Aktualisiere die Ressourcen nach der Wartezeit
#     updated_storage = models.Storage(
#         gold=updated_storage.gold + base_production.gold * wait_time,
#         stone=updated_storage.stone + base_production.stone * wait_time,
#         wood=updated_storage.wood + base_production.wood * wait_time
#     )
    
#     # Führe das Upgrade durch und berechne die Bauzeit
#     for resource in ['gold', 'stone', 'wood']:
#         setattr(updated_storage, resource, getattr(updated_storage, resource) - getattr(upgrade_costs, resource))
    
#     upgrade_time = calculate_upgrade_time(base_time_sec, level, fortress_level)
    
#     # Aktualisiere die Ressourcen während der Bauzeit
#     updated_storage = models.Storage(
#         gold=updated_storage.gold + base_production.gold * upgrade_time,
#         stone=updated_storage.stone + base_production.stone * upgrade_time,
#         wood=updated_storage.wood + base_production.wood * upgrade_time
#     )
    
#     total_time = math.floor(wait_time + upgrade_time)
    
#     return upgrade_costs, total_time, updated_storage
    