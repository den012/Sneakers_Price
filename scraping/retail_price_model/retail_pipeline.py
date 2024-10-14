from parsing_data import *
import pandas as pd

df = pd.read_json('../testing_steps/retail_price_help/train_data.json')

# Check for missing values in the dataframe
print(df.isnull().sum())
#
# clean_dataset('../testing_steps/sneakers_data.json', '../testing_steps/sneakers_data.json')
#
# # get_test_train_data('../testing_steps/sneakers_data.json', '../testing_steps/train_data.json', '../testing_steps/test_data.json')
#
# # get_prediction_data('../testing_steps/sneakers_data.json', '../testing_steps/prediction_data.json')
#
# # merge_predicted_data('../testing_steps/sneakers_data.json', '../testing_steps/retail_price_help/predictions.json', '../testing_steps/sneakers_data.json')
