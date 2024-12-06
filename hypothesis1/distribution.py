import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('../sneakers.csv')

# # Boxplot for price comparison
# sns.boxplot(x='collaboration', y='lowest_price_eur', data=data)
# plt.xticks([0, 1], ['Non-Collaborative', 'Collaborative'])
# plt.title('Price Distribution: Collaborative vs Non-Collaborative Sneakers')
# plt.show()

# from scipy.stats import ttest_ind
#
# # Separate the two groups
# collaborative_prices = data[data['collaboration'] == 1]['lowest_price_eur']
# non_collaborative_prices = data[data['collaboration'] == 0]['lowest_price_eur']
#
# # Perform t-test
# t_stat, p_value = ttest_ind(collaborative_prices, non_collaborative_prices, equal_var=False)
# print(f"T-Statistic: {t_stat}, P-Value: {p_value}")
#
# # Interpret
# if p_value < 0.05:
#     print("The difference in mean prices is statistically significant.")
# else:
#     print("No significant difference in mean prices.")


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# # Prepare features and target
# X = data[['collaboration']]
# y = data['lowest_price_eur']
#
# # Split the dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # Train the model
# linear_model = LinearRegression()
# linear_model.fit(X_train, y_train)
#
# # Evaluate
# y_pred = linear_model.predict(X_test)
# print(f"Coefficient (Collaboration Premium): {linear_model.coef_[0]} €")

from sklearn.ensemble import RandomForestRegressor

# Prepare additional features
X = data[['collaboration', 'days_since_release']]  # Add other features if needed
y = data['lowest_price_eur']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate
y_pred_rf = rf_model.predict(X_test)
r2_rf = r2_score(y_test, y_pred_rf)
print(f"R² (Random Forest): {r2_rf}")