
import networkx as nx
import numpy as np

def cascade_seeded_by_outdegree(G, population, node_limit, budget):
    """
    Improved version of select_by_out_degree with a smarter budget utilization.
    
    :param G: networkx graph - graph of nodes and population flow
    :param population: numpy array - index corresponds to node id, value is population at that node
    :param node_limit: int - max number of nodes 
    :param budget: float - max population budget 
    
    :return: numpy array with index corresponding to node id, value to percent adoption allocated to that node
    """
    initial_adoptions = np.zeros(len(population))
    used_budget = 0
    nodes_sorted = sorted(G.nodes(), key=lambda x: G.out_degree(x), reverse=True)

    for node in nodes_sorted:
        pop_node = population[node]

        if used_budget + pop_node <= budget:
            initial_adoptions[node] = 1
            used_budget += pop_node

            if np.count_nonzero(initial_adoptions) == node_limit:
                break

    while used_budget < 0.9 * budget:
        node_max_pop = max((n for n in G.nodes() if initial_adoptions[n] == 0), key=lambda x: population[x])
        additional_budget = 0.9 * budget - used_budget
        additional_adoption = min(additional_budget / population[node_max_pop], 1)
        initial_adoptions[node_max_pop] += additional_adoption
        used_budget += additional_adoption * population[node_max_pop]

    return initial_adoptions