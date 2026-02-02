import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize an empty DataFrame to hold the matrix
matrix_df = pd.DataFrame()

# Path to the 'fun_anno' and 'fun_ttst' folders
fun_anno_path = 'fun_anno'
fun_ttst_path = 'fun_ttst'
os.makedirs("fungroup_label", exist_ok=True)
os.makedirs("label_heatmap", exist_ok=True)

# List all files in the 'fun_anno' folder
fun_anno_files = os.listdir(fun_anno_path)

for file in fun_anno_files:
    # Process fun_anno files to get unique 'fun' labels
    fun_file_path = os.path.join(fun_anno_path, file)
    fun_df = pd.read_csv(fun_file_path)
    fun_labels = fun_df['fun'].unique()
    #删掉nofun标签
    fun_labels_delnofun = fun_labels[fun_labels != 'nofun']
    filename = os.path.splitext(file)[0]
    
    # Generate the name for the corresponding bonf file
    bonf_file_name = filename + '_significant_bonf.csv'
    bonf_file_path = os.path.join(fun_ttst_path, bonf_file_name)
    
    if os.path.exists(bonf_file_path):
        bonf_df = pd.read_csv(bonf_file_path)
        fungroup_label = bonf_df['label'].unique()

        # Initialize a temporary DataFrame for this iteration
        temp_df = pd.DataFrame(index=fungroup_label, columns=fun_labels_delnofun).fillna(0)
        for _, row in bonf_df.iterrows():
            label = row['label']
            t_stat = row['t_stat']
            fun_label = row['fun']  # Assuming 'fun' column exists in bonf_df for mapping
            
            # Assign values based on t_stat
            temp_df.at[label, fun_label] = 1 if t_stat > 0 else -1
        
    # Ensure the matrix is filled with 0 for any NaN values
    temp_df.fillna(0, inplace=True)

    # Save the matrix to a CSV file
    temp_df.to_csv(f'fungroup_label/{filename}_label.csv')
    
    #事先调整字体大小
    plt.rcParams['xtick.labelsize'] = 30
    plt.rcParams['ytick.labelsize'] = 30


    # Draw and save a clustered heatmap
    plt.figure(figsize=(20, 16))

    clustergrid = sns.clustermap(temp_df, figsize=(15, 20), cmap='vlag', center=0, metric='euclidean', method='ward', linewidths=.5)
        
    
    # Rotate column labels for readability
    plt.setp(clustergrid.ax_heatmap.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    # Ensure row labels are horizontal
    plt.setp(clustergrid.ax_heatmap.get_yticklabels(), rotation=0)
    
    #自动调整布局
    plt.tight_layout()
    
    plt.savefig(f'label_heatmap/{filename}_label_heatmap.png')