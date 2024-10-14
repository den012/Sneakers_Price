import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error

# Step 1: Load and Preprocess the Data
def load_and_preprocess_data(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Fill missing values
    df.fillna(0, inplace=True)

    # Encode categorical variables
    label_encoder = LabelEncoder()
    df['collaboration'] = label_encoder.fit_transform(df['collaboration'])
    df['sneaker_brand'] = label_encoder.fit_transform(df['sneaker_brand'])
    df['sneaker_color'] = label_encoder.fit_transform(df['sneaker_color'])

    return df

def apply_clustering(df, clustering_features):
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['cluster'] = kmeans.fit_predict(df[clustering_features])
    return df, kmeans

# Step 3: Train the Models with Time Series Cross-Validation
# python
def train_models(df, features, target):
    models = {'high_end': {}, 'regular': {}}

    # Split data into high-end and regular clusters
    high_end = df[df['cluster'] == 1]
    regular = df[df['cluster'] == 0]

    # Initialize TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=5)

    # Train XGBoost and Linear Regression for high-end sneakers
    xgb_model_high = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    lin_model_high = LinearRegression()
    for train_index, test_index in tscv.split(high_end):
        X_train, X_test = high_end[features].iloc[train_index], high_end[features].iloc[test_index]
        y_train, y_test = high_end[target].iloc[train_index], high_end[target].iloc[test_index]

        xgb_model_high.fit(X_train, y_train)
        lin_model_high.fit(X_train, y_train)

        y_pred_xgb = xgb_model_high.predict(X_test)
        y_pred_lin = lin_model_high.predict(X_test)
        print("High-end MAE (XGBoost):", mean_absolute_error(y_test, y_pred_xgb))
        print("High-end MAE (Linear Regression):", mean_absolute_error(y_test, y_pred_lin))

    models['high_end']['xgb'] = xgb_model_high
    models['high_end']['lin'] = lin_model_high

    # Train XGBoost and Linear Regression for regular sneakers
    xgb_model_reg = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)
    lin_model_reg = LinearRegression()
    for train_index, test_index in tscv.split(regular):
        X_train, X_test = regular[features].iloc[train_index], regular[features].iloc[test_index]
        y_train, y_test = regular[target].iloc[train_index], regular[target].iloc[test_index]

        xgb_model_reg.fit(X_train, y_train)
        lin_model_reg.fit(X_train, y_train)

        y_pred_xgb = xgb_model_reg.predict(X_test)
        y_pred_lin = lin_model_reg.predict(X_test)
        print("Regular MAE (XGBoost):", mean_absolute_error(y_test, y_pred_xgb))
        print("Regular MAE (Linear Regression):", mean_absolute_error(y_test, y_pred_lin))

    models['regular']['xgb'] = xgb_model_reg
    models['regular']['lin'] = lin_model_reg

    return models

def predict_retail_price(df, kmeans, models, features):
    predictions = []
    clustering_features = ['lowest_price_eur']  # Only include clustering features used for KMeans

    for _, row in df.iterrows():
        # Create a DataFrame for the clustering feature
        cluster_feature_df = pd.DataFrame([row[clustering_features].values], columns=clustering_features)
        cluster = kmeans.predict(cluster_feature_df)[0]

        # Create a DataFrame for the feature values to preserve feature names
        feature_df = pd.DataFrame([row[features].values], columns=features)

        if cluster == 0:
            model_xgb = models['regular']['xgb']
            model_lin = models['regular']['lin']
        else:
            model_xgb = models['high_end']['xgb']
            model_lin = models['high_end']['lin']

        prediction_xgb = model_xgb.predict(feature_df)
        prediction_lin = model_lin.predict(feature_df)
        # Average the predictions from both models
        prediction = (prediction_xgb[0] + prediction_lin[0]) / 2
        predictions.append(prediction)

    return predictions

def retail_model():
    # Define the features and target
    features = ['collaboration', 'sneaker_brand', 'sneaker_color', 'release_year', 'lowest_price_eur']
    clustering_features = ['lowest_price_eur']
    target = 'retail_price_eur'

    # Step 1: Load and preprocess training data
    df = load_and_preprocess_data('testing_steps/retail_price_help/train_data.json')

    # Step 2: Apply K-Means clustering
    df, kmeans = apply_clustering(df, clustering_features)

    # Step 3: Train models with time series cross-validation
    models = train_models(df, features, target)

    # Step 4: Load new sneaker data for predictions
    new_sneakers_df = load_and_preprocess_data('testing_steps/retail_price_help/data_to_predict.json')

    # Step 5: Predict retail prices for new sneakers
    new_sneakers_df['retail_price_eur'] = predict_retail_price(new_sneakers_df, kmeans, models, features)

    # Step 6: Save predictions to JSON
    new_sneakers_df.to_json('predicted_sneakers.json', orient='records', indent=4)

