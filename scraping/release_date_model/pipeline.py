import json
import pandas as pd
from model import load_data, prepare_data, train_model, predict_missing_dates, save_results, encode_colors
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.impute import SimpleImputer

# Main pipeline
def main_pipeline():
    # Load training and testing data
    df_train = load_data('data/training_data.json')
    df_test = load_data('data/testing_data.json')
    df_predict = load_data('data/data_to_predict.json')

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
    output_file = 'predicted_release_dates.json'
    save_results(df_with_dates, df_with_predictions, output_file)

if __name__ == "__main__":
    main_pipeline()