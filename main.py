import logging
from typing import List, Tuple
import igraph as ig

import models as md
import params as pr
from state_updater import is_possible_action, update_state

def explore_states(states: List[md.State], transitions: List[Tuple[int, int]], current_state: md.State):
    # Generate all possible actions for the current state
    possible_actions = [action for action in md.Action if is_possible_action(state=current_state, action=action)]
    for action in possible_actions:
        # Compute the new state
        new_state = update_state(state=current_state, action=action)
        
        # Add the new state to the list of states and edges
        states.append(new_state)
        transitions.append((current_state.id, new_state.id))

        # Check if the new state is a final state
        if new_state.is_final_state:
            logging.info(f"Final state reached at id: {new_state.id}")
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
        num_stone_hurler=0
    )
    states: List[md.State] = [initial_state]
    transitions: List[Tuple[int, int]] = []
    
    logging.info("Start exploring all possible states from the initial states")
    explore_states(states, transitions, initial_state)

    logging.info("populate graph with vertices and edges")
    g = ig.Graph(
        n=len(states),
        edges=transitions,
        edge_attrs={'weight': [i for i in range(0,len(states))], 'label': [str(i) for i in range(0,len(states))]},
        vertex_attrs={'label': [state.id for state in states]},
        directed=True
        )
    

    # some testing code
    # edges=[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 6)]
    # edge_weights=[2, 1, 2, 3, 4, 5, 16]
    # gtest = ig.Graph(
    #     n=6,
    #     edges=edges,
    #     edge_attrs={'weight': edge_weights, 'label': [str(i) for i in range(0,len(edges))]},
    #     vertex_attrs={'label': [str(i) for i in range(0,6)]},
    #     directed=True
    #     )
    # gtest.get_shortest_paths(0, to=6, weights='weight')
    

    # g = ig.Graph(directed=True)
    # g.add_vertex(label=str(initial_state.id), id=initial_state.id)
    # g.add_vertex(label=str(new_state.id), id=new_state.id)
    # g.add_edge(current_state.id, new_state.id)

    logging.info("Find all shortest paths")
    final_state_ids = [state.id for state in states if state.is_final_state]
    shortest_paths = g.get_shortest_paths(0, to=final_state_ids, weights='weight', output="epath")
    if shortest_paths:
        shortest_path = min(shortest_paths, key=lambda path: sum([g.es[edge]["weight"] for edge in path]))
        shortest_distance = sum([g.es[edge]["weight"] for edge in shortest_path])
        print(f"Shortest Path: {shortest_path}, Distance: {shortest_distance}")
    else:
        print("No paths found.")

if __name__ == "__main__":
    main()
