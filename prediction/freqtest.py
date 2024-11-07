import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy import stats

# Load the test dataset
df_test = pd.read_csv("./test_model.csv")

# Identify categorical columns
categorical_columns = ['sneaker_brand', 'collaboration_name', 'sneaker_color', 'data.category', 'discount_tag', 'box_condition', 'product_condition']

# One-hot encode categorical columns
df_test_encoded = pd.get_dummies(df_test, columns=categorical_columns)

# Load the saved model
xgb_model = joblib.load("./xgb_sneaker_price_model.pkl")

# Load the columns used for training
training_columns = joblib.load("./xgb_model_columns.pkl")

# Align the test data columns with the training data columns
X_test = df_test_encoded.reindex(columns=training_columns, fill_value=0)
y_test = df_test_encoded['retail_price_eur']

# Make predictions
y_pred = xgb_model.predict(X_test)

# Calculate errors
errors = y_test - y_pred
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# Frequentist Testing
# Hypothesis: Is the mean of prediction errors (errors) significantly different from zero?
t_stat, p_value = stats.ttest_1samp(errors, 0)

# Print results
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Squared Error: {rmse}")
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")



# Root Mean Squared Error: 20.802483691634112
# T-statistic: 1.80013552814242
# P-value: 0.07498007287977607