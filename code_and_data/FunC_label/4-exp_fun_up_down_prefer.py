import pandas as pd
import os

# 读取paper_and_anno.csv文件到DataFrame A
A = pd.read_csv('paper_and_anno.csv')

# 指定fun_anno文件夹路径
anno_path = 'fun_anno'
label_path = "fungroup_label"

#实验物种
species = "Dm"
down_threshold = -1000

#输出文件夹
outputfold = f"paper_OR_prefer/{down_threshold}"
os.makedirs(outputfold, exist_ok=True)

# 遍历fun_anno文件夹中的所有文件
for file in os.listdir(anno_path):
    file_path = os.path.join(anno_path, file)
    filename = os.path.splitext(file)[0]
    # 确保是文件而不是文件夹
    if os.path.isfile(file_path):
        # 读取当前文件到DataFrame B
        B = pd.read_csv(file_path)
        # 将B的OR列左连接到A的anno列
        expOR_family_df = pd.merge(A, B, left_on='anno', right_on='OR', how='left')
        
    # 读取fun注释文件并创建字典
    expOR_family = dict(zip(expOR_family_df['paper'], expOR_family_df['fun']))
    
    # 读取标签label文件为 matrix，列名更正为 fungroup
    matrix = pd.read_csv(f'{label_path}/{filename}_label.csv', index_col=0)
    #划分table的时候跟之前脚本搞反了，这里需要转置一下
    matrix = matrix.T
    # 读取 Dm_exp_matrix.csv 文件
    Dm_exp_matrix = pd.read_csv(f'exp_matrix/{species}_exp_matrix.csv')
    
    # 初始化输出数据结构
    output_data = []
    
    # 处理每个fungroup
    for fungroup_label in matrix.columns:
        # 初始化存储每个fungroup下的total_count
        fungroup_counts = {'up': [], 'mid': [], 'down': []}
        # 筛选出 fungroup 列等于 fungroup_label 的行
        filtered_df = Dm_exp_matrix[Dm_exp_matrix['fungroup'] == fungroup_label]
        # 遍历每个OR并计算total_count
        for or_name in Dm_exp_matrix.columns[2:]:
            # 获取当前OR对应的fun
            fun = expOR_family.get(or_name)
            if fun is not None and fun in matrix.index:
                # 计算当前OR的total_count
                total_count = (filtered_df[or_name] > 50).sum() + (filtered_df[or_name] < down_threshold).sum()
                #total_count = (filtered_df[or_name] > 50).sum()
                #total_count = (filtered_df[or_name] == 1).sum()
                
                # 确定当前fun在当前fungroup下的分类（up, mid, down）
                label_value = matrix.loc[fun, fungroup_label]
                if label_value == 1:
                    prefer = 'up'
                elif label_value == 0:
                    prefer = 'mid'
                else:  # label_value == -1
                    prefer = 'down'
                
                # 将total_count添加到对应的分类下
                fungroup_counts[prefer].append(total_count)
        
        # 将当前fungroup的结果添加到输出数据
        for prefer, counts in fungroup_counts.items():
            if counts:  # 只有当有计数时才添加
                total_count_str = ",".join(map(str, counts))
                output_data.append([fungroup_label, prefer, total_count_str])
    
    # 将结果保存到CSV文件
    output_df = pd.DataFrame(output_data, columns=['fungroup', 'prefer', 'total_count'])
    output_df.to_csv(f'{outputfold}/{filename}_{species}50{down_threshold}.csv', index=False)

    print(f'{filename}文件已保存')
