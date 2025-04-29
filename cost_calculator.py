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

def calculate_upgrade_time(base_time_sec: int, level: models.Level, fortress_level: models.Level) -> int:
    """Berechnet die Bauzeit in Sekunden für ein Upgrade auf (level + 1)."""
    fortress_reduction = 1 - 0.005 * (1.25 ** fortress_level.value)
    time = base_time_sec * (1.25 ** level.value) * fortress_reduction
    return math.floor(time)

def calculate_production_per_hour(base_production: float, level: models.Level) -> float:
    """Berechnet die Produktion pro Stunde für ein Gebäude mit gegebener Stufe."""
    return base_production * (1.25 ** level.value)

def calculate_storage_capacity(base_capacity: int, warehouse_level: models.Level) -> int:
    """Berechnet die maximale Lagerkapazität für einen bestimmten Speicherlevel."""
    return math.floor(base_capacity * (1.25 ** warehouse_level.value))

# # Beispiel Basiskosten
# goldmine_base_costs = models.Storage(90, 60,60)
# goldmine_base_time_sec = 1000  # 16 min 40 sek


# # Was kostet es, die Goldmine von Level 1 auf 2 auszubauen?
# next_costs = calculate_upgrade_costs(goldmine_base_costs, level=models.Level.L9)
# print(next_costs)

# # Wie lange dauert der Bau bei Fortress Level 1?
# next_build_time = calculate_upgrade_time(goldmine_base_time_sec, level=models.Level.L19, fortress_level=models.Level.L1)
# print(next_build_time)

# # Produktion einer Goldmine auf Level 3
# production = calculate_production_per_hour(base_production=4.5, level=models.Level.L19)
# print(production)

# # Speicherplatz bei Lager auf Level 2
# storage = calculate_storage_capacity(base_capacity=1000, warehouse_level=models.Level.L19)
# print(storage)
