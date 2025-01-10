import pandas as pd

# Load datasets
grafik_verileri = pd.read_csv('cleaned_data/Grafik verileri.csv')
monthly_comparison = pd.read_csv('cleaned_data/monthly_comparison.csv')

# Ensure the date column in the YouTube data is in datetime format
grafik_verileri['Tarih'] = pd.to_datetime(grafik_verileri['Tarih'])

# Calculate monthly YouTube viewership by summing views grouped by month
grafik_verileri['Month'] = grafik_verileri['Tarih'].dt.month
monthly_youtube_views = (
    grafik_verileri.groupby('Month')['Görüntüleme']
    .sum()
    .reset_index()
    .rename(columns={'Görüntüleme': 'Monthly YouTube Views'})
)

# Merge monthly YouTube views with the student gain data
combined_data = pd.merge(monthly_comparison, monthly_youtube_views, on='Month', how='inner')

# Save the combined data to a CSV file
combined_data.to_csv('combined_data.csv', index=False)

# Calculate the correlation between monthly YouTube views and student gain
correlation = combined_data['Monthly YouTube Views'].corr(combined_data['Student Gain'])

# Save the correlation result to a text file
with open('correlation_result.txt', 'w') as f:
    f.write(f"Correlation between Monthly YouTube Views and Student Gain: {correlation}")
