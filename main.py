import logging
from typing import List, Tuple
import igraph as ig

from global_state_manager import GlobalStateManager
import models as md
import params as pr
from state_updater import is_possible_action, update_state

def explore_states(states: List[md.State], transitions: List[Tuple[int, int, int, md.Action]], current_state: md.State) -> None:
    """
    Recursively explores all possible states and transitions from the current state.
    Args:
        states (List[md.State]): List of all states explored so far.
        transitions (List[Tuple[int, int, int, md.Action]]): List of transitions between states.
        current_state (md.State): The current state to explore from.
    """
    # Check if the new state is already above the lowest known duration
    global_state = GlobalStateManager.get_global_state()
    lowest_duration = global_state.get_lowest_known_duration()
    if current_state.current_duration >= lowest_duration:
        logging.debug(f"Skipping state {current_state.id} with duration {current_state.current_duration} as it exceeds the lowest known duration {lowest_duration}")
        return
    
    # Generate all possible actions for the current state
    possible_actions = [action for action in md.Action if is_possible_action(state=current_state, action=action)]
    for action in possible_actions:
        new_state = update_state(state=current_state, action=action)
        
        # Add the new state to the list of states and edges
        states.append(new_state)
        transitions.append((current_state.id, new_state.id, new_state.current_duration, action))
        logging.debug(f"Transition from state {current_state.id} to state {new_state.id} with action {action.name} and duration {new_state.current_duration}")

        # Check if the new state is a final state
        if new_state.is_final_state:
            logging.info(f"Final state reached at id: {new_state.id} with duration: {new_state.current_duration}")
            global_state.update_lowest_known_duration(new_state.current_duration)
            continue
        
        # Recursively explore further actions from the new state
        explore_states(states, transitions, new_state)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Initialize the program")
    
    initial_state = md.State(
        storage=md.Storage(
            gold=pr.initial_gold,
            stone=pr.initial_stone,
            wood=pr.initial_wood,
        ),
        gold_mine_level=md.Level.L0,
        wood_mine_level=md.Level.L0,
        stone_mine_level=md.Level.L0,
        fortress_level=md.Level.L1,
        harbor_level=md.Level.L0,
        garrison_level=md.Level.L0,
        warehouse_level=md.Level.L0,
        num_frigates=0,
        num_cargo_ships=0,
        num_stone_hurler=0,
        current_duration=0
    )
    states: List[md.State] = [initial_state]
    transitions: List[Tuple[int, int, int, md.Action]] = []
    
    logging.info("Start exploring all possible states from the initial states")
    explore_states(states, transitions, initial_state)

    logging.info("populate graph with vertices and edges")
    g = ig.Graph(
        n=len(states),
        edges=[(a, b) for a, b, _, _ in transitions],
        edge_attrs={
            'weight': [c for _, _, c, _ in transitions],
            'action': [str(d.name) for _, _, _, d in transitions],  # Store action names as edge attributes
            'label': [str(c) for _, _, c, _ in transitions]
        },
        vertex_attrs={'label': [state.id for state in states]},
        directed=True
    )

    logging.info("Find all shortest paths")
    final_state_ids = [state.id for state in states if state.is_final_state]
    shortest_paths = g.get_shortest_paths(0, to=final_state_ids, weights='weight', output="epath")
    if shortest_paths:
        shortest_path = min(shortest_paths, key=lambda path: sum([g.es[edge]["weight"] for edge in path]))
        shortest_distance = sum([g.es[edge]["weight"] for edge in shortest_path])
        action_labels = [g.es[edge]["action"] for edge in shortest_path]  # Retrieve actions from edge attributes
        print(f"Shortest Path Actions: {action_labels}, Distance: {shortest_distance}")
    else:
        print("No paths found.")

if __name__ == "__main__":
    main()
