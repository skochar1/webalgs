
# analysis_by_bet_centrality.py
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load data
edges_path = 'path_to_edges_file.txt'
edges_df = pd.read_csv(edges_path, delim_whitespace=True, header=None, names=['source', 'target'])
gender_path = 'path_to_gender_file.csv'
gender_df = pd.read_csv(gender_path)
gender_df.columns = ['user_id', 'gender']

# Create graph
G = nx.from_pandas_edgelist(edges_df, 'source', 'target', create_using=nx.Graph())

# Calculate betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G, normalized=True)
betweenness_df = pd.DataFrame(list(betweenness_centrality.items()), columns=['user_id', 'betweenness'])

# Merge data
merged_df = pd.merge(betweenness_df, gender_df, on='user_id', how='left')

# Analyze data
total_females = merged_df[merged_df['gender'] == 'F'].shape[0]
betweenness_values = sorted(set(betweenness_centrality.values()))
fraction_females_betweenness = []
marker_sizes_betweenness = []

for betweenness in betweenness_values:
    num_females_at_betweenness = merged_df[(merged_df['gender'] == 'F') & (merged_df['betweenness'] >= betweenness)].shape[0]
    fraction = num_females_at_betweenness / total_females if total_females != 0 else 0
    fraction_females_betweenness.append(fraction * 100)
    
    total_users_at_betweenness = merged_df[merged_df['betweenness'] >= betweenness].shape[0]
    total_users = merged_df.shape[0]
    marker_sizes_betweenness.append(total_users_at_betweenness / total_users * 1000)

# Plot results
center_marker_sizes_betweenness = [2 for _ in fraction_females_betweenness]
plt.figure(figsize=(10, 6))
plt.scatter(betweenness_values, fraction_females_betweenness, s=marker_sizes_betweenness, color='hotpink', alpha=0.3)
plt.scatter(betweenness_values, fraction_females_betweenness, s=center_marker_sizes_betweenness, color='hotpink')
plt.xscale('log')
plt.xlabel('Betweenness Centrality')
plt.ylabel('Percentage of Female Users')
plt.title('Glass Ceiling Effect by Betweenness Centrality in Instagram Network')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
