import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.preprocessing import StandardScaler



data = pd.read_csv("../sneakers.csv")

data = pd.get_dummies(data, columns=['brand', 'collaboration_name', 'box_condition'], drop_first=True)

scaler = StandardScaler()
data['days_since_release_normalized'] = scaler.fit_transform(data[['days_since_release']])

# interaction features
data['interaction_days_collab'] = data['days_since_release'] * data['collaboration']
data['price_ratio'] = data['lowest_price_eur'] / data['retail_price_eur']


X = data[['days_since_release_normalized', 'retail_price_eur', 'collaboration', 'interaction_days_collab', 'price_ratio']]
y = data['lowest_price_eur']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Evaluate
y_pred_linear = linear_model.predict(X_test)
print("Linear Regression Metrics:")
print("MSE:", mean_squared_error(y_test, y_pred_linear))

# Random Forest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate
y_pred_rf = rf_model.predict(X_test)
print("Random Forest Metrics:")
print("MSE:", mean_squared_error(y_test, y_pred_rf))

# Feature Importance
feature_importances = pd.DataFrame(rf_model.feature_importances_, index=X_train.columns, columns=['Importance'])
print(feature_importances.sort_values(by='Importance', ascending=False))

# XGBoost

xgb_model = XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
xgb_model.fit(X_train, y_train)

# Evaluate
y_pred_xgb = xgb_model.predict(X_test)
print("XGBoost Metrics:")
print("MSE:", mean_squared_error(y_test, y_pred_xgb))

# SHAP Values (Optional, for interpretability)
explainer = shap.Explainer(xgb_model)
shap_values = explainer(X_test)
shap.summary_plot(shap_values, X_test)


results = {
    'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
    'MSE': [mean_squared_error(y_test, y_pred_linear), mean_squared_error(y_test, y_pred_rf), mean_squared_error(y_test, y_pred_xgb)],
}
results_df = pd.DataFrame(results)
print(results_df)

import joblib
joblib.dump(xgb_model, 'xgb_model.pkl')
model = joblib.load('xgb_model.pkl')