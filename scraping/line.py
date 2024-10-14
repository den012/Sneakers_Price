import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import json

# Load the data
df = pd.read_json('testing_steps/sneakers_data.json')

# Assuming 'retail_price' is the target and 'lowest_price_eur' is the feature
X = df[['lowest_price_eur']]
y = df['retail_price_eur']

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

# Make predictions
y_pred = model.predict(X)

# Plot the data and the fitted line
plt.scatter(X, y, color='blue', label='Actual Data')
plt.plot(X, y_pred, color='red', label='Fitted Line')
plt.xlabel('Lowest Price (EUR)')
plt.ylabel('Retail Price')
plt.title('Retail Price vs Lowest Price (EUR)')
plt.legend()
plt.show()