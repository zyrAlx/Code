import pandas as pd
from scipy import stats
import numpy as np
import os

# 注释文件所在文件夹
fun_anno_path = 'fun_table'
fun_anno_files = os.listdir(fun_anno_path)
outfold = "fun_ttst"

os.makedirs(f"{outfold}", exist_ok=True)

# 遍历所有类型的功能社团注释文件
for file in fun_anno_files:
    file_path = os.path.join(fun_anno_path, file)
    
    # Load each file
    df = pd.read_csv(file_path)
    
    filename = os.path.splitext(file)[0]
    
    # 列名提取，第二列到第11列
    labels = df.columns[1:11]  # 调整索引以匹配实际列位置

    # 结果容器
    results = []

    # 遍历每一个label
    for label in labels:
        # B: 不分组的数据
        B = df[label]
        
        # 获取独特的fun列表,去掉nofunction
        families = df['fun'].unique()
        families = [f for f in families if f != 'nofun']
        
        # 对每一个fun进行循环
        for fun in families:
            # A: 当前fun的数据
            A = df[df['fun'] == fun][label]
            
            # 执行t检验
            t_stat, p_val = stats.ttest_ind(A, B, equal_var=False)  # 使用Welch's t-test，因为我们不能假设方差相等
            
            # 添加到结果中（先不进行Bonferroni修正）
            results.append({'label': label, 'fun': fun, 't_stat': t_stat, 'p_val': p_val})

    # 转换为DataFrame
    results_df = pd.DataFrame(results)

    # Bonferroni修正：调整p值
    adjusted_p_vals = results_df['p_val'] * len(results_df)  # 总测试数作为乘数
    results_df['adjusted_p_val'] = np.minimum(adjusted_p_vals, 1)  # 修正后的p值不能超过1

    # 输出检验结果
    results_df.to_csv(f"{outfold}/{filename}_background_bonf.csv", index=False)

    #筛选具有显著性的function
    significant_results = results_df[results_df['adjusted_p_val'] < 0.05]

    # 输出显著性检验结果
    significant_results.to_csv(f"{outfold}/{filename}_significant_bonf.csv", index=False)
    