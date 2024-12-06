import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# Load dataset

df = pd.read_csv('../sneakers.csv')

# Clean data (removing NaNs in important columns)
df_cleaned = df.dropna(subset=['collaboration_name', 'lowest_price_eur'])

# Optional: Filter out rows with irrelevant or missing collaboration names
df_cleaned = df_cleaned[df_cleaned['collaboration_name'].notnull()]
# Set plot size
plt.figure(figsize=(12, 6))

# Create the violin plot
sns.violinplot(x='collaboration_name', y='lowest_price_eur', data=df_cleaned)

# Set the plot title and labels
plt.title('Collaboration Influence on Sneaker Price (Violin Plot)', fontsize=16)
plt.xlabel('Collaboration Name', fontsize=12)
plt.ylabel('Lowest Price (EUR)', fontsize=12)

# Rotate x-axis labels for readability
plt.xticks(rotation=45, ha='right')

# Show plot
plt.tight_layout()
plt.show()