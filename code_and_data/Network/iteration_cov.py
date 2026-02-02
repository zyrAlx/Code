import pandas as pd
import numpy as np
import os
import networkx as nx
from pathlib import Path
import re

cov_path = "coverage2"
table_path = "table_cov2"
output_path = "table_cov3"

for filename in os.listdir(cov_path):
    threshold = filename.split('_statistic_of_gro_coverage.csv')[0]
    df = pd.read_csv(cov_path + "/" + filename)
    maxid = max(df[['str1', 'str2']].applymap(lambda x: int(re.search(r'\d+$', x).group()) if pd.notnull(x) and re.search(r'\d+$', x) else 0).max())
    df['output'] = df.apply(lambda row: (row['str1'], row['str2'], 1) if row['precent of str1'] >= 0.5 or row['precent of str2'] >= 0.5 else None, axis=1)
    df = df.dropna(subset=['output'])
    if not df.empty:
        with open('temp.txt', 'w') as f:
            for row in df['output']:
                f.write(','.join(map(str, row)) + '\n')
                
        G = nx.read_edgelist('temp.txt', delimiter=',', nodetype=str, data=(('weight', int),))
        connected_components = list(nx.connected_components(G))

        table_df = pd.read_csv(f'{table_path}/{threshold}.csv')

        for i, component in enumerate(connected_components):
            for strid in component:
                table_df.replace(strid, f'group{maxid + 1 + i}', inplace=True)
                #print(f"{strid} structure{maxid + 1 + i}")

        Path(output_path).mkdir(parents=True, exist_ok=True)
        table_df.to_csv(f'{output_path}/{threshold}.csv', index=False)