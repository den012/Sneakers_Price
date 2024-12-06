import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
# Replace 'your_dataset.csv' with your file name or dataset
df = pd.read_csv('../sneakers.csv')

# Select relevant columns for the correlation matrix
columns_to_analyze = ['days_since_release', 'collaboration', 'retail_price_eur', 'gp_lowest_price_eur']
correlation_data = df[columns_to_analyze]

# Compute the correlation matrix
correlation_matrix = correlation_data.corr()

# Plot the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.show()