import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:admin123@localhost:5432/product_analytics')

pd.read_csv('data/events.csv').to_sql('events', engine, if_exists='replace', index=False)
pd.read_csv('data/users.csv').to_sql('users', engine, if_exists='replace', index=False)

print('Loaded events and users to PostgreSQL')