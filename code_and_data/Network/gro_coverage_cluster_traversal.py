import pandas as pd
import itertools
from collections import defaultdict
import numpy as np
import os
from pathlib import Path

table_path = "table_cov2"
cov_output = "coverage2"

for filename in os.listdir(table_path):
    thre = filename.split('.csv')[0]
    threshold = pd.read_csv(f'threshold/filtered_{thre}.csv')
    annotations = pd.read_csv(f'{table_path}/{thre}.csv')
    
    merged = pd.merge(threshold, annotations, left_on='nodeA', right_on='node', how='left').drop(columns='node').rename(columns={'family': 'familyA'})
    merged = pd.merge(merged, annotations, left_on='nodeB', right_on='node', how='left').drop(columns='node').rename(columns={'family': 'familyB'})
    
    str_dict = defaultdict(set)
    for _, row in merged.iterrows():
        str_dict[row['familyA']].add(row['nodeA'])
        str_dict[row['familyB']].add(row['nodeB'])
    
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
    Path(cov_output).mkdir(parents=True, exist_ok=True)
    results_df.to_csv(f'{cov_output}/{thre}_statistic_of_gro_coverage.csv', index=False)