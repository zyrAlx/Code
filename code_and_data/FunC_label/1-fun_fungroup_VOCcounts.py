import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind


# 1.读取CID_label.csv
label_df = pd.read_csv('CID_label.csv',dtype={"CID": float})

# 初始化结果数组
result = []

os.makedirs("fun_table", exist_ok=True)


# 遍历no-ORco文件夹下的所有文件
directory = '/home/zhangtm/Insect/Paper/Result-5/1-FSN/8792_noORco_DOCK'
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        data_df = pd.read_csv(file_path,dtype={"CIDname": float})
    
        # 检查数据行数，去掉空文件
        if data_df.shape[0] == 0: 
            continue  # 跳过此文件
            
        # 对每个文件名进行处理，提取ORname
        ORname = filename.split('_score')[0]
        
        # 删除score列大于-8的行
        data_df = data_df[data_df['score'] <= -8]
        
        # 与label列表左连接
        data_df['CIDname'] = data_df['CIDname'].astype(str)
        label_df['CID'] = label_df['CID'].astype(str)
        merged_df = data_df.merge(label_df, left_on='CIDname', right_on='CID', how='left')
        
        # 根据label进行分组，计算每组的数量
        counts = merged_df.groupby('label').size().reset_index(name='count')
        counts['OR'] = ORname
        result.append(counts)

# 转化为一个大的DataFrame
result_df = pd.concat(result, axis=0)

# 整合数据，长变宽
pivot_df = result_df.pivot_table(index='OR', columns='label', values='count', fill_value=0).reset_index()

# 注释文件所在文件夹
fun_anno_path = 'fun_anno'
fun_anno_files = os.listdir(fun_anno_path)

# 遍历所有类型的功能社团注释文件
for file in fun_anno_files:
    file_path = os.path.join(fun_anno_path, file)
    
    # Load each file
    anno_df = pd.read_csv(file_path)
    
    filename = os.path.splitext(file)[0]
    # 与asg_df合并，添加asg标签
    merged_df = pivot_df.merge(anno_df, left_on='OR', right_on='OR', how='left')

    #输出
    merged_df.to_csv(f"fun_table/{filename}.table", index=False)
