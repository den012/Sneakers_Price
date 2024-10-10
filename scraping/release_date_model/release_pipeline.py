import json
import pandas as pd
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import mean_squared_error

# Load data
def load_data(file_path):
    return pd.read_json(file_path)

# Encode categorical features
def encode_colors(df, encoder=None):
    # Check if the encoder exists; if not, fit a new one
    if encoder is None:
        encoder = LabelEncoder()
        df['sneaker_color'] = encoder.fit_transform(df['sneaker_color'])
    else:
        # Handle unseen labels by adding them to the classes
        new_classes = set(df['sneaker_color']) - set(encoder.classes_)
        if new_classes:
            encoder.classes_ = np.append(encoder.classes_, list(new_classes))

        # Transform the data, but handle unseen labels by assigning them a new label
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

# Train model
def train_model(X, y, model):
    model.fit(X, y)
    predictions = model.predict(X)
    mse = mean_squared_error(y, predictions)
    return model, mse

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

# Main pipeline
def model_pipeline():
    # Load training and testing data
    df_train = load_data('testing_steps/train_data.json')
    df_test = load_data('testing_steps/test_data.json')
    df_predict = load_data('testing_steps/data_to_predict.json')

    # Combine training and testing data for encoding
    combined_df = pd.concat([df_train, df_test])

    # Fit encoder on combined data
    combined_df, encoder = encode_colors(combined_df, None)

    # Prepare training data with the fitted encoder
    df_train, _ = encode_colors(df_train, encoder)
    X_train, y_train, df_with_dates = prepare_data(df_train, encoder)

    # Train and evaluate models
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

    # Select the best model
    best_model_name = min(models_mse, key=lambda x: models_mse[x][1])
    best_model = models_mse[best_model_name][0]
    print(f'Best model: {best_model_name} with MSE: {models_mse[best_model_name][1]}')

    # Prepare testing data with the fitted encoder
    df_test, _ = encode_colors(df_test, encoder)
    X_test, _, _ = prepare_data(df_test, encoder, is_train=False)

    # Evaluate the best model on testing data
    test_predictions = best_model.predict(X_test)
    print(f'Test predictions: {test_predictions}')

    # Prepare data to predict
    imputer = SimpleImputer(strategy='constant', fill_value=0)
    imputed_values = imputer.fit_transform(df_predict[['release_year', 'release_month', 'release_day']])
    df_predict[['release_year', 'release_month', 'release_day']] = pd.DataFrame(imputed_values, columns=['release_year', 'release_month', 'release_day'])

    # Predict missing dates
    df_with_predictions = predict_missing_dates(best_model, df_predict, encoder)

    # Save the combined data
    output_file = 'testing_steps/data_predicted.json'
    save_results(df_with_dates, df_with_predictions, output_file)