import pandas as pd

def filter_outbound_prices(input_file, output_file):
    data = pd.read_json(input_file)
    print(data.head())

    #Filter the DataFrame
    filtered_data = data[
        (data['retail_price_eur'] >= 50) &
        (data['retail_price_eur'] <= 240) &
        (data['lowest_price_eur'] <= 210) &
        (data['gp_lowest_price_eur'] <= 300)
        # (data['instant_ship_lowest_price_eur'] >= 350)
    ]

    filtered_data.to_json(output_file, orient='records', indent=4)

def filter_release_date(input_file, output_file):
    data = pd.read_json(input_file)
    data = data.dropna(subset=['release_year',
    'release_month','release_day'])

    data.to_json(output_file, orient='records', indent=4)

def filter_box_condition(input_file, output_file):
    data = pd.read_json(input_file)
    data = data.dropna(subset=['box_condition'])

    data.to_json(output_file, orient='records', indent=4)


def filter_null(input_file, output_file):
    data = pd.read_json(input_file)
    data = data.dropna(subset=['retail_price_eur',
    'lowest_price_eur','gp_lowest_price_eur'])

    data.to_json(output_file, orient='records', indent=4)