import pandas as pd
import json

def clear_columns(input_file, output_file):
    #load json data
    with open(input_file, 'r') as file:
        data = json.load(file)

    # # Remove unwanted columns
    for sneaker in data:
        data_dict = sneaker.pop('data', {})
        sneaker.update({
            'id': data_dict.get('id'),
            'slug': data_dict.get('slug'),
            'color': data_dict.get('color'),
            'image_url': data_dict.get('image_url'),
            'release_date': data_dict.get('release_date'),
            'retail_price_eur': data_dict.get('retail_price_cents_eur'),
            'box_condition': data_dict.get('box_condition'),
            'lowest_price_eur': data_dict.get('lowest_price_cents_eur'),
            # 'instant_ship_lowest_price_eur': data_dict.get('instant_ship_lowest_price_cents_eur'),
            'gp_lowest_price_eur': data_dict.get('gp_lowest_price_cents_224'),
            # 'gp_instant_ship_lowest_price_eur': data_dict.get('gp_instant_ship_lowest_price_cents_224'),
        })
    # Process the release_date and add release_year, release_month, release_day
    for sneaker in data:
        del sneaker['matched_terms']
        del sneaker['is_slotted']
        del sneaker['labels']
        del sneaker['variations_map']
        release_date = sneaker.get('release_date')
        if release_date is not None:
            release_date = int(release_date)
            sneaker['release_year'] = release_date // 10000
            sneaker['release_month'] = (release_date % 10000) // 100
            sneaker['release_day'] = release_date % 100
        else:
            sneaker['release_year'] = None
            sneaker['release_month'] = None
            sneaker['release_day'] = None
        if 'release_date' in sneaker:
            del sneaker['release_date']

    # Convert the JSON data to a DataFrame
    ordered_data = pd.DataFrame(data)

    # Process price columns
    price_columns = [
        "retail_price_eur",
        "lowest_price_eur",
        # "instant_ship_lowest_price_eur",
        "gp_lowest_price_eur",
        # "gp_instant_ship_lowest_price_eur",
    ]

    for column in price_columns:
        if column in ordered_data.columns:
            ordered_data[column] = pd.to_numeric(ordered_data[column], errors='coerce') / 100

    # Rename columns
    ordered_data.rename(columns={
        "value": "sneaker_name",
    }, inplace=True)

    # Save the processed data back to JSON
    with open(output_file, 'w') as file:
        json.dump(json.loads(ordered_data.to_json(orient='records')), file, indent=4)
