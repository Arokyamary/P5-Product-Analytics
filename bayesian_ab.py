import pymc as pm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    users = pd.read_csv('data/users.csv')
    A = users[users['variant']=='A']
    B = users[users['variant']=='B']
    n_A, conv_A = len(A), A['converted'].sum()
    n_B, conv_B = len(B), B['converted'].sum()

    print(f'Control A: {conv_A}/{n_A} = {conv_A/n_A*100:.2f}%')
    print(f'Variant B: {conv_B}/{n_B} = {conv_B/n_B*100:.2f}%')

    with pm.Model() as ab_model:
        p_A = pm.Beta('p_A', alpha=1, beta=1)
        p_B = pm.Beta('p_B', alpha=1, beta=1)
        obs_A = pm.Binomial('obs_A', n=n_A, p=p_A, observed=conv_A)
        obs_B = pm.Binomial('obs_B', n=n_B, p=p_B, observed=conv_B)
        lift = pm.Deterministic('lift', (p_B - p_A) / p_A)
        trace = pm.sample(2000, tune=1000, return_inferencedata=True, progressbar=True, chains=2)

    p_B_better = float((trace.posterior['p_B'].values > trace.posterior['p_A'].values).mean())
    print(f'P(B > A) = {p_B_better*100:.1f}%')

    if p_B_better > 0.90:
        print('DECISION: SHIP Variant B!')
    elif p_B_better > 0.70:
        print('DECISION: Promising - collect more data.')
    else:
        print('DECISION: Insufficient evidence.')

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(trace.posterior['p_A'].values.flatten(), bins=50, alpha=0.7, label='Control A')
    axes[0].hist(trace.posterior['p_B'].values.flatten(), bins=50, alpha=0.7, label='Variant B')
    axes[0].set_title('Posterior Conversion Rates')
    axes[0].legend()
    axes[1].hist(trace.posterior['lift'].values.flatten()*100, bins=50, alpha=0.7)
    axes[1].axvline(x=0, color='red', linestyle='--')
    axes[1].set_title('Expected Lift (%)')
    plt.savefig('bayesian_posteriors.png', dpi=150, bbox_inches='tight')
    print('Saved bayesian_posteriors.png')