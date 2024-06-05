
import networkx as nx
import numpy as np

def cascade_seeded_by_centrality(G, population, node_limit, budget):
    """
    Improved version of select_by_centrality with cost-efficiency adjustment.
    
    :param G: networkx graph - graph of nodes and population flow
    :param population: numpy array - index corresponds to node id, value is population at that node
    :param node_limit: int - max number of nodes 
    :param budget: float - max population budget 
    
    :return: numpy array with index corresponding to node id, value to percent adoption allocated to that node
    """
    initial_adoptions = np.zeros(len(population))
    used_budget = 0
    selected_nodes = 0
    centrality_scores = nx.betweenness_centrality(G)

    # Adjust centrality scores by population to consider cost-efficiency
    adjusted_scores = {node: centrality_scores[node] / population[node] if population[node] > 0 else 0 for node in G.nodes()}
    
    # Sort nodes by adjusted scores in descending order
    sorted_nodes = sorted(adjusted_scores, key=adjusted_scores.get, reverse=True)

    for node in sorted_nodes:
        if selected_nodes >= node_limit or used_budget >= budget:
            break
        
        pop_node = population[node]
        if pop_node == 0:
            continue

        remaining_budget = budget - used_budget
        adoption_rate = min(1, remaining_budget / pop_node)
        initial_adoptions[node] = adoption_rate
        used_budget += adoption_rate * pop_node
        selected_nodes += 1

    # Smarter loop to ensure at least 90% of the budget is utilized
    while used_budget < 0.9 * budget and selected_nodes < node_limit:
        for node in sorted_nodes[selected_nodes:]:
            pop_node = population[node]
            if pop_node > 0:
                additional_budget = min(pop_node, 0.9 * budget - used_budget)
                if additional_budget <= 0:
                    break
                adoption_rate = additional_budget / pop_node
                initial_adoptions[node] = adoption_rate
                used_budget += additional_budget
                selected_nodes += 1
                if used_budget >= 0.9 * budget:
                    break

    return initial_adoptions