initial_gold: int = 1000
initial_wood: int = 1000
initial_stone: int = 1000

initial_warehouse_capacity: int  = 500

initial_rate_gold: float = 4.5
initial_rate_wood: float = 4.0
initial_rate_stone: float = 3.0

max_number_stone_hurler: int = 5
max_number_frigates: int = 1
max_number_cargo_ships: int = 1

max_level_mines: int = 7                    # it is quite unlikely that you will find effective strategies above this level
max_level_warehouse: int = 4                # the maximum allowed level of the warehouse
max_diff_level_mines: int = 10

cost_estimation_parameter: float = 0.95     # determines how much the algorithm should underestimate needed time to reach a final state, do not set to >1.0

base_costs_fortress_gold: int = 150
base_costs_fortress_stone: int = 120
base_costs_fortress_wood: int = 90
base_time_fortress: int = 1500

base_costs_garrison_gold: int = 120
base_costs_garrison_stone: int = 120
base_costs_garrison_wood: int = 120
base_time_garrison: int = 1120

base_costs_warehouse_gold: int = 90
base_costs_warehouse_stone: int = 60
base_costs_warehouse_wood: int = 90
base_time_warehouse: int = 960

base_costs_harbor_gold: int = 150
base_costs_harbor_stone: int = 160
base_costs_harbor_wood: int = 120
base_time_harbor: int = 1280

base_costs_gold_mine_gold: int = 90
base_costs_gold_mine_stone: int = 60
base_costs_gold_mine_wood: int = 60
base_time_gold_mine: int = 800

base_costs_stone_mine_gold: int = 60
base_costs_stone_mine_stone: int = 60
base_costs_stone_mine_wood: int = 60
base_time_stone_mine: int = 800

base_costs_wood_mine_gold: int = 90
base_costs_wood_mine_stone: int = 70
base_costs_wood_mine_wood: int = 60
base_time_wood_mine: int = 960

base_costs_stone_hurler_gold: int = 50
base_costs_stone_hurler_stone: int = 10
base_costs_stone_hurler_wood: int = 5
base_time_stone_hurler: int = 1492

base_costs_fregate_gold: int = 600
base_costs_fregate_stone: int = 0
base_costs_fregate_wood: int = 500
base_time_fregate: int = 8962

base_costs_cargo_ship_gold: int = 600
base_costs_cargo_ship_stone: int = 0
base_costs_cargo_ship_wood: int = 750
base_time_cargo_ship: int = 14937