import matplotlib.pyplot as plt
import numpy as np

# Example MAE values
mae_values = {
    'Random Forest': 2.054285182255343e+16,
    'XGBoost': 2.059111278227617e+16,
    'Linear Regression': 2.0577255937032816e+16,
}

# Extracting keys and values for plotting
models = list(mae_values.keys())
mae = list(mae_values.values())

# Creating the bar plot
plt.figure(figsize=(12, 8))
bars = plt.bar(models, mae, color=plt.cm.viridis(np.linspace(0, 1, len(models))))

# Adding labels and title
plt.xlabel('Model', fontsize=14)
plt.ylabel('Mean Absolute Error (MAE)', fontsize=14)
plt.title('Comparison of Model Performance (MAE)', fontsize=16)
plt.ylim(0, max(mae) * 1.1)

# Adding grid
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adding value labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (max(mae) * 0.01), f'{yval:.2e}', ha='center', va='bottom', fontsize=12)

plt.gca().set_facecolor('#f7f7f7')


# Show plot
plt.show()