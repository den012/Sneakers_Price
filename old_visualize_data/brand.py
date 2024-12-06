import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Load the CSV file
file_path = './sneakers.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Extract the 'brand' column
brand_data = data['brand']

# Transform the 'brand' column to numerical values using LabelEncoder
label_encoder = LabelEncoder()
brand_data_encoded = label_encoder.fit_transform(brand_data)

# Create a DataFrame with the encoded brand data
encoded_df = pd.DataFrame({'brand': brand_data, 'encoded': brand_data_encoded})

# Plot the Kernel Density Estimate (KDE) of the encoded 'brand' column
plt.figure(figsize=(12, 6))
sns.kdeplot(brand_data_encoded, fill=True)
plt.title('Kernel Density Estimate of Brand Popularity')
plt.xlabel('Brand')
plt.ylabel('Density')

# Map the encoded values back to brand names for the x-axis labels
brand_names = label_encoder.inverse_transform(range(len(label_encoder.classes_)))
plt.xticks(ticks=range(len(brand_names)), labels=brand_names, rotation=90)

plt.show()