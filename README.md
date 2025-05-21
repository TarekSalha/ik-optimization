# IK Optimization

This project explores and optimizes state transitions for a resource management scenario, building a state graph and finding the shortest path to a final state using Python. It is designed to be run on a typical developer laptop.

## Features

- Models resource states and transitions using Python dataclasses and enums.
- Efficiently explores possible states and transitions.
- Builds a graph of all explored states and transitions using [igraph](https://igraph.org/python/).
- Finds and prints the shortest sequence of actions to reach a final state.
- Designed for extensibility and clarity.

## Requirements

- Python 3.13 or newer
- [uv](https://github.com/astral-sh/uv) (for dependency and environment management)
- [igraph](https://igraph.org/python/) (`python-igraph`)

## Installation

1. **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd ik-optimization
    ```

2. **Install [uv](https://github.com/astral-sh/uv):**

    Install UV using the official standalone installer

    **macOS and Linux:**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    **Windows:**

    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    *Tip:* UV can also be installed via `pip`, Homebrew, and other  methods. Refer to the [installation page](https://docs.astral.sh/uv/getting-started/installation/) for more options.

## Usage

Run the main optimization script using [uv](https://github.com/astral-sh/uv):

```bash
uv run main.py
```

### Expected Output

When you run the script, it will:

- Print a summary of the initial and final resource states.
- Display the shortest sequence of actions (state transitions) required to reach the final state.
- Show the total time and resources consumed along the optimal path.
- Output detailed logs or progress updates, depending on the verbosity settings.

The output helps you understand the optimal steps and resource usage for your scenario.

## Conversion Algorithm

The core of the project is a conversion algorithm that systematically explores all possible resource state transitions. It works by:

- Representing each unique resource configuration as a node in a graph
- Generating all valid transitions (actions) from the current state using well-defined rules
- Pruning the search tree by avoiding the exploration of suboptimal paths
- Using efficient search strategies to avoid redundant computations and cycles
- Once the graph is built, the algorithm computes the shortest path from the initial state to the desired final state, providing a step-by-step sequence of actions for optimal resource conversion

This approach ensures both completeness (all possible states are considered) and efficiency (minimizing unnecessary exploration).

## Pruning Method

At each node in the state graph, the algorithm estimates the minimum required time to reach the final state (i.e., to build the full fleet). This estimation uses a configurable parameter that controls the degree of underestimation. By adjusting this parameter, you can influence the trade-off between exploration and runtime:

- **Lower estimation parameter (more underestimation):** The algorithm explores more states, which increases runtime but can yield more optimal solutions.
- **Higher estimation parameter (closer to 1, less underestimation):** The algorithm explores fewer states, reducing runtime but potentially missing the optimal path.

When the parameter is set to 1, the algorithm performs minimal underestimation, resulting in faster execution but possibly suboptimal results. This pruning approach allows you to balance solution quality and computational efficiency based on your needs.

> **Hint:** For best results, set the estimation parameter to a value between **0.8 and 1**. Lower values may significantly increase runtime, while higher values may miss optimal solutions.

## Configuration Parameters

You can fine-tune the optimization by editing the [`params.py`](params.py) file. Below are the main parameters you can set and their descriptions:

| Parameter Name                   | Type    | Description                                                                                   |
|----------------------------------|---------|-----------------------------------------------------------------------------------------------|
| `initial_gold`                   | int     | Starting amount of gold resources.|
| `initial_wood`                   | int     | Starting amount of wood resources.|
| `initial_stone`                  | int     | Starting amount of stone resources.|
| `initial_warehouse_capacity`     | int     | Initial storage capacity for resources.|
| `initial_rate_gold`              | float   | Initial gold production rate.|
| `initial_rate_wood`              | float   | Initial wood production rate.|
| `initial_rate_stone`             | float   | Initial stone production rate.|
| `max_number_stone_hurler`        | int     | Maximum number of stone hurlers that will be built by the algorithm.|
| `max_number_frigates`            | int     | Maximum number of frigates that will be built by the algorithm.|
| `max_number_cargo_ships`         | int     | Maximum number of cargo ships that will be built by the algorithm.|
| `max_level_mines`                | int     | Maximum allowed level for mines. The algorithm will only explore states with a level <= this parameter|
| `max_level_warehouse`            | int     | Maximum allowed level for the warehouse. In cases of large intial space, this parameter should be set to 0 as the algorithm will then not consider building a warehouse, which lets the computation converge much faster|
| `max_diff_level_mines`           | int     | Maximum allowed difference between mine levels. this parameter can additionally narrow the explored states as it immediately eliminates permutations where mine levels are too far from each other (e.g. gold L8 and  stone L1).|
| `cost_estimation_parameter`      | float   | Controls how much the algorithm underestimates the time needed to reach a final state. Lower values = more exploration (slower, more optimal); higher values = less exploration. Recommended: between **0.8 and 1.0**.|
| `base_costs_*` and `base_time_*` | int     | Base resource costs and build times for each building/unit type (see `params.py` for details). These must be gathered from the game UI.|

**Tip:**  
Adjust these parameters to match your scenario or to experiment with different optimization strategies. For example, increasing `cost_estimation_parameter` will make the algorithm run faster but may miss the most optimal solution.

---
