import pandas as pd
import json
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