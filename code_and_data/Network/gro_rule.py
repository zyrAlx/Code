import pandas as pd
import numpy as np
import networkx as nx
from collections import Counter
from networkx.algorithms.components import connected_components
from collections import defaultdict
import itertools

for threshold in sorted(np.arange(10, 70, 1), reverse=True):
    #threshold = round(threshold, 2)
    threshold_net = threshold - 1
    #threshold_net = round(threshold_net, 2)
    anno_csv = pd.read_csv(f'table/1e-{threshold}.csv')
    anno = anno_csv.set_index('node')['family'].to_dict()
    
    threshold_csv = pd.read_csv(f'threshold/filtered_1e-{threshold_net}.csv')
    G = nx.from_pandas_edgelist(threshold_csv, 'nodeA', 'nodeB', edge_attr='e-value')
    
    for component in connected_components(G):
        if not any(node in anno for node in component) and len(component) > 20:
            if anno.values(): 
                max_family_num = max(int(name[5:]) for name in anno.values())
            else: 
                max_family_num = 0
            new_family_name = 'group' + str(max_family_num + 1)
    
            anno.update({node: new_family_name for node in component})

    new_nodes = set(G.nodes()) - set(anno.keys())
    for _ in range(5): 
        still_new_nodes = set()
        for node in new_nodes:
            neighbors = G.neighbors(node)
            neighbor_anno = [anno[neighbor] for neighbor in neighbors if neighbor in anno]
    
            if neighbor_anno:
                anno[node] = Counter(neighbor_anno).most_common(1)[0][0]
            else:
                still_new_nodes.add(node)
        new_nodes = still_new_nodes

    str_dict = {}
    for key, value in anno.items():
        if value not in str_dict:
            str_dict[value] = [key]
        else:
            str_dict[value].append(key)
    merged = pd.merge(threshold_csv, anno_csv, left_on='nodeA', right_on='node', how='left').drop(columns='node').rename(columns={'family': 'familyA'})
    merged = pd.merge(merged, anno_csv, left_on='nodeB', right_on='node', how='left').drop(columns='node').rename(columns={'family': 'familyB'})
    
    edges_dict = defaultdict(set)
    for _, row in merged.iterrows():
        edges_dict[(row['familyA'], row['familyB'])].add(row['nodeA'])
        edges_dict[(row['familyB'], row['familyA'])].add(row['nodeB'])
    results = []
    for str1, str2 in itertools.combinations(str_dict.keys(), 2):
        str1_cluster_count = len(edges_dict[(str1, str2)])
        str2_cluster_count = len(edges_dict[(str2, str1)])
        results.append({
            'str1': str1,
            'str2': str2,
            'cluster counts of str1': str1_cluster_count,
            'precent of str1': str1_cluster_count / len(str_dict[str1]),
            'cluster counts of str2': str2_cluster_count,
            'precent of str2': str2_cluster_count / len(str_dict[str2]),
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.dropna()
    results_df = results_df[(results_df != 0).all(1)]
    results_df.to_csv(f'coverage/1e-{threshold_net}_statistic_of_gro_coverage.csv', index=False)
    
    result_df = pd.DataFrame(list(anno.items()), columns=['node', 'family'])
    result_df.to_csv(f'table/1e-{threshold_net}.csv', index=False)