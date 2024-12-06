# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# # Example data loading (replace with your own dataset if needed)
# df = pd.read_csv('../sneakers.csv')
#
# # Remove rows with missing values in key columns
# df_clean = df.dropna(subset=['days_since_release', 'lowest_price_eur'])
#
# # Create the KDE plot
# plt.figure(figsize=(12, 6))
#
# # KDE Plot for joint distribution of days and prices
# sns.kdeplot(
#     data=df_clean,
#     x='days_since_release',
#     y='lowest_price_eur',
#     cmap='Blues',  # Color map for the density
#     fill=True,     # Fill under the density curves
#     alpha=0.7,     # Transparency for the fill
#     levels=30      # Number of contour levels
# )
#
# # Customize the plot
# plt.title('Sneaker Price Density Over Time (KDE)')
# plt.xlabel('Days Since Release')
# plt.ylabel('Lowest Price (EUR)')
# plt.grid(True)
# plt.tight_layout()
#
# # Show the plot
# plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example data loading (replace with your dataset)
df = pd.read_csv('../sneakers.csv')

# Remove rows with missing values
df_clean = df.dropna(subset=['days_since_release', 'lowest_price_eur'])

# Create the plot
plt.figure(figsize=(12, 6))

# Polynomial Regression Plot with Confidence Interval
sns.regplot(
    data=df_clean,
    x='days_since_release',
    y='lowest_price_eur',
    order=3,      # Polynomial degree (adjust for more curvature)
    scatter=False, # No scatter points, just the curve
    ci=100,         # Confidence interval 100% by default)
    color='blue'   # Curve color
)

# Optional: Scatter for actual data points (if desired)
sns.scatterplot(
    data=df_clean,
    x='days_since_release',
    y='lowest_price_eur',
    alpha=0.5,
    color='gray',
    label='Actual Prices'
)

# Customize the plot
plt.title('Smoothed Sneaker Price Trend Over Time with 100% CI')
plt.xlabel('Days Since Release')
plt.ylabel('Lowest Price (EUR)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
