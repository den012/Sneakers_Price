from scraper import scrape_sneakers

from functions.remove_rename_add_columns import remove_rename_add_data_cols
from functions.detect_brand import detect_brands
from functions.detect_collab import celebs, add_collaboration
from functions.detect_sneaker_dicount_tag import fix_sneaker_discount

from release_date_model.filter_data import *
from release_date_model.merge_to_dataset import *
from release_date_model.model import *

from release_date_model.graph import *

from retail_price_model.model import *
from retail_price_model.parsing_data import *

from ship_price_model.parsing_data import *
from ship_price_model.model import *

# scraped_sneakers = scrape_sneakers('sneakers', 'testing_steps/sneakers_data.json')
# print(f"Scraped {len(scraped_sneakers)}")

# remove_rename_add_data_cols('testing_steps/sneakers_data.json')

# detect_brands('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')
#
# number, sneakers_with_collab = add_collaboration('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')
# print(number)
# print(f"Processed {len(sneakers_with_collab)}")


# RELEASE DATE
#prepare data for model
# refractor_data('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')
#
# get model data
# get_data_for_model('testing_steps/sneakers_data.json', 'testing_steps/release_date_help/data_for_model.json')
#
# get training and testing data
# get_training_and_testing_data('testing_steps/release_date_help/data_for_model.json', 'testing_steps/release_date_help/train_data.json')
#
# get data to predict
# get_data_to_predict('testing_steps/release_date_help/data_for_model.json', 'testing_steps/release_date_help/data_to_predict.json')
#
# run the model and get predictions
# model_pipeline()
#
# merge predictions with the original dataset
# update_release_dates('testing_steps/sneakers_data.json', 'testing_steps/release_date_help/data_predicted.json', 'testing_steps/sneakers_data.json')

#draw graph
# XGBoost MSE: 37.094441639862524
# Linear Regression MSE: 36.88507205098689
# Decision Tree MSE: 37.09477684233433
# models_mse = {
#     "XGBoost MSE": (None, 37.094441639862524),
#     "Linear Regression MSE": (None, 36.88507205098689),
#     "Decision Tree MSE": (None,37.09477684233433)
#      }
# plot_model_accuracies(models_mse, 'Release Date Model MSE Scores')



# RETAIL PRICE
# clean_dataset('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')
#
# get_test_train_data('testing_steps/sneakers_data.json', 'testing_steps/retail_price_help/train_data.json', 'testing_steps/retail_price_help/data_to_predict.json')

# retail_model()
# merge_predicted_data('testing_steps/sneakers_data.json', 'testing_steps/retail_price_help/predicted_sneakers.json', 'testing_steps/sneakers_data.json')

# fix_sneaker_discount('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')
# High-end MAE (XGBoost): 630.1270853678385
# High-end MAE (Linear Regression): 664.7012977342359
# Regular MAE (XGBoost): 30.039757382281902
# Regular MAE (Linear Regression): 33.33324378221126
# models_mse = {
#     'XGBoost': (None, 30.039757382281902),
#     'Linear Regression': (None, 33.33324378221126)
# }
# plot_model_accuracies(models_mse, 'Retail Price Model MSE Scores')



# SHIP PRICE
# parse_model_data('testing_steps/sneakers_data.json', 'testing_steps/ship_price_help/data_for_model.json')
#
# get_training_testing_data('testing_steps/ship_price_help/data_for_model.json', 'testing_steps/ship_price_help/train_data.json', 'testing_steps/ship_price_help/test_data.json')
#
# get_data_to_predict('testing_steps/ship_price_help/data_for_model.json', 'testing_steps/ship_price_help/data_to_predict.json')
#
# shipping_model()
# merge_predicted_data('testing_steps/sneakers_data.json', 'testing_steps/ship_price_help/predicted_data.json', 'testing_steps/sneakers_data.json')

# Linear Regression MSE on test data (instant_ship): 1615.7266021407206
# XGBoost MSE on test data (instant_ship): 11119.166623513236
# Linear Regression MSE on test data (gp_instant_ship): 3326.7673653015313
# XGBoost MSE on test data (gp_instant_ship): 62176.906672632016
# models_mse = {
#     'LinearRegression': (None, 3326.7673653015313),
#     'XGBoost': (None, 62176.906672632016),
# }
# plot_model_accuracies(models_mse, 'Shippping Price Model MSE Scores')
