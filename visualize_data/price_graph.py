# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# file_path = '../sneakers.json'
# data = pd.read_json(file_path)
#
# # Define an array with the price fields
# price_fields = [
#     'retail_price_eur',
#     'lowest_price_eur',
#     'gp_lowest_price_eur'
# ]
#
# # Step 2: Calculate IQR for each price field and filter the data
# filtered_data = data.copy()
#
# for price_field in price_fields:
#     # Calculate Q1 (25th percentile) and Q3 (75th percentile)
#     Q1 = data[price_field].quantile(0.25)
#     Q3 = data[price_field].quantile(0.75)
#     IQR = Q3 - Q1
#
#     # Determine bounds for filtering
#     lower_bound = Q1 - 1.5 * IQR
#     upper_bound = Q3 + 1.5 * IQR
#
#     # Filter the data using IQR
#     filtered_data = filtered_data[(filtered_data[price_field] >= lower_bound) &
#                                   (filtered_data[price_field] <= upper_bound)]
#
# # Step 3: Plotting the Curved Line
# plt.figure(figsize=(12, 6))
#
# # Scatter Plot with Curved Line for each price field
# for price_field in price_fields:
#     # Histogram
#     plt.figure(figsize=(12, 6))
#     sns.kdeplot(filtered_data[price_field], color='blue', fill=True, alpha=0.6)
#     plt.title('Kernel Density Estimate')
#     plt.ylabel('Density')
#     plt.grid()
#     plt.tight_layout()
#     plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = '../sneakers.json'
data = pd.read_json(file_path)

# Define an array with the price fields
price_fields = [
    'retail_price_eur',
    'lowest_price_eur',
    'gp_lowest_price_eur'
]

# Step 2: Calculate IQR for each price field and filter the data
filtered_data = data.copy()

for price_field in price_fields:
    Q1 = data[price_field].quantile(0.25)
    Q3 = data[price_field].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_data = filtered_data[(filtered_data[price_field] >= lower_bound) &
                                  (filtered_data[price_field] <= upper_bound)]

# Step 3: Plot Real vs Filtered Data
for price_field in price_fields:
    plt.figure(figsize=(12, 6))

    # KDE plot for original data
    sns.kdeplot(data[price_field], color='red', label='Original Data', fill=True, alpha=0.3)

    # KDE plot for filtered data
    sns.kdeplot(filtered_data[price_field], color='blue', label='Filtered Data (IQR)', fill=True, alpha=0.5)

    plt.title(f'Kernel Density Estimate: {price_field}')
    plt.xlabel('Price')
    plt.ylabel('Density')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()