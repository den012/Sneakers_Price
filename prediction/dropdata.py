import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the Data
file_path = './filtered_file.csv'  # Path to your CSV file
data = pd.read_csv(file_path)

# Step 2: Calculate IQR for retail prices under 400 EUR
# Filter for prices under 400 EUR

# Calculate Q1 (25th percentile) and Q3 (75th percentile)
Q1 = data['instant_ship_lowest_price_eur'].quantile(0.25)
Q3 = data['instant_ship_lowest_price_eur'].quantile(0.75)
IQR = Q3 - Q1

# Determine bounds for filtering
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter the data using IQR
iqr_filtered_data = data[(data['instant_ship_lowest_price_eur'] >= lower_bound) & 
                                   (data['instant_ship_lowest_price_eur'] <= upper_bound)]

# Step 3: Plotting the Distribution
plt.figure(figsize=(12, 6))

# Box Plot
plt.figure(figsize=(12, 6))
sns.boxplot(x=iqr_filtered_data['instant_ship_lowest_price_eur'], color='lightblue')
plt.title('Out of bounds data')
plt.xlabel('Price (EUR)')
plt.grid()
plt.tight_layout()
plt.show()
