import pandas as pd  # <== You must import pandas first!

df = pd.read_csv('data/clean/ntd_attention_table.csv')
df['Total Attention'] = df['YouTube Mentions'] + df['Google News Mentions']
print(df)

# Save to CSV if you like
df.to_csv('data/clean/ntd_attention_table_with_totals.csv', index=False)
print("\nSaved to data/clean/ntd_attention_table_with_totals.csv")
