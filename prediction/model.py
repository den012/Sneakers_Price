import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from sklearn.ensemble import StackingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib

# Load your dataset
df = pd.read_csv("./filtered_file.csv")

# Rename columns to 'year', 'month', 'day' temporarily for pd.to_datetime compatibility
df.rename(columns={'release_year': 'year', 'release_month': 'month', 'release_day': 'day'}, inplace=True)

# Convert release date components to a single 'release_date' column
df['release_date'] = pd.to_datetime(df[['year', 'month', 'day']])

# Rename columns back to their original names
df.rename(columns={'year': 'release_year', 'month': 'release_month', 'day': 'release_day'}, inplace=True)

# Calculate days since release
today = datetime.now()
df['days_since_release'] = (today - df['release_date']).dt.days

# Drop the original release date columns
df = df.drop(['release_year', 'release_month', 'release_day', 'release_date'], axis=1)

# Handle missing values by filling them with -1
df.fillna(-1, inplace=True)

# Convert categorical columns to dummy/indicator variables
categorical_columns = ['sneaker_brand', 'collaboration', 'collaboration_name', 'sneaker_color', 
                       'data.category', 'discount_tag', 'box_condition', 'product_condition']
df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

# Define target and features
target = 'retail_price_eur'
features = df.drop(columns=['sneaker_name', 'sneaker_slug', target]).columns

X = df[features]
y = df[target]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define base models for stacking
xgb_model = XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=8, random_state=42)
rf_model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
lr_model = LinearRegression()

# Create a stacking regressor with XGBoost, Random Forest, and Linear Regression
stacking_model = StackingRegressor(
    estimators=[
        ('xgb', xgb_model),
        ('rf', rf_model),
        ('lr', lr_model)
    ],
    final_estimator=LinearRegression(),  # Meta-model
    cv=5  # Cross-validation for stacking
)

# Hyperparameter tuning using GridSearchCV
param_grid = {
    'xgb__n_estimators': [100, 200],
    'xgb__learning_rate': [0.05, 0.1],
    'rf__n_estimators': [50, 100],
    'rf__max_depth': [6, 8, 10]
}

grid_search = GridSearchCV(estimator=stacking_model, param_grid=param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best parameters
print("Best parameters found:", grid_search.best_params_)

# Use the best model from grid search
best_model = grid_search.best_estimator_

# Fit the model
best_model.fit(X_train, y_train)

# Make predictions
y_pred = best_model.predict(X_test)

# Calculate performance metrics for the best model
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print(f"Best Model Mean Absolute Error: {mae}")
print(f"Best Model RMSE: {rmse}")
print(f"Best Model MAPE: {mape:.2f}%")
print(f"Best Model R-squared: {r2}")

# Perform cross-validation on the stacking model
cv_scores = cross_val_score(best_model, X, y, cv=5, scoring='neg_mean_absolute_error')
print("Cross-Validation MAE Scores:", -cv_scores)
print("Mean Cross-Validation MAE:", -np.mean(cv_scores))

# Save the final model and columns for future predictions
joblib.dump(best_model, "xgb_sneaker_price_model_final.pkl")
joblib.dump(X_train.columns, './xgb_model_columns.pkl')


# Stacking Model Mean Absolute Error: 14.257182445783577
# Stacking Model RMSE: 20.404463148146693
# Stacking Model MAPE: 12.44%
# Stacking Model R-squared: 0.5525500468729165
# Cross-Validation MAE Scores: [21.78414914 14.27854507 15.20479867 14.89851794 15.0779938 ]
# Mean Cross-Validation MAE: 16.24880092416553

#ACCURACY OF THE MODEL IS 87.56%