from model import *


file_path = 'copy.json'
df = load_data(file_path)
inspect_data(df)

# ENCODE COLORS
df, encoder = encode_colors(df)

# PREPARE TRAINING DATA
X, y, df_with_dates, df_without_dates = prepare_data(df, encoder)

# TRAIN MODELS AND STORE MAE VALUES
models_mae = {}

# RANDOM FOREST MODEL
rf_model, rf_mae = train_model(X, y)
models_mae['Random Forest'] = (rf_model, rf_mae)

# XGBOOST MODEL
xgb_model, xgb_mae = train_xgboost(X, y)
models_mae['XGBoost'] = (xgb_model, xgb_mae)

# LINEAR REGRESSION MODEL
lr_model, lr_mae = train_linear_regression(X, y)
models_mae['Linear Regression'] = (lr_model, lr_mae)

# DETERMINE THE BEST MODEL BASED ON MAE
best_model_name = min(models_mae, key=lambda x: models_mae[x][1])
best_model = models_mae[best_model_name][0]

print(f'Best model: {best_model_name} with MAE: {models_mae[best_model_name][1]}')

# USE THE BEST MODEL TO PREDICT MISSING RELEASE DATES
X_missing = df_without_dates[encoder.get_feature_names_out(['sneaker_color'])]
predicted_release_dates = best_model.predict(X_missing)

# Add predictions to the DataFrame
df_without_dates = df_without_dates.copy()
df_without_dates.loc[:, 'predicted_release_date'] = predicted_release_dates

# Save the combined data
output_file = 'test_output.json'
save_results(df_with_dates, df_without_dates, output_file)