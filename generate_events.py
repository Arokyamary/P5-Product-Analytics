import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)
n_users = 50000

users = pd.DataFrame({
    'user_id': range(n_users),
    'variant': np.random.choice(['A','B'], n_users),
    'signup_date': pd.date_range('2024-01-01', periods=n_users, freq='1min'),
    'device': np.random.choice(['mobile','desktop','tablet'], n_users, p=[0.65,0.30,0.05]),
    'city': np.random.choice(['Bengaluru','Mumbai','Delhi','Chennai'], n_users),
})

# Variant B converts 33% better than A
users['converted'] = users.apply(
    lambda r: np.random.random() < (0.08 if r['variant']=='B' else 0.06), axis=1
)

events = []
for _, u in users.iterrows():
    t = u['signup_date']
    events.append({'user_id':u.user_id,'event':'landing','ts':t,'variant':u.variant})
    if np.random.random() < 0.65:
        events.append({'user_id':u.user_id,'event':'product_view','ts':t+pd.Timedelta(seconds=30),'variant':u.variant})
    if np.random.random() < 0.40:
        events.append({'user_id':u.user_id,'event':'add_to_cart','ts':t+pd.Timedelta(seconds=90),'variant':u.variant})
    if np.random.random() < 0.30:
        events.append({'user_id':u.user_id,'event':'checkout','ts':t+pd.Timedelta(seconds=180),'variant':u.variant})
    if u.converted:
        events.append({'user_id':u.user_id,'event':'purchase','ts':t+pd.Timedelta(seconds=240),'variant':u.variant})

events_df = pd.DataFrame(events)
users.to_csv('data/users.csv', index=False)
events_df.to_csv('data/events.csv', index=False)
print(f'Generated {len(events_df):,} events for {n_users:,} users')
print(f'Control A CVR: {users[users.variant=="A"].converted.mean()*100:.1f}%')
print(f'Variant B CVR: {users[users.variant=="B"].converted.mean()*100:.1f}%')