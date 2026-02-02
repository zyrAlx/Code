import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Load the table CSV file
table = pd.read_csv('fun_table/best_partition_OR_fun_modify_0723.table')

#输出文件夹
heatmapfold = "label_heatmap"
os.makedirs(heatmapfold, exist_ok=True)

# Initialize an empty DataFrame to hold the matrix
matrix_df = pd.DataFrame()

fun_file_path = "fun_anno/best_partition_OR_fun_modify_0723.csv"

# Process fun_anno files to get unique 'fun' labels
fun_df = pd.read_csv(fun_file_path)
fun_labels = fun_df['fun'].unique()
# Remove 'nofun' label
fun_labels_delnofun = fun_labels[fun_labels != 'nofun']

# Generate the name for the corresponding bonf file
bonf_file_path = 'fun_ttst/best_partition_OR_fun_modify_0723_significant_bonf.csv'

if os.path.exists(bonf_file_path):
    bonf_df = pd.read_csv(bonf_file_path)
    fungroup_label = bonf_df['label'].unique()
    
    # Initialize a temporary DataFrame for this iteration
    temp_df = pd.DataFrame(index=fungroup_label, columns=fun_labels_delnofun).fillna(0)
    for _, row in bonf_df.iterrows():
        label = row['label']
        t_stat = row['t_stat']
        fun_label = row['fun']  # Assuming 'fun' column exists in bonf_df for mapping
        
        # 过滤出'fun'列值为fun_label的行
        filtered_rows = table[table['fun'] == fun_label]
        # 如果label列存在于DataFrame中，则进行后续操作
        if label in filtered_rows.columns:
            # 从过滤后的行中选取label列，并计算平均值
            avg = filtered_rows[label].mean()
            # Normalize the average and update temp_df based on t_stat
            normalized_avg = (avg - filtered_rows[label].min()) / (filtered_rows[label].max() - filtered_rows[label].min())
            
            temp_df.at[label, fun_label] = normalized_avg if t_stat > 0 else normalized_avg - 1

    
# Ensure the matrix is filled with 0 for any NaN values
temp_df.fillna(0, inplace=True)

# Save the matrix to a CSV file
temp_df.to_csv(f'{heatmapfold}/pearson_rank_counts_filter-8_06_048_louvain_fungroup_AVG_normalization_label_0724.csv')

# Adjust font size
plt.rcParams['xtick.labelsize'] = 30
plt.rcParams['ytick.labelsize'] = 30

# Draw and save a clustered heatmap
plt.figure(figsize=(20, 16))

clustergrid = sns.clustermap(temp_df, figsize=(30, 20), cmap='vlag', center=0, metric='euclidean', method='ward', linewidths=.5)
    
# Rotate column labels for readability
plt.setp(clustergrid.ax_heatmap.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
# Ensure row labels are horizontal
plt.setp(clustergrid.ax_heatmap.get_yticklabels(), rotation=0)

# Automatically adjust layout
plt.tight_layout()

plt.savefig(f'{heatmapfold}/pearson_rank_counts_filter-8_06_048_louvain_fungroup_AVG_normalization_label_heatmap_0724.png')
