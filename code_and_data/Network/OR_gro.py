import pandas as pd
import os
import re

df = pd.read_csv('1e-25_new_0702.csv')

cluster_dict = {}
current_cluster_key = None
current_cluster_list = []

with open("/home/zhangtm/Insect/Paper/Result-2/1-SSN/1-cdhit/final_OR_8912_0701_cdhit06.clstr", 'r') as file:
    for line in file:
        # Check if the line indicates a new cluster
        if line.startswith('>Cluster'):
            # If we have been collecting a cluster, save it before starting a new one
            if current_cluster_key and current_cluster_list:
                cluster_dict[current_cluster_key] = current_cluster_list
                current_cluster_list = []  # Reset the list for the next cluster
            # Extract the cluster number and create a new key
            num = re.findall(r'Cluster (\d+)', line)[0]
            current_cluster_key = f"node{num}"
        else:
            # Extract the string between '>' and '...'
            match = re.search(r'>([^\.]+)\.\.\.', line)
            if match:
                current_cluster_list.append(match.group(1))

# Add the last cluster to the dictionary if it exists
if current_cluster_key and current_cluster_list:
    cluster_dict[current_cluster_key] = current_cluster_list

not_in_df_keys = set(cluster_dict.keys()) - set(df['node'].tolist())

fun_dict = {}

for index, row in df.iterrows():
    cluster = row['node']
    fun = row['family']
    ORs = cluster_dict.get(cluster, [])
    if fun in fun_dict:
        fun_dict[fun].extend(ORs)
    else:
        fun_dict[fun] = ORs

max_structure_num = max([int(fun.split('group')[1]) for fun in fun_dict.keys() if 'group' in fun], default=0)
keys_to_remove = set()
for key in not_in_df_keys:
    if len(cluster_dict[key]) >= 20 and key not in df['node'].values:
        max_structure_num += 1
        fun_dict[f'group{max_structure_num}'] = cluster_dict[key]
        keys_to_remove.add(key)

not_in_df_keys -= keys_to_remove

with open("1e-25_OR_gro_20240702.csv", 'w') as f:
    f.write("OR,gro\n")
    for fun, ORs in fun_dict.items():
        for OR in ORs:
            f.write(f"{OR},{fun}\n")
    
    for key in not_in_df_keys:
        for nofun_OR in cluster_dict[key]:
            f.write(f"{nofun_OR},nogro\n")