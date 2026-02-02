import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


file_path = 'all_life_history_fungroup_BPS_perfomance_AVG_normalization_label.csv'
df = pd.read_csv(file_path)


#df = df.drop(columns=['OTHERS'])


features = df.drop(columns=['adult', 'larval','circadian','habitat'])
labels = df[['adult', 'larval','circadian','habitat']]


scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)


pca = PCA(n_components=2)
features_pca = pca.fit_transform(features_scaled)


tsne = TSNE(n_components=2)
features_tsne = tsne.fit_transform(features_scaled)


pca_df = pd.DataFrame(features_pca, columns=['PCA1', 'PCA2'])
tsne_df = pd.DataFrame(features_tsne, columns=['tSNE1', 'tSNE2'])

pca_df['adult'] = labels['adult']
pca_df['larval'] = labels['larval']
pca_df['circadian'] = labels['circadian']
pca_df['habitat'] = labels['habitat']
tsne_df['adult'] = labels['adult']
tsne_df['larval'] = labels['larval']
tsne_df['circadian'] = labels['circadian']
tsne_df['habitat'] = labels['habitat']


pca_df.to_csv('pca_results.csv', index=False)
tsne_df.to_csv('tsne_results.csv', index=False)
