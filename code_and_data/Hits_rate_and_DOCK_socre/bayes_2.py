import stan
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns

data_array = pd.read_csv('random_sampling.csv')

data_array['mean'] = data_array[['Sampling_1', 'Sampling_2', 'Sampling_3', 'Sampling_4']].mean(axis=1)
data_array['std'] = data_array[['Sampling_1', 'Sampling_2', 'Sampling_3', 'Sampling_4']].std(axis=1)

long_df = data_array.melt(id_vars=['energy'], value_vars=['Sampling_1', 'Sampling_2', 'Sampling_3', 'Sampling_4'], 
                  var_name='sample', value_name='value')

x_sample = long_df['energy'].tolist()
y_sample = long_df['value'].tolist()

stan_code = """
data {
    int<lower=0> N;
    vector[N] x;
    vector[N] y;
}

parameters {
    real<lower=0, upper=1> Top;
    real<upper=0> S;
    real Dock50;
}

model {
    Top ~ beta(20, 80);
    Dock50 ~ normal(-5, 15);
    S ~ normal(-0.6, 0.1);
    
    y ~ normal(Top ./ (1 + exp(-S .* (x - Dock50))), 0.1);  
}
"""

data = {
    'N': len(x_sample),
    'x': x_sample,
    'y': y_sample
}
posterior = stan.build(stan_code,data=data,random_seed=101)

fit = posterior.sample(num_samples=100000, 
                  num_chains=4, 
                  num_warmup=50000, 
                  #adapt_delta=0.99, 
                  max_depth=12)
                  

Top_samples = fit['Top'][0]
S_samples = fit['S'][0]
Dock50_samples = fit['Dock50'][0]

# Plotting
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 12))

# Top Parameter
x = np.linspace(0, 0.4, 100)
axes[0].plot(x, stats.beta.pdf(x, 20, 80), 'r-', label='Prior: Beta(20, 80)')
sns.kdeplot(Top_samples, ax=axes[0], alpha=0.6, label='Posterior')
axes[0].set_title('Top')
axes[0].legend()

# S Parameter
x = np.linspace(-2, 0, 100)
axes[1].plot(x, stats.norm.pdf(x, -1, 0.1), 'r-', label='Prior: Normal(-5, 15)')
sns.kdeplot(S_samples, ax=axes[1], alpha=0.6, label='Posterior')
axes[1].set_title('S')
axes[1].legend()

# Dock50 Parameter
x = np.linspace(-40, 40, 100)
axes[2].plot(x, stats.norm.pdf(x, -5, 15), 'r-', label='Prior: Normal(-0.2, 0.1)')
sns.kdeplot(Dock50_samples, ax=axes[2], alpha=0.6, label='Posterior')
axes[2].set_title('Dock50')
axes[2].legend()

plt.savefig("3sample_canshu.png", dpi=300, bbox_inches='tight')
#plt.show()


x_values = np.linspace(-30, 10, 100)
plt.figure(figsize=(12, 8))

plt1 = plt.gca()
plt2 = plt.gca().twinx()

for i in range(500): 
    y_pred = Top_samples[i] / (1 + np.exp(-S_samples[i] * (x_values - Dock50_samples[i])))
    plt2.plot(x_values, y_pred, color='gray', alpha=0.1, linewidth=2)


all_data = np.loadtxt('all_OR_dock_exp.txt')
sns.kdeplot(all_data, ax=plt1, color='black', lw=8)

Top_mean = np.mean(Top_samples)
S_mean = np.mean(S_samples)
Dock50_mean = np.mean(Dock50_samples)
y_mean_pred = Top_mean / (1 + np.exp(-S_mean * (x_values - Dock50_mean)))
plt2.plot(x_values, y_mean_pred, color='#FF2F91', linewidth=8)

plt2.errorbar(data_array['energy'], data_array['mean'], yerr=data_array['std'], fmt='o', label='sample Data average', markersize=30, capsize=20,elinewidth=10, color='#8DF900')


#plt.scatter(x_sample, y_sample, c='red', marker='o')  # 原始数据点

plt1.set_ylim(0, 0.1)
plt2.set_ylim(0, 0.35)
plt2.set_xlim(-30, 10)

#plt2.set_ylabel('Density', fontsize=20)
plt2.tick_params(axis='y', labelsize=20)
plt1.tick_params(axis='y', labelsize=20)
plt1.tick_params(axis='x', labelsize=20)
plt.savefig('3sample_out2.png', dpi=300, bbox_inches='tight')
#plt.show()