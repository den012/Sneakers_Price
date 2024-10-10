from scraper import scrape_sneakers
from functions.remove_rename_add_columns import remove_rename_add_data_cols
from functions.detect_brand import detect_brands
from functions.detect_collab import celebs, add_collaboration
from functions.detect_sneaker_dicount_tag import fix_sneaker_discount
from release_date_model.filter_data import *
from release_date_model.merge_to_dataset import *
from release_date_model.release_pipeline import *
from release_date_model.graph import *


# scraped_sneakers = scrape_sneakers('sneakers', 'testing_steps/sneakers_data.json')
# print(f"Scraped {len(scraped_sneakers)}")
#
# remove_rename_add_data_cols('testing_steps/sneakers_data.json')
#
# detect_brands('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')
#
# number, sneakers_with_collab = add_collaboration('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')
# print(number)
# print(f"Processed {len(sneakers_with_collab)}")
#
# fix_sneaker_discount('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')

#prepare data for model
# refractor_data('testing_steps/sneakers_data.json', 'testing_steps/sneakers_data.json')

# get model data
# get_data_for_model('testing_steps/sneakers_data.json', 'testing_steps/data_for_model.json')

#get training and testing data
# get_training_and_testing_data('testing_steps/data_for_model.json', 'testing_steps/train_data.json', 'testing_steps/test_data.json')

#get data to predict
# get_data_to_predict('testing_steps/sneakers_data.json', 'testing_steps/data_to_predict.json')

# run the model and get predictions
# model_pipeline()

#merge predictions with the original dataset
# update_release_dates('testing_steps/sneakers_data.json', 'testing_steps/data_predicted.json', 'testing_steps/sneakers_data.json')

#draw graph
# models_mse = {
#         'XGBoost': (None, 32.033138721185516),
#         'Linear Regression': (None, 32.429062066651895),
#         'Decision Tree': (None, 32.0331386834529)
#     }
# plot_model_accuracies(models_mse)

