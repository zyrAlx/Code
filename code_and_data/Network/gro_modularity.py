import networkx as nx
import community as community_louvain
import pandas as pd
import os

# Open the output file
with open('gro_modularity.txt', 'w') as f:
    # Write the headers
    f.write('thre,best,my_community\n')

    for filename in os.listdir("final_table"):
        threshold = filename.split('.csv')[0]
        edges_df = pd.read_csv(f'threshold/filtered_{threshold}.csv')
        communities_df = pd.read_csv(f'final_table/{threshold}.csv')
        communities_df['family'] = communities_df['family'].str.replace('group', '').astype(int)

        # Create a set of nodes
        nodes_set = set(communities_df['node'])

        # Keep only rows in edges_df where both 'clusterA' and 'clusterB' are in the set of nodes
        edges_df = edges_df[edges_df['nodeA'].isin(nodes_set) & edges_df['nodeB'].isin(nodes_set)]

        # Create the graph
        G = nx.from_pandas_edgelist(edges_df, 'nodeA', 'nodeB', 'e-value')

        # Create the partition dictionary
        partition = dict(zip(communities_df['node'], communities_df['family']))

        ####Compute the best partition
        best_partition = community_louvain.best_partition(G)
        ####Compute modularity of the best partition
        modularity_best = community_louvain.modularity(best_partition, G)

        # Compute modularity of your provided partition
        modularity_your_partition = community_louvain.modularity(partition, G)

        # Write the results to the file
        f.write(f'{threshold},{modularity_best},{modularity_your_partition}\n')