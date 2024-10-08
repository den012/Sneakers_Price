import matplotlib.pyplot as plt
import seaborn as sns

def plot_model_accuracies(models_mse):
    # Extract model names and their corresponding MSE values
    model_names = list(models_mse.keys())
    mse_values = [mse for _, mse in models_mse.values()]

    # Set the style
    sns.set(style="whitegrid")

    # Create a bar chart
    plt.figure(figsize=(12, 8))
    barplot = sns.barplot(x=model_names, y=mse_values, hue=model_names, palette="viridis", legend=False)

    # Add title and labels
    plt.title('Model Accuracies (MSE)', fontsize=16)
    plt.xlabel('Models', fontsize=14)
    plt.ylabel('Mean Squared Error (MSE)', fontsize=14)

    # Adjust y-axis limits to add more space at the top
    plt.ylim(0, max(mse_values) * 1.2)

    # Draw a red line at the top of the smallest bar
    min_mse = min(mse_values)
    plt.axhline(y=min_mse, color='red', linestyle='--', linewidth=2)

    # Display the values on top of the bars
    for i, v in enumerate(mse_values):
        barplot.text(i, v + 0.5, f"{v:.2f}", ha='center', va='bottom', fontsize=15, color='black', fontdict={'weight': 'bold'})

    # Show the plot
    plt.show()