import pandas as pd

# Load merged file
df = pd.read_csv('data/clean/ntd_burden_attention_merged.csv')

# Standardize spelling: always "Kala-azar"
df['Disease'] = df['Disease'].str.replace('Kala Azar', 'Kala-azar')

# Group by Disease to collapse duplicates
df = df.groupby('Disease', as_index=False).sum(numeric_only=True)

# Reorder columns
df = df[['Disease', 'Mean Burden', 'YouTube Mentions', 'Google News Mentions', 'Total Attention']]

# Fill NaN Mean Burden with 0
df['Mean Burden'] = df['Mean Burden'].fillna(0).astype(int)

# Save cleaned version
df.to_csv('data/clean/ntd_burden_attention_final.csv', index=False)

print(df)
