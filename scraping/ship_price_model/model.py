import json
import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.pipeline import Pipeline
import xgboost as xgb
import lightgbm as lgb
import numpy as np

# Load data
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Prepare data
def prepare_data(data):
    df = pd.DataFrame(data)

    # Drop rows where target values are null
    df = df.dropna(subset=['instant_ship_lowest_price_eur', 'gp_instant_ship_lowest_price_eur'])

    # Define features and targets
    X = df[['retail_price_eur', 'lowest_price_eur', 'gp_lowest_price_eur']]
    y = df[['instant_ship_lowest_price_eur', 'gp_instant_ship_lowest_price_eur']]

    # Handle missing feature values
    imputer = SimpleImputer(strategy='mean')
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

    # Optionally log-transform y (if target is skewed)
    y_log = np.log1p(y)  # Can comment/uncomment depending on data distribution

    return X_imputed, y_log  # You can return y_log for better predictions

# Train and evaluate models
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    models = {
        'LinearRegression': MultiOutputRegressor(LinearRegression()),
        'XGBoost': MultiOutputRegressor(xgb.XGBRegressor(objective='reg:squarederror')),
        'LightGBM': MultiOutputRegressor(lgb.LGBMRegressor())
    }

    best_model = None
    best_mse = float('inf')

    param_grids = {
        'LinearRegression': {
            'model__estimator__fit_intercept': [True, False]
        },
        'XGBoost': {
            'model__estimator__learning_rate': [0.01, 0.1],
            'model__estimator__n_estimators': [100, 300],
            'model__estimator__max_depth': [3, 5],
            'model__estimator__subsample': [0.8, 1.0]
        },
        'LightGBM': {
            'model__estimator__num_leaves': [31, 127],
            'model__estimator__learning_rate': [0.01, 0.1],
            'model__estimator__n_estimators': [100, 200],
            'model__estimator__min_child_samples': [20, 30]
        }
    }

    for name, model in models.items():
        # Create a pipeline with imputation, scaling, and model
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', RobustScaler()),  # Try different scalers
            ('model', model)
        ])

        # Perform Grid Search with Cross-Validation
        grid_search = GridSearchCV(pipeline, param_grids.get(name, {}), cv=3, scoring='neg_mean_squared_error', n_jobs=-1)
        grid_search.fit(X_train, y_train)

        # Get the best model
        best_pipeline = grid_search.best_estimator_
        y_pred = best_pipeline.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        print(f'{name} Mean Squared Error: {mse}')
        print(f'{name} R² Score: {r2}')
        print(f'{name} Mean Absolute Error: {mae}')

        if mse < best_mse:
            best_mse = mse
            best_model = best_pipeline

    print(f'Best model: {best_model}')
    return best_model

# Predict missing values
def predict_missing_values(model, data):
    df = pd.DataFrame(data)

    # Features for prediction
    X_predict = df[['retail_price_eur', 'lowest_price_eur', 'gp_lowest_price_eur']]

    # Impute and scale
    imputer = SimpleImputer(strategy='mean')
    scaler = StandardScaler()

    # Ensure missing values are handled before prediction
    X_predict = pd.DataFrame(imputer.fit_transform(X_predict), columns=X_predict.columns)
    X_predict_scaled = pd.DataFrame(scaler.fit_transform(X_predict), columns=X_predict.columns)

    # Make predictions
    predictions = model.predict(X_predict_scaled)

    # Reverse log-transform if applied
    predictions = np.expm1(predictions)  # Uncomment if y was log-transformed during training

    # Assign predictions back to the DataFrame
    df['instant_ship_lowest_price_eur'], df['gp_instant_ship_lowest_price_eur'] = predictions.T

    return df

# Main function
def main():
    train_file = '../testing_steps/release_date_help/train_data.json'
    test_file = '../testing_steps/release_date_help/test_data.json'
    predict_file = '../testing_steps/predict_data.json'
    output_file = '../testing_steps/release_date_help/data_predicted.json'

    train_data = load_data(train_file)
    test_data = load_data(test_file)
    predict_data = load_data(predict_file)

    X_train, y_train = prepare_data(train_data)
    X_test, y_test = prepare_data(test_data)

    model = train_model(X_train, y_train)

    # Evaluate the model on the test data
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'Test Mean Squared Error: {mse}')
    print(f'Test R² Score: {r2}')
    print(f'Test Mean Absolute Error: {mae}')

    df_predicted = predict_missing_values(model, predict_data)
    df_predicted.to_json(output_file, orient='records', indent=4)
    print(f'Predictions saved to {output_file}')

if __name__ == "__main__":
    main()