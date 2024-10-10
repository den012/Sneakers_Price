import json
import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
import xgboost as xgb
import lightgbm as lgb


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
    X = df[['retail_price_eur', 'lowest_price_eur', 'gp_lowest_price_eur']]
    y = df[['instant_ship_lowest_price_eur', 'gp_instant_ship_lowest_price_eur']]
    return X, y


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

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f'{name} Mean Squared Error: {mse}')

        if mse < best_mse:
            best_mse = mse
            best_model = model

    print(f'Best model: {best_model}')
    return best_model


# Predict missing values
from sklearn.impute import SimpleImputer


# Predict missing values
def predict_missing_values(model, data):
    df = pd.DataFrame(data)
    X_predict = df[['retail_price_eur', 'lowest_price_eur', 'gp_lowest_price_eur']]

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X_predict = imputer.fit_transform(X_predict)

    # Convert back to DataFrame with column names
    X_predict = pd.DataFrame(X_predict, columns=['retail_price_eur', 'lowest_price_eur', 'gp_lowest_price_eur'])

    predictions = model.predict(X_predict)
    df['instant_ship_lowest_price_eur'], df['gp_instant_ship_lowest_price_eur'] = predictions.T
    return df


# Main function
def main():
    train_file = '../testing_steps/train_data.json'
    test_file = '../testing_steps/test_data.json'
    predict_file = '../testing_steps/predict_data.json'
    output_file = '../testing_steps/data_predicted.json'

    train_data = load_data(train_file)
    test_data = load_data(test_file)
    predict_data = load_data(predict_file)

    X_train, y_train = prepare_data(train_data)
    X_test, y_test = prepare_data(test_data)

    model = train_model(X_train, y_train)

    # Evaluate the model on the test data
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Test Mean Squared Error: {mse}')

    df_predicted = predict_missing_values(model, predict_data)
    df_predicted.to_json(output_file, orient='records', indent=4)
    print(f'Predictions saved to {output_file}')


main()