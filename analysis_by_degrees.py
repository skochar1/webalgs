
# analysis_by_degrees.py
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
degrees = dict(G.degree())
degrees_df = pd.DataFrame(list(degrees.items()), columns=['user_id', 'degree'])

# Merge data
merged_df = pd.merge(degrees_df, gender_df, on='user_id', how='left')

# Analyze data
total_females = merged_df[merged_df['gender'] == 'F'].shape[0]
max_degree = merged_df['degree'].max()
degrees = range(max_degree + 1)
fraction_females = []
marker_sizes = []

for k in degrees:
    num_females_at_k = merged_df[(merged_df['gender'] == 'F') & (merged_df['degree'] >= k)].shape[0]
    fraction = num_females_at_k / total_females if total_females != 0 else 0
    fraction_females.append(fraction * 100)
    total_users_at_k = merged_df[merged_df['degree'] >= k].shape[0]
    total_users = merged_df.shape[0]
    marker_sizes.append(total_users_at_k / total_users * 1000)

# Plot results
center_marker_sizes = [2 for _ in fraction_females]
plt.figure(figsize=(10, 6))
plt.scatter(degrees, fraction_females, marker='o', s=marker_sizes, color='hotpink', alpha=0.3)
plt.scatter(degrees, fraction_females, s=center_marker_sizes, color='hotpink')
plt.xscale('log')
graph = plt.gca()
graph.set_xscale('log')
graph.xaxis.set_major_locator(ticker.FixedLocator([1, 2, 5, 10, 20, 50, 100, 200]))
graph.xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.xlabel('Degree')
plt.ylabel('Fraction of Females (%)')
plt.title('Glass Ceiling Effect by Node Degree in Instagram Network')
plt.show()
