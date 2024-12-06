import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('../sneakers.csv')

# Calculate the deviation
df['price_deviation'] = df['gp_lowest_price_eur'] - df['retail_price_eur']

# Set a threshold for anomalies
threshold = df['price_deviation'].std() * 2  # Example: 2 standard deviations
anomalies = df[abs(df['price_deviation']) > threshold]

# Plot the scatter plot
plt.figure(figsize=(12, 8))
plt.scatter(df['retail_price_eur'], df['gp_lowest_price_eur'], alpha=0.7, label='Normal Data')
plt.scatter(anomalies['retail_price_eur'], anomalies['gp_lowest_price_eur'], color='red', label='Anomalies')

# Add annotations for anomalies
for _, row in anomalies.iterrows():
    plt.annotate(
        row['days_since_release'],
        (row['retail_price_eur'], row['gp_lowest_price_eur']),
        textcoords="offset points", xytext=(5, 5), ha='center'
    )

plt.axline((0, 0), slope=1, color='gray', linestyle='--', label='Expected Equality Line')
plt.xlabel('Retail Price (EUR)')
plt.ylabel('Market Price (gp_lowest_price_eur)')
plt.title('Market Misinformation Indicators')
plt.legend()
plt.show()