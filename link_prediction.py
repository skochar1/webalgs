"""
Link Prediction Algorithm in Networks

This script implements a link prediction algorithm that evaluates and predicts links between two graphs. 
It reads graph edges and linked pairs from specified file paths, constructs graphs, 
iteratively finds and adds new links, writes the new links to a file, and estimates the error rate of the link prediction process.
"""

from collections import defaultdict
import networkx as nx
import random

file_paths = {
    'linked_pairs': '...',
    'g1': '...',
    'g2': '...'
}

def count_correct_predictions(predicted_links, g1, g2):
    """
    Evaluate the number of correct predicted links between two graphs.
    
    Parameters:
        predicted_links (list): List of tuples representing the predicted links.
        g1 (dict): First graph as a dictionary.
        g2 (dict): Second graph as a dictionary.

    Returns:
        int: Number of correct predicted links.
    """
    correct_links = 0
    for u, v in predicted_links:
        if u in g1 and v in g2 and v == u:
            correct_links += 1
    return correct_links

def create_evaluation_graph(graph):
    """
    Create a testing graph from an input graph using known information.
    
    Parameters:
        graph (dict): Input graph as a dictionary.

    Returns:
        nx.Graph: Testing graph.
    """
    return nx.Graph(graph)

def eliminate_duplicate_edges(graph):
    """
    Remove duplicate edges from the graph to ensure fairness in evaluation.
    
    Parameters:
        graph (nx.Graph): Input graph.

    Returns:
        nx.Graph: Cleaned graph without duplicate edges.
    """
    cleaned_graph = nx.Graph()
    for u, v in graph.edges():
        cleaned_graph.add_edge(u, v)
    return cleaned_graph

def calculate_error_rate(g1, g2, new_pairs):
    """
    Compute the error rate of the link prediction process.
    
    Parameters:
        g1 (dict): First graph as a dictionary.
        g2 (dict): Second graph as a dictionary.
        new_pairs (list): List of new predicted pairs.

    Returns:
        float: Error rate.
    """
    correct_predictions = count_correct_predictions(new_pairs, g1, g2)
    total_predictions = len(new_pairs)
    
    error_rate = 1 - (correct_predictions / total_predictions) if total_predictions > 0 else 0
    return error_rate

def parse_graph_edges(file_path):
    """
    Read graph edges from a text file.
    
    Parameters:
        file_path (str): Path to the text file containing the graph edges.

    Returns:
        list: List of tuples representing the edges of the graph.
    """
    with open(file_path, 'r') as file:
        edges = [tuple(line.strip().split()) for line in file]
    return edges

def construct_graph_dict(edges):
    """
    Build a graph from a list of edges.
    
    Parameters:
        edges (list): List of tuples representing the edges of the graph.

    Returns:
        dict: Graph as a dictionary where keys are nodes and values are sets of neighbor nodes.
    """
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph

def load_linked_pairs(file_path):
    """
    Read linked pairs from a text file.
    
    Parameters:
        file_path (str): Path to the text file containing the linked pairs.

    Returns:
        list: List of tuples representing the linked pairs.
    """
    with open(file_path, 'r') as file:
        linked_pairs = [tuple(line.strip().split()) for line in file]
    return linked_pairs

def find_potential_links(g1, g2, linked_pairs):
    """
    Calculate potential links between two graphs based on linked pairs.
    
    Parameters:
        g1 (dict): First graph as a dictionary.
        g2 (dict): Second graph as a dictionary.
        linked_pairs (list): List of linked pairs.

    Returns:
        dict: Potential links with common neighbors count.
    """
    g1_to_g2 = {pair[0]: pair[1] for pair in linked_pairs}
    potential_links = defaultdict(list)
    for node1, neighbors1 in g1.items():
        translated_neighbors1 = {g1_to_g2.get(n) for n in neighbors1 if n in g1_to_g2}
        for node2 in g2:
            common = sum(1 for n in translated_neighbors1 if n in g2[node2])
            if common > 0:
                potential_links[node1].append((node2, common))
        potential_links[node1] = sorted(potential_links[node1], key=lambda x: (-x[1], int(x[0])))

    return potential_links

