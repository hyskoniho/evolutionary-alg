import pandas as pd


df = pd.read_csv(r'.\data\produtos.csv', sep='|', encoding='utf-8')
print(list(df['categoria'].unique()))