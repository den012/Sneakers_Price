import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# Load data from JSON files
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)


# Prepare the data for modeling
def prepare_data(df):
    X = df[['release_year', 'lowest_price_eur', 'collaboration']]
    y = df['retail_price_eur']
    return X, y


# Train and evaluate the XGBoost model
def train_and_evaluate_xgboost(X_train, y_train, X_test, y_test):
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2]
    }

    xgb_model = xgb.XGBRegressor(objective='reg:squarederror')

    grid_search = GridSearchCV(xgb_model, param_grid, scoring='neg_mean_squared_error', cv=5)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    xgb_pred = best_model.predict(X_test)
    xgb_mse = mean_squared_error(y_test, xgb_pred)
    print(f'XGBoost Mean Squared Error: {xgb_mse}, R²: {r2_score(y_test, xgb_pred)}')
    return best_model, xgb_mse


# Train and evaluate the Linear Regression model
def train_and_evaluate_linear_regression(X_train, y_train, X_test, y_test):
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_mse = mean_squared_error(y_test, lr_pred)
    print(f'Linear Regression Mean Squared Error: {lr_mse}, R²: {r2_score(y_test, lr_pred)}')
    return lr_model, lr_mse


# Main function
def predict_data():
    train_file = 'testing_steps/train_data.json'
    test_file = 'testing_steps/test_data.json'
    predict_file = 'testing_steps/data_to_predict.json'

    # Load data
    train_data = load_data(train_file)
    test_data = load_data(test_file)
    predict_data = load_data(predict_file)

    # Prepare training and testing data
    X_train, y_train = prepare_data(train_data)
    X_test, y_test = prepare_data(test_data)

    # Train and evaluate the models
    best_model, xgb_mse = train_and_evaluate_xgboost(X_train, y_train, X_test, y_test)
    lr_model, lr_mse = train_and_evaluate_linear_regression(X_train, y_train, X_test, y_test)

    # Prepare prediction data
    X_predict = predict_data[['release_year', 'lowest_price_eur', 'collaboration']]
    predictions = best_model.predict(X_predict)

    # Overwrite retail_price_eur with predictions
    predict_data['retail_price_eur'] = predictions

    # Save predictions to JSON file
    output_file = 'testing_steps/predictions.json'
    predict_data.to_json(output_file, orient='records', indent=4)
    print(f'Predictions saved to {output_file}')
