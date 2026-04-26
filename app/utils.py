import pandas as pd
import os

def load_all_data():
    countries = ['ethiopia', 'kenya', 'sudan', 'tanzania', 'nigeria']
    dfs = []
    for c in countries:
        path = f'data/{c}_clean.csv'
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=['Date'])
            dfs.append(df)
    return pd.concat(dfs) if dfs else pd.DataFrame()

def filter_data(df, selected_countries, start_year, end_year):
    df = df[df['Country'].isin(selected_countries)]
    df = df[(df['Date'].dt.year >= start_year) & (df['Date'].dt.year <= end_year)]
    return df