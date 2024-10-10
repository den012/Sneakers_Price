import pandas as pd
from pandas import json_normalize
import json

#load scraped data
with open('../testing_steps/sneakers_data.json', 'r') as file:
    data = json.load(file)

normalized_data = json_normalize(data)
columns = [
        "sneaker_name",
        "sneaker_brand",
        "collaboration",
        "collaboration_name",
        "sneaker_slug",
        "sneaker_color",
        "data.category",
        "discount_tag",
        "box_condition",
        "product_condition",
        "retail_price_eur",
        "lowest_price_eur",
        "instant_ship_lowest_price_eur",
        "gp_lowest_price_eur",
        "gp_instant_ship_lowest_price_eur",
        "release_year",
        "release_month",
        "release_day",
]

#sort the columns for more readability
ordered_data = normalized_data[columns].copy()

#converting prices to euro
# price_columns = ['data.retail_price_cents', 'data.lowest_price_cents', 'data.instant_ship_lowest_price_cents',
#            'data.gp_lowest_price_cents_224', 'data.gp_instant_ship_lowest_price_cents_224',]
#
# for column in price_columns:
#     ordered_data.loc[:, column] = pd.to_numeric(ordered_data[column], errors='coerce') / 100

#rename columns for more readability
# ordered_data.rename(columns={
#     'value' : 'sneaker_name',
#     'brand' : 'sneaker_brand',
#     'data.slug' : 'sneaker_slug',
#     'data.color' : 'sneaker_color',
#     'data.release_date_year' : 'sneaker_release_date',
#     'data.discount_tag' : 'sneaker_discount_tag',
#     'data.box_condition' : 'sneaker_box_condition',
#     'data.product_condition' : 'sneaker_condition',
#     'data.retail_price_cents': 'retail_price_euros',
#     'data.lowest_price_cents': 'lowest_price_euros',
#     'data.instant_ship_lowest_price_cents': 'instant_ship_price_euros',
#     'data.gp_lowest_price_cents_224': 'gp_lowest_price_euros',
#     'data.gp_instant_ship_lowest_price_cents_224': 'gp_instant_ship_price_euros'
# }, inplace=True)

ordered_data.to_csv('sneakers_data', index = False)