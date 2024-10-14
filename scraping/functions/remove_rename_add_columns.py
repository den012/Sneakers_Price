import pandas as pd
from pandas import json_normalize
import json


def remove_rename_add_data_cols(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    normalized_data = json_normalize(data)

    columns = [
        "value",
        "sneaker_brand",
        "collaboration",
        "collaboration_name",

        "data.slug",
        "data.color",
        "data.category",
        "data.release_date",
        "data.discount_tag",
        "data.box_condition",
        "data.product_condition",

        "data.retail_price_cents",
        "data.lowest_price_cents",
        "data.instant_ship_lowest_price_cents",
        "data.gp_lowest_price_cents_224",
        "data.gp_instant_ship_lowest_price_cents_224",
    ]

    for column in columns:
        if column not in normalized_data.columns:
            normalized_data[column] = pd.NA

    ordered_data = normalized_data[columns].copy()

    price_columns = [
        "data.retail_price_cents",
        "data.lowest_price_cents",
        "data.instant_ship_lowest_price_cents",
        "data.gp_lowest_price_cents_224",
        "data.gp_instant_ship_lowest_price_cents_224",
    ]

    for column in price_columns:
        if column in ordered_data.columns:
            ordered_data[column] = pd.to_numeric(ordered_data[column], errors='coerce') / 100

    ordered_data.rename(columns={
        "value" : "sneaker_name",
        "data.slug" : "sneaker_slug",
        "data.color" : "sneaker_color",
        "data.category " : "category",
        "data.release_date" : "release_date",
        "data.discount_tag" : "discount_tag",
        "data.box_condition" : "box_condition",
        "data.product_condition" : "product_condition",
        # price columns
        "data.retail_price_cents" : "retail_price_eur",
        "data.lowest_price_cents" : "lowest_price_eur",
        "data.instant_ship_lowest_price_cents" : "instant_ship_lowest_price_eur",
        "data.gp_lowest_price_cents_224" : "gp_lowest_price_eur",
        "data.gp_instant_ship_lowest_price_cents_224" : "gp_instant_ship_lowest_price_eur",
    }, inplace=True)

    with open(json_file, 'w') as file:
        json.dump(json.loads(ordered_data.to_json(orient='records')), file, indent=4)

