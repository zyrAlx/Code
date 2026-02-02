import pandas as pd
import numpy as np
import scipy.stats as stats

df1 = pd.read_csv('Species_fun_matrix.csv')
df2 = pd.read_csv('all_115sp_habit_label_0715.csv')

table = pd.merge(df1, df2, on='Species', how='left')

grouped = table.groupby(['adult','larval','circadian','habitat']).sum()
grouped = grouped.drop(columns=['OR','nofun'])

df = grouped

def wilson_score_interval(p, n, alpha=0.05):
    z = stats.norm.ppf(1 - alpha / 2)
    denominator = 1 + z**2/n
    centre_adjusted_probability = p + z**2 / (2*n)
    adjusted_standard_deviation = np.sqrt((p*(1 - p) + z**2 / (4*n)) / n)
    
    lower_bound = (centre_adjusted_probability - z*adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z*adjusted_standard_deviation) / denominator
    
    return [round(lower_bound, 3), round(upper_bound, 3)]

order_totals = df.sum(axis=1)

wilson_scores = {}
lower_bounds = {}

for order in df.index:
    wilson_scores[order] = {}
    lower_bounds[order] = {}
    for function in df.columns:
        p = df.at[order, function] / order_totals[order]
        wilson_scores[order][function] = wilson_score_interval(p, order_totals[order])
        bounds = wilson_score_interval(p, order_totals[order])
        lower_bounds[order][function] = bounds[0]  
        
        

wilson_df = pd.DataFrame(wilson_scores).T
lower_bounds_df = pd.DataFrame(lower_bounds).T * 100 
lower_bounds_df = lower_bounds_df.round(1) 

gro_df = lower_bounds_df

gro_df = gro_df.sort_index(axis=1)

gro_matrix = gro_df.T.to_numpy()

phe_df = pd.read_csv('pearson_rank_counts_filter-8_06_048_louvain_fungroup_AVG_normalization_label_0724.csv', index_col=0)

#phe_df.replace({-1: 0, 0: 0.5}, inplace=True)

phe_df = phe_df.reindex(columns=gro_df.columns)

pheromone_matrix = phe_df.to_numpy()

result_matrix = np.dot(pheromone_matrix, gro_matrix)

result_matrix_rounded = np.round(result_matrix, 1)

result_df = pd.DataFrame(result_matrix_rounded, index=phe_df.index, columns=gro_df.index)

result_df = result_df.drop(index=['OTHERS'])

result_df = result_df.T

result_df.to_csv(f'all_life_history_fungroup_BPS_perfomance_AVG_normalization_label.csv')