def generate_new_links(g1, g2, initial_pairs, threshold, potential_links):
    """
    Identify new links based on potential links and a threshold.
    
    Parameters:
        g1 (dict): First graph as a dictionary.
        g2 (dict): Second graph as a dictionary.
        initial_pairs (list): List of initial linked pairs.
        threshold (int): Threshold for considering a potential link.
        potential_links (dict): Potential links with common neighbors count.

    Returns:
        list: List of new identified links.
    """
    existing_links = set(initial_pairs)
    g1_linked_nodes = {pair[0] for pair in initial_pairs}
    g2_linked_nodes = {pair[1] for pair in initial_pairs}
    new_links = []

    for node1, links in potential_links.items():
        if node1 in g1_linked_nodes:
            continue
        for node2, score in links:
            if score >= threshold and node2 not in g2_linked_nodes:
                if (node1, node2) not in existing_links:
                    new_links.append((node1, node2))
                    g1_linked_nodes.add(node1)
                    g2_linked_nodes.add(node2)
                    break

    return new_links

def initialize_linked_pairs(g1, g2):
    """
    Generate initial linked pairs based on nodes present in both graphs.
    
    Parameters:
        g1 (dict): First graph as a dictionary.
        g2 (dict): Second graph as a dictionary.

    Returns:
        list: List of initial linked pairs.
    """
    linked_pairs = []
    for node_g1 in g1:
        if node_g1 in g2:
            linked_pairs.append((node_g1, node_g1))
        if len(linked_pairs) >= 1000:
            return linked_pairs

def execute_link_prediction(file_paths):
    """
    Execute the link prediction process.
    
    Parameters:
        file_paths (dict): Dictionary containing paths to input files.
    """
    # Load graphs and linked pairs from file paths
    g1_edges = parse_graph_edges(file_paths['g1'])
    g2_edges = parse_graph_edges(file_paths['g2'])
    linked_pairs = load_linked_pairs(file_paths['linked_pairs'])

    # Construct graphs
    g1 = construct_graph_dict(g1_edges)
    g2 = construct_graph_dict(g2_edges)
    
    # Adaptive thresholding based on graph properties
    threshold = 3

    new_links = []
    check = True
    links = linked_pairs.copy()
    while check:
        potential_links = find_potential_links(g1, g2, links)
        additional_links = generate_new_links(g1, g2, links, threshold, potential_links)
        if len(additional_links) == 0:
            check = False
        new_links.extend(additional_links)
        links.extend(additional_links)

    # Write new links to a file
    with open('Ex3-3.txt', 'w') as f:
        for link in new_links:
            f.write(f"{link[0]} {link[1]}\n")

    graph_file_path = '...'
    graph_edges = parse_graph_edges(graph_file_path)
    graph = construct_graph_dict(graph_edges)

    g_nodes = random.sample(list(graph.keys()), int(0.8 * len(graph)))
    g1_edges = [(node, neighbor) for node in g_nodes for neighbor in graph[node]]
    g2_edges = [(node, neighbor) for node in g_nodes for neighbor in graph[node]]

    g1_snap = construct_graph_dict(g1_edges)
    g2_snap = construct_graph_dict(g2_edges)

    linked_sn = initialize_linked_pairs(g1_snap, g2_snap)
    thresholds = range(3, 6)

    for T in thresholds:
        new_links = []
        check = True
        links = linked_sn.copy()
        while check:
            potential_links = find_potential_links(g1_snap, g1_snap, links)
            additional_links = generate_new_links(g1_snap, g2_snap, links, T, potential_links)
            if len(additional_links) == 0:
                check = False
            new_links.extend(additional_links)
            links.extend(additional_links)

        # Estimate error rate for the current threshold
        error_rate = calculate_error_rate(g1_snap, g2_snap, new_links)
        print(f"Threshold {T}: Error rate = {error_rate}")

# Execute the link prediction process
execute_link_prediction(file_paths)
