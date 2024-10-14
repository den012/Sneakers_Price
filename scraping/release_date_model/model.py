import json
import pandas as pd
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit, train_test_split

# Load data
def load_data(file_path):
    return pd.read_json(file_path)

# Encode categorical features
def encode_colors(df, encoder=None):
    if encoder is None:
        encoder = LabelEncoder()
        df['sneaker_color'] = encoder.fit_transform(df['sneaker_color'])
    else:
        new_classes = set(df['sneaker_color']) - set(encoder.classes_)
        if new_classes:
            encoder.classes_ = np.append(encoder.classes_, list(new_classes))
        df['sneaker_color'] = df['sneaker_color'].apply(
            lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1)
    return df, encoder

# Prepare data for training/testing
def prepare_data(df, encoder, is_train=True):
    df, encoder = encode_colors(df, encoder)
    X = df[['sneaker_color']]
    if is_train:
        y = df[['release_year', 'release_month', 'release_day']]
        return X, y, df
    return X, None, df

# Predict missing dates
def predict_missing_dates(model, df, encoder):
    X, _, _ = prepare_data(df, encoder, is_train=False)
    predictions = model.predict(X)
    df[['release_year', 'release_month', 'release_day']] = predictions
    return df

# Save results
def save_results(df_with_dates, df_with_predictions, output_file):
    combined_df = pd.concat([df_with_dates, df_with_predictions])
    combined_df.to_json(output_file, orient='records', indent=4)


# Train model with Time Series Split
def train_model(X, y, model):
    tscv = TimeSeriesSplit(n_splits=5)
    mse_scores = []
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mse_scores.append(mean_squared_error(y_test, predictions))
    avg_mse = np.mean(mse_scores)
    return model, avg_mse

# Main pipeline
def model_pipeline():
    df = load_data('testing_steps/release_date_help/train_data.json')
    df, encoder = encode_colors(df, None)
    X, y, df_with_dates = prepare_data(df, encoder)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    models = {
        'XGBoost': xgb.XGBRegressor(objective='reg:squarederror'),
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor()
    }

    models_mse = {}
    for model_name, model in models.items():
        trained_model, mse = train_model(X_train, y_train, model)
        models_mse[model_name] = (trained_model, mse)
        print(f'{model_name} MSE: {mse}')

    best_model_name = min(models_mse, key=lambda x: models_mse[x][1])
    best_model = models_mse[best_model_name][0]
    print(f'Best model: {best_model_name} with MSE: {models_mse[best_model_name][1]}')

    test_predictions = best_model.predict(X_test)
    print(f'Test predictions: {test_predictions}')

    df_predict = load_data('testing_steps/release_date_help/data_to_predict.json')
    df_predict, _ = encode_colors(df_predict, encoder)
    imputer = SimpleImputer(strategy='constant', fill_value=0)
    imputed_values = imputer.fit_transform(df_predict[['release_year', 'release_month', 'release_day']])
    df_predict[['release_year', 'release_month', 'release_day']] = pd.DataFrame(imputed_values, columns=['release_year',
                                                                                                         'release_month',
                                                                                                         'release_day'])

    df_with_predictions = predict_missing_dates(best_model, df_predict, encoder)
    output_file = 'testing_steps/data_predicted.json'
    save_results(df_with_dates, df_with_predictions, output_file)