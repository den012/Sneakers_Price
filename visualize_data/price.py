import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json


# Function to plot KDE for all price fields
def plot_price_kde(input_file):
    # Load the data from JSON file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract the necessary price fields into a pandas DataFrame
    price_fields = ['retail_price_eur', 'lowest_price_eur', 'gp_lowest_price_eur']
    price_data = pd.DataFrame(data, columns=price_fields)


    # Plotting the KDE (Kernel Density Estimate)
    plt.figure(figsize=(12, 6))

    # Plot the KDE for each price field
    for price_field in price_fields:
        sns.kdeplot(price_data[price_field], label=price_field, fill=True, alpha=0.6)

    # Customize the plot
    plt.title('Price Distribution (KDE)', fontsize=16)
    plt.xlabel('Price in EUR', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend(title="Price Fields")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Example usage
plot_price_kde('../sneakers.json')


# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import json
#
#
# # Function to plot boxplot and highlight outliers
# def plot_outliers(input_file):
#     # Load the data from JSON file
#     with open(input_file, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#
#     # Extract the necessary price fields into a pandas DataFrame
#     price_fields = ['retail_price_eur', 'lowest_price_eur', 'gp_lowest_price_eur']
#     price_data = pd.DataFrame(data, columns=price_fields)
#
#
#     # Calculate IQR for each price field and detect outliers
#     for price_field in price_fields:
#         Q1 = price_data[price_field].quantile(0.25)
#         Q3 = price_data[price_field].quantile(0.75)
#         IQR = Q3 - Q1
#
#         # Calculate bounds for outliers
#         lower_bound = Q1 - 1.5 * IQR
#         upper_bound = Q3 + 1.5 * IQR
#
#         # Detect outliers
#         price_data[f'{price_field}_outlier'] = price_data[price_field].apply(
#             lambda x: 'Outlier' if x < lower_bound or x > upper_bound else 'Normal'
#         )
#
#     # Plotting the Boxplot with Outliers
#     plt.figure(figsize=(12, 6))
#
#     # Create a boxplot for each price field
#     sns.boxplot(data=price_data[price_fields], palette="Set2", showfliers=True)
#
#     # Customize the plot
#     plt.title('Price Distribution with Outliers (Boxplot)', fontsize=16)
#     plt.xlabel('Price Fields', fontsize=12)
#     plt.ylabel('Price in EUR', fontsize=12)
#     plt.grid(True)
#     plt.tight_layout()
#
#     # Show the plot
#     plt.show()
#
#
# # Example usage
# plot_outliers('../sneakers.json')