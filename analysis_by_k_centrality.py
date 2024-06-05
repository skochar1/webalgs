
# analysis_by_k_centrality.py
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
k_centrality = nx.katz_centrality_numpy(G)
k_centrality_df = pd.DataFrame(list(k_centrality.items()), columns=['user_id', 'k_centrality'])

# Merge data
merged_df = pd.merge(k_centrality_df, gender_df, on='user_id', how='left')

# Analyze data
total_females = merged_df[merged_df['gender'] == 'F'].shape[0]
max_k_centrality = merged_df['k_centrality'].max()
k_centralities = sorted(set(merged_df['k_centrality']))
fraction_females = []
marker_sizes = []

for k in k_centralities:
    num_females_at_k = merged_df[(merged_df['gender'] == 'F') & (merged_df['k_centrality'] >= k)].shape[0]
    fraction = num_females_at_k / total_females if total_females != 0 else 0
    fraction_females.append(fraction * 100)
    total_users_at_k = merged_df[merged_df['k_centrality'] >= k].shape[0]
    total_users = merged_df.shape[0]
    marker_sizes.append(total_users_at_k / total_users * 1000)

# Plot results
center_marker_sizes = [2 for _ in fraction_females]
plt.figure(figsize=(10, 6))
plt.scatter(k_centralities, fraction_females, marker='o', s=marker_sizes, color='hotpink', alpha=0.3)
plt.scatter(k_centralities, fraction_females, s=center_marker_sizes, color='hotpink')
plt.xscale('log')
graph = plt.gca()
graph.set_xscale('log')
graph.xaxis.set_major_locator(ticker.FixedLocator([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e0]))
graph.xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.xlabel('K-Centrality')
plt.ylabel('Fraction of Females (%)')
plt.title('Glass Ceiling Effect by K-Centrality in Instagram Network')
plt.show()
