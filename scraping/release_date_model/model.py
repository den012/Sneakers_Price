import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import xgboost as xgb  # Import XGBoost


# Step 1: Load the JSON data
def load_data(file_path):
    return pd.read_json(file_path)


# Step 2: Inspect missing release dates
def inspect_data(df):
    print(f'Missing release dates: {df["release_date"].isna().sum()}')
    print(f'Unique colors: {df["sneaker_color"].unique()}')


# Step 3: One-hot encode sneaker colors
def encode_colors(df):
    encoder = OneHotEncoder(sparse_output=False)
    color_encoded = encoder.fit_transform(df[['sneaker_color']])
    color_df = pd.DataFrame(color_encoded, columns=encoder.get_feature_names_out(['sneaker_color']))
    df = pd.concat([df, color_df], axis=1)
    return df, encoder


# Step 4: Prepare training and prediction sets
def prepare_data(df, encoder):
    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y%m%d', errors='coerce')

    df_with_dates = df.dropna(subset=['release_date'])
    df_without_dates = df[df['release_date'].isna()]
    X = df_with_dates[encoder.get_feature_names_out(['sneaker_color'])]
    y = df_with_dates['release_date'].astype(int)  # Convert datetime to int for model training
    return X, y, df_with_dates, df_without_dates


# Step 5: Train random forest model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'Random Forest Mean Absolute Error: {mae}')
    return model, mae


# Step 5a: Train the XGBoost model
def train_xgboost(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = xgb.XGBRegressor(objective='reg:squarederror')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'XGBoost Mean Absolute Error: {mae}')
    return model, mae


# Step 5b: Train the Linear Regression model
def train_linear_regression(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'Linear Regression Mean Absolute Error: {mae}')
    return model, mae


# Step 6: Predict missing release dates
def predict_missing_dates(model, df_without_dates, encoder):
    X_missing = df_without_dates[encoder.get_feature_names_out(['sneaker_color'])]
    predicted_release_dates = model.predict(X_missing)

    # Debugging: Print the predicted release dates
    print("Predicted release dates:", predicted_release_dates)

    # Use .loc to set the predicted_release_date to avoid SettingWithCopyWarning
    df_without_dates = df_without_dates.copy()
    df_without_dates.loc[:, 'predicted_release_date'] = predicted_release_dates

    # Debugging: Print the first few rows to verify the predictions
    print(df_without_dates[['sneaker_color', 'predicted_release_date']].head())

    return df_without_dates


# Step 7: Save combined results to a new file
def save_results(df_with_dates, df_without_dates, output_file):
    df_combined = pd.concat([df_with_dates, df_without_dates], ignore_index=True)
    df_combined.to_json(output_file, orient='records', indent=4)
    print(f'Results saved to {output_file}')