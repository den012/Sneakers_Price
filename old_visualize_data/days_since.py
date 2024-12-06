import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
file_path = './sneakers.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Extract the 'days_since_release' column
days_since_release_data = data['days_since_release']

# Plot the Kernel Density Estimate (KDE) of the 'days_since_release' column
plt.figure(figsize=(12, 6))
sns.kdeplot(days_since_release_data, fill=True)
plt.title('Kernel Density Estimate of Days Since Release')
plt.xlabel('Days Since Release')
plt.ylabel('Density')
plt.show()