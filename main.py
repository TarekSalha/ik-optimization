import logging
import datetime
from typing import List, Tuple
import igraph as ig

from cost_calculator import estimate_remaining_time
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
    # Check if the current state is already above the lowest known duration
    global_state = GlobalStateManager.get_global_state()
    lowest_duration = global_state.get_lowest_known_duration()
    estimated_duration_current_state = estimate_remaining_time(current_state)
    if (current_state.current_duration + estimated_duration_current_state) >= lowest_duration:
        logging.debug(f"Skipping state {current_state.id} with duration {current_state.current_duration}s {str(datetime.timedelta(seconds=current_state.current_duration))} (HH:MM:SS) as it exceeds the lowest known duration {lowest_duration}")
        return
    
    # Generate all possible actions for the current state
    possible_actions = [action for action in md.Action if is_possible_action(state=current_state, action=action)]
    for action in possible_actions:
        new_state = update_state(state=current_state, action=action)
        if new_state.id % 100000 == 0:
            logging.info(f"exploring new state with id: {new_state.id}")
        estimated_duration_new_state = estimate_remaining_time(new_state)
        lowest_duration = global_state.get_lowest_known_duration()
        if (new_state.current_duration + estimated_duration_new_state) >= lowest_duration:
            logging.debug(f"Skipping state {new_state.id} with duration {new_state.current_duration}s {str(datetime.timedelta(seconds=new_state.current_duration))} (HH:MM:SS) as it exceeds the lowest known duration {lowest_duration}")
            continue

        # Add the new state to the list of states and edges
        states.append(new_state)
        logging.debug(f"New state added with id: {new_state.id} and duration: {new_state.current_duration}s {str(datetime.timedelta(seconds=new_state.current_duration))} (HH:MM:SS) for action: {action.name} Storage: {new_state.storage}")
        transitions.append((current_state.id, new_state.id, new_state.current_duration - current_state.current_duration, action))
        logging.debug(f"Transition from state {current_state.id} to state {new_state.id} with action {action.name} and duration {new_state.current_duration}s {str(datetime.timedelta(seconds=new_state.current_duration))} (HH:MM:SS)")

        # Check if the new state is a final state
        if new_state.is_final_state:
            logging.info(f"Final state reached at id: {new_state.id} with duration: {new_state.current_duration}s {str(datetime.timedelta(seconds=new_state.current_duration))} (HH:MM:SS)")
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
        # Output the final result as a list of applied actions and storage at every step
        print("Shortest Path Steps:")
        current_state = states[0]
        print(f"Step 0: Action: Initial State, Storage: {current_state.storage}, Total Duration: {str(datetime.timedelta(seconds=current_state.current_duration))} (HH:MM:SS)")
        for idx, edge in enumerate(shortest_path):
            action = g.es[edge]["action"]
            next_state_id = g.es[edge].target
            next_state = next(s for s in states if s.id == next_state_id)
            print(f"Step {idx+1}: Action: {action}, Storage: {next_state.storage}, Total Duration: {str(datetime.timedelta(seconds=next_state.current_duration))} (HH:MM:SS)")
    else:
        print("No paths found.")

if __name__ == "__main__":
    main()
