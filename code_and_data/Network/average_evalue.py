#根据cdhit聚类结果生成比对average e-value矩阵，而不是只用代表性序列比对
import re
import pandas as pd
import numpy as np

# 处理 all_gs2_0419_04.clstr 文件
cluster_file = '/home/zhangtm/Insect/Paper/Result-2/1-SSN/1-cdhit/final_OR_8912_0701_cdhit06.clstr'
cluster_data = {}
with open(cluster_file, 'r') as file:
    for line in file:
        if line.startswith('>Cluster'):
            cluster_id = int(line.split()[1])
        else:
            match = re.search(r'>(.*?)\.', line)
            if match:
                sequence_id = match.group(1)
                cluster_data[sequence_id] = cluster_id

# 处理 all_gs2_0419_annotation.txt 文件
annotation_file = 'final_OR_8912_0701_annotation.txt'
annotation_data = {}
with open(annotation_file, 'r') as file:
    for line in file:
        node_num, id = line.strip().split('\t')
        annotation_data[node_num] = id

# 读取 all_gs2_mmseqs_evalue_dedup.csv 文件
csv_file = 'final_OR_8912_0701_mmseqs_evalue_dedup.csv'
df = pd.read_csv(csv_file)

# 匹配 nodeA 和 nodeB 列中的数字
df['nodeA_num'] = df['nodeA'].str.extract('(\d+)', expand=False)
df['nodeB_num'] = df['nodeB'].str.extract('(\d+)', expand=False)

# 转换 nodeA 和 nodeB 为组号
df['nodeA'] = df['nodeA_num'].map(annotation_data).map(cluster_data)
df['nodeB'] = df['nodeB_num'].map(annotation_data).map(cluster_data)

# 添加 'node' 前缀
df['nodeA'] = 'node' + df['nodeA'].astype(str)
df['nodeB'] = 'node' + df['nodeB'].astype(str)

# 删除不再需要的 nodeA_num 和 nodeB_num 列
df.drop(['nodeA_num', 'nodeB_num'], axis=1, inplace=True)

# 根据 nodeA 和 nodeB 分组求平均值
average_df = df.groupby(['nodeA', 'nodeB']).mean().reset_index()

# 输出结果到 average_cdhit04.csv 文件
output_file = 'final_OR_8912_0701_average_cdhit06.csv'
average_df.to_csv(output_file, index=False)