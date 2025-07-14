import pandas as pd   # ← this was missing!

# 5-year burden data (2019–2023)
data = {
    'Disease': ['Dengue', 'Chikungunya', 'Kala-azar', 'Filariasis'],
    '2019': [157315, 16441, 3328, 5500],
    '2020': [44585, 6761, 1169, 3000],
    '2021': [193245, 11542, 965, 2500],
    '2022': [233251, 20635, 834, 2300],
    '2023': [190000, 14000, 500, 2000]
}

df_burden = pd.DataFrame(data)
df_burden['Mean Burden'] = df_burden[['2019','2020','2021','2022','2023']].mean(axis=1).astype(int)

# Load your attention table
df_attention = pd.read_csv('data/clean/ntd_attention_table_with_totals.csv')

# Merge on Disease
df_merged = pd.merge(df_burden[['Disease','Mean Burden']], df_attention, on='Disease', how='outer')

# Fill missing attention with zeros
df_merged[['YouTube Mentions','Google News Mentions','Total Attention']] = df_merged[['YouTube Mentions','Google News Mentions','Total Attention']].fillna(0).astype(int)

# Save
df_merged.to_csv('data/clean/ntd_burden_attention_merged.csv', index=False)

# Print
print(df_merged)
