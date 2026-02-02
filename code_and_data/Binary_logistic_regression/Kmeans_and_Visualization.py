import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from matplotlib.patches import Ellipse
from sklearn.covariance import MinCovDet
from scipy.stats import chi2

pca_df = pd.read_csv('pca_results.csv')
tsne_df = pd.read_csv('tsne_results.csv')

kmeans_pca = KMeans(n_clusters=3, random_state=42)
clusters_pca = kmeans_pca.fit_predict(pca_df[['PCA1', 'PCA2']])

kmeans_tsne = KMeans(n_clusters=3, random_state=42)
clusters_tsne = kmeans_tsne.fit_predict(tsne_df[['tSNE1', 'tSNE2']])

pca_df['Cluster'] = clusters_pca
tsne_df['Cluster'] = clusters_tsne

def draw_minimum_ellipse(ax, points, edgecolor, confidence_level=0.8):
    if points.shape[0] < 3:
        return 

    mcd = MinCovDet(random_state=0).fit(points)
    mean = mcd.location_
    cov = mcd.covariance_

    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    order = eigenvalues.argsort()[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]

    vx, vy = eigenvectors[:, 0][0], eigenvectors[:, 0][1]
    theta = np.arctan2(vy, vx)
    theta = np.degrees(theta)

    chi_square_val = chi2.ppf(confidence_level, df=2)
    width, height = 2 * np.sqrt(eigenvalues * chi_square_val)
    ellip = Ellipse(xy=mean, width=width, height=height, angle=theta, edgecolor=edgecolor, fc='None', lw=2, ls='--')
    ax.add_patch(ellip)

confidence_level = 0.90 

plt.figure(figsize=(24, 8))

ax1 = plt.subplot(1, 2, 1)
scatter1 = ax1.scatter(pca_df['PCA1'], pca_df['PCA2'], c=pca_df['Cluster'], cmap='viridis', marker='o', edgecolor='k', s=500)
plt.title('K-means Clustering on PCA Results')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.colorbar(scatter1, ax=ax1, label='Cluster')

for cluster in range(kmeans_pca.n_clusters):
    points = pca_df[pca_df['Cluster'] == cluster][['PCA1', 'PCA2']].values
    draw_minimum_ellipse(ax1, points, 'k', confidence_level=confidence_level)

ax2 = plt.subplot(1, 2, 2)
scatter2 = ax2.scatter(tsne_df['tSNE1'], tsne_df['tSNE2'], c=tsne_df['Cluster'], cmap='viridis', marker='o', edgecolor='k', s=500)
plt.title('K-means Clustering on t-SNE Results')
plt.xlabel('tSNE1')
plt.ylabel('tSNE2')
plt.colorbar(scatter2, ax=ax2, label='Cluster')

for cluster in range(kmeans_tsne.n_clusters):
    points = tsne_df[tsne_df['Cluster'] == cluster][['tSNE1', 'tSNE2']].values
    draw_minimum_ellipse(ax2, points, 'k', confidence_level=confidence_level)

plt.tight_layout()
plt.savefig('kmeans_clustering_results_with_minimum_ellipses.png')
#plt.show()

#pca_df.to_csv('kmeans_pca_clustering_results.csv', index=False)
tsne_df.to_csv('kmeans_tsne_clustering_results.csv', index=False)
