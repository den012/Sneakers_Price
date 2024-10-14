import json
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error


# Load data from JSON file
def load_json_data(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return pd.DataFrame(data)


# Prepare features and target for training or prediction (two cases)
def prepare_data(df, target_column=None, target_type=None):
    if target_type == 'instant_ship':
        feature_columns = ['release_year', 'retail_price_eur', 'lowest_price_eur', 'collaboration']
    elif target_type == 'gp_instant_ship':
        feature_columns = ['release_year', 'retail_price_eur', 'gp_lowest_price_eur', 'collaboration']

    X = df[feature_columns]

    if target_column:
        y = df[target_column]
        return X, y

    return X  # For prediction


# Perform cross-time validation with MSE calculation
def cross_time_validation_mse(model, X, y, n_splits=5):
    tscv = TimeSeriesSplit(n_splits=n_splits)
    mse_scores = []

    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mse_scores.append(mse)

    return sum(mse_scores) / len(mse_scores)


# Train models on the training data for both target variables
def train_models(train_file):
    df_train = load_json_data(train_file)

    # Prepare data for instant_ship_lowest_price_eur prediction
    X_instant, y_instant = prepare_data(df_train, target_column='instant_ship_lowest_price_eur',
                                        target_type='instant_ship')

    # Prepare data for gp_instant_ship_lowest_price_eur prediction
    X_gp_instant, y_gp_instant = prepare_data(df_train, target_column='gp_instant_ship_lowest_price_eur',
                                              target_type='gp_instant_ship')

    # Initialize models for both cases
    lr_instant_model = LinearRegression()
    xgb_instant_model = XGBRegressor()

    lr_gp_instant_model = LinearRegression()
    xgb_gp_instant_model = XGBRegressor()

    # Train models on the entire training data for instant_ship_lowest_price_eur
    lr_instant_model.fit(X_instant, y_instant)
    xgb_instant_model.fit(X_instant, y_instant)

    # Train models on the entire training data for gp_instant_ship_lowest_price_eur
    lr_gp_instant_model.fit(X_gp_instant, y_gp_instant)
    xgb_gp_instant_model.fit(X_gp_instant, y_gp_instant)

    return {
        'instant_lr_model': lr_instant_model,
        'instant_xgb_model': xgb_instant_model,
        'gp_instant_lr_model': lr_gp_instant_model,
        'gp_instant_xgb_model': xgb_gp_instant_model
    }


def evaluate_models(test_file, models):
    df_test = load_json_data(test_file)

    # Prepare test data for instant_ship_lowest_price_eur
    X_test_instant, y_test_instant = prepare_data(df_test, target_column='instant_ship_lowest_price_eur',
                                                  target_type='instant_ship')

    # Prepare test data for gp_instant_ship_lowest_price_eur
    X_test_gp_instant, y_test_gp_instant = prepare_data(df_test, target_column='gp_instant_ship_lowest_price_eur',
                                                        target_type='gp_instant_ship')

    # Get predictions and calculate MSE for Linear Regression (instant)
    lr_instant_pred = models['instant_lr_model'].predict(X_test_instant)
    lr_instant_mse = mean_squared_error(y_test_instant, lr_instant_pred)

    # Get predictions and calculate MSE for XGBoost (instant)
    xgb_instant_pred = models['instant_xgb_model'].predict(X_test_instant)
    xgb_instant_mse = mean_squared_error(y_test_instant, xgb_instant_pred)

    # Get predictions and calculate MSE for Linear Regression (gp_instant)
    lr_gp_instant_pred = models['gp_instant_lr_model'].predict(X_test_gp_instant)
    lr_gp_instant_mse = mean_squared_error(y_test_gp_instant, lr_gp_instant_pred)

    # Get predictions and calculate MSE for XGBoost (gp_instant)
    xgb_gp_instant_pred = models['gp_instant_xgb_model'].predict(X_test_gp_instant)
    xgb_gp_instant_mse = mean_squared_error(y_test_gp_instant, xgb_gp_instant_pred)

    return {
        'lr_instant_mse': lr_instant_mse,
        'xgb_instant_mse': xgb_instant_mse,
        'lr_gp_instant_mse': lr_gp_instant_mse,
        'xgb_gp_instant_mse': xgb_gp_instant_mse
    }


# Predict the missing values in data-to-predict for both models and save the results
def predict_missing_values(models, predict_file, output_file):
    df_predict = load_json_data(predict_file)

    # Prepare data for instant_ship_lowest_price_eur prediction
    X_predict_instant = prepare_data(df_predict, target_type='instant_ship')

    # Prepare data for gp_instant_ship_lowest_price_eur prediction
    X_predict_gp_instant = prepare_data(df_predict, target_type='gp_instant_ship')

    # Predict missing values for 'instant_ship_lowest_price_eur'
    df_predict['instant_ship_lowest_price_eur'] = models['instant_xgb_model'].predict(X_predict_instant)

    # Predict missing values for 'gp_instant_ship_lowest_price_eur'
    df_predict['gp_instant_ship_lowest_price_eur'] = models['gp_instant_xgb_model'].predict(X_predict_gp_instant)

    # Save the predicted data to a file (JSON)
    df_predict.to_json(output_file, orient='records', indent=4)
    print(f"Predicted data saved to {output_file}")


# Main pipeline function
def shipping_model():
    train_file = 'testing_steps/ship_price_help/train_data.json'
    test_file = 'testing_steps/ship_price_help/test_data.json'
    predict_file = 'testing_steps/ship_price_help/data_to_predict.json'
    output_file = 'testing_steps/ship_price_help/predicted_data.json'

    # Train models for both targets
    models = train_models(train_file)

    # Evaluate models on test data
    mse_values = evaluate_models(test_file, models)

    # Print MSE values for both models
    print(f"Linear Regression MSE on test data (instant_ship): {mse_values['lr_instant_mse']}")
    print(f"XGBoost MSE on test data (instant_ship): {mse_values['xgb_instant_mse']}")
    print(f"Linear Regression MSE on test data (gp_instant_ship): {mse_values['lr_gp_instant_mse']}")
    print(f"XGBoost MSE on test data (gp_instant_ship): {mse_values['xgb_gp_instant_mse']}")

    # Use the models (XGBoost in this case) to predict missing values
    predict_missing_values(models, predict_file, output_file)